# payment.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid
import razorpay
from datetime import datetime
from models import db, Order, Payment, Product, User
from utils import send_universal_push_notification

payment_bp = Blueprint('payment', __name__)

# ==========================================
# RAZORPAY CONFIGURATION
# ==========================================
# Replace these with your actual Test API Keys from the Razorpay Dashboard
RAZORPAY_KEY_ID = "rzp_test_APuQCp0MiHoD9M"
RAZORPAY_KEY_SECRET = "06kTw2BRDXPQ3FUuhBZTrPXZ"

razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

@payment_bp.route('/create_razorpay_order', methods=['POST'])
@jwt_required()
def create_razorpay_order():
    try:
        data = request.get_json()
        amount = float(data.get('amount', 0)) * 100 # Razorpay expects amount in PAISE

        order_data = {
            "amount": int(amount),
            "currency": "INR",
            "payment_capture": "1" # Auto-capture payment
        }
        
        # Call Razorpay to generate a secure Order ID
        razorpay_order = razorpay_client.order.create(data=order_data)
        
        return jsonify({
            "status": "success", 
            "razorpay_order_id": razorpay_order['id']
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@payment_bp.route('/process_payment', methods=['POST'])
@jwt_required()
def process_payment():
    try:
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        data = request.get_json()
        order_id = data.get('order_id')
        
        payment_method = data.get('payment_method') or "Online / Razorpay"
        amount = data.get('amount')
        
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_signature = data.get('razorpay_signature')
        
        if not order_id: 
            return jsonify({"status": "error", "message": "Order ID required"}), 400

        # 1. Update Order Status
        order = db.session.get(Order, order_id)
        product_name = "your item"
        
        if order:
            order.status = "Paid & Processing"
            order.payment_method = payment_method 
            
            # Fetch product name for the notification
            if order.product_id:
                product = db.session.get(Product, order.product_id)
                if product: 
                    product_name = product.name
            
        transaction_id = razorpay_payment_id if razorpay_payment_id else f"TXN-{uuid.uuid4().hex[:8].upper()}"
        
        # 2. Save the payment
        new_payment = Payment(
            order_id=order_id, 
            payment_method=payment_method, 
            amount=amount, 
            transaction_id=transaction_id,
            razorpay_order_id=razorpay_order_id,
            razorpay_signature=razorpay_signature,
            status="Successful"
        )
        db.session.add(new_payment)
        
        # NOTE: Warranty is intentionally NOT registered here anymore. 
        # It is handled in admin.py when the order is marked "Delivered".
        
        db.session.commit()
        
        # 🚀 3. TRIGGER FLIPKART/AMAZON STYLE NOTIFICATION
        send_universal_push_notification(
            user,
            "📦 Order Confirmed!",
            f"Your order for the {product_name} was successful. We will notify you once it dispatches."
        )
        
        return jsonify({
            "status": "success", 
            "message": "Payment successful!", 
            "transaction_id": transaction_id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ PROCESS PAYMENT ERROR: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@payment_bp.route('/payment_history', methods=['GET'])
@jwt_required()
def get_payment_history():
    try:
        user_id = get_jwt_identity()
        
        user_orders = Order.query.filter_by(user_id=user_id).all()
        order_ids = [o.id for o in user_orders]
        
        if not order_ids:
            return jsonify({"status": "success", "history": []}), 200
            
        payments = Payment.query.filter(Payment.order_id.in_(order_ids)).order_by(Payment.created_at.desc()).all()
            
        history_list = []
        for p in payments:
            # Match the order to get the invoice number
            order = next((o for o in user_orders if o.id == p.order_id), None)
            invoice_str = getattr(order, 'invoice_no', None) if order else f"ORD-{p.order_id}"
            
            date_str = p.created_at.strftime("%b %d, %I:%M %p") if p.created_at else "Unknown Date"
            
            raw_status = p.status or "Pending"
            ui_status = "Successful" if raw_status in ["Completed", "Paid & Processing", "Successful"] else raw_status
            
            amount_str = str(p.amount)
            if not amount_str.startswith('₹'):
                amount_str = f"₹{amount_str}"

            history_list.append({
                "id": p.id,
                "order_id": invoice_str,
                "transaction_id": p.transaction_id or "N/A",
                "payment_method": p.payment_method or "Online",
                "amount": amount_str,
                "date": date_str,
                "status": ui_status
            })
            
        return jsonify({"status": "success", "history": history_list}), 200
        
    except Exception as e:
        print(f"PAYMENT HISTORY ERROR: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500