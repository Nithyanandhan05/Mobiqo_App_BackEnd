# payment.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid
import razorpay
from datetime import datetime, timedelta
from models import db, Order, Payment, Warranty, Product

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
        if order:
            order.status = "Paid & Processing"
            order.payment_method = payment_method 
            
        transaction_id = razorpay_payment_id if razorpay_payment_id else f"TXN-{uuid.uuid4().hex[:8].upper()}"
        
        # 2. Save the payment (FIXED: Removed user_id as it doesn't exist in the Payment table)
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
        
        # 3. AUTO-REGISTER WARRANTY
        if order and order.product_id:
            product = db.session.get(Product, order.product_id)
            if product:
                today = datetime.now().date()
                expiry = today + timedelta(days=365) # Standard 1 Year Warranty
                
                device_type = 'Smartphone'
                name_lower = product.name.lower()
                if 'macbook' in name_lower or 'laptop' in name_lower:
                    device_type = 'Laptop'
                elif any(x in name_lower for x in ['headphone', 'airpods', 'buds', 'sony']):
                    device_type = 'Headphones'

                auto_warranty = Warranty(
                    user_id=user_id,
                    product_id=product.id,
                    device_name=product.name,
                    device_type=device_type,
                    purchase_date=today,
                    expiry_date=expiry,
                    status="Secure"
                )
                db.session.add(auto_warranty)
                print(f"✅ Auto-Warranty activated for {product.name}")

        # Commit everything (Order update, Payment, and new Warranty) at once
        db.session.commit()
        
        return jsonify({"status": "success", "message": "Payment successful and Warranty Registered!", "transaction_id": transaction_id}), 200
    except Exception as e:
        db.session.rollback()
        print(f"❌ PROCESS PAYMENT ERROR: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@payment_bp.route('/payment_history', methods=['GET'])
@jwt_required()
def get_payment_history():
    try:
        user_id = get_jwt_identity()
        
        # FIXED: We find the payments by checking the user's orders first
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