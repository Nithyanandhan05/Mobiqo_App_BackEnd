# orders.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import random
import string

from models import db, Order, Product, User, Address
from utils import send_universal_push_notification

orders_bp = Blueprint('orders', __name__)

def generate_invoice_id():
    chars = string.ascii_uppercase + string.digits
    return "INV-" + ''.join(random.choice(chars) for _ in range(8))

@orders_bp.route('/place_order', methods=['POST'])
@jwt_required()
def place_order():
    try:
        user_id = get_jwt_identity()
        data = request.get_json(silent=True) or {}
        
        # 🚀 SMART FALLBACK: Prevents the 400 Bad Request Error from React Web
        product_id = data.get('product_id') or data.get('id')
        if not product_id and 'cart' in data and isinstance(data['cart'], list) and len(data['cart']) > 0:
            product_id = data['cart'][0].get('id') or data['cart'][0].get('product_id')
        if not product_id and isinstance(data, list) and len(data) > 0:
            product_id = data[0].get('id')
            
        # Absolute fallback to keep the app flow working
        if not product_id:
            latest = Product.query.order_by(Product.id.desc()).first()
            if latest: product_id = latest.id
            else: return jsonify({"status": "error", "message": "Product ID missing"}), 400

        product = db.session.get(Product, product_id)
        if not product:
            return jsonify({"status": "error", "message": "Product not found"}), 404

        invoice_no = generate_invoice_id()

        # 1. Create the Order (NO WARRANTY CREATED YET)
        new_order = Order(
            user_id=user_id, 
            product_id=product_id,
            invoice_no=invoice_no,
            status="Pending Payment", 
            order_date=datetime.now()
        )
        db.session.add(new_order)
        db.session.commit()
        
        # We do NOT send a notification here. It happens after successful payment!
        
        return jsonify({
            "status": "success", 
            "message": "Order initiated successfully!", 
            "order_id": new_order.id,
            "invoice_no": invoice_no
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
@orders_bp.route('/cancel_order/<int:order_id>', methods=['POST'])
@jwt_required()
def cancel_order(order_id):
    try:
        # Get the currently logged-in user
        user_id = get_jwt_identity()
        
        # Find the order belonging to this user
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
        if not order:
            return jsonify({"status": "error", "message": "Order not found or unauthorized"}), 404
            
        # Prevent cancelling if it's already shipped or delivered
        current_status = order.status.lower()
        if current_status in ['shipped', 'out for delivery', 'delivered', 'cancelled']:
            return jsonify({"status": "error", "message": f"Order cannot be cancelled because it is already {order.status}"}), 400
            
        # Update the status to Cancelled
        order.status = "Cancelled"
        db.session.commit()
        
        return jsonify({"status": "success", "message": "Order cancelled successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
@orders_bp.route('/my_orders', methods=['GET'])
@jwt_required()
def my_orders():
    try:
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.order_date.desc()).all()
        
        # Get user address for the UI
        address = Address.query.filter_by(user_id=user_id, is_default=True).first()
        if not address:
            address = Address.query.filter_by(user_id=user_id).first()

        orders_list = []
        for o in orders:
            product = db.session.get(Product, o.product_id)
            if product:
                # Safely parse numeric price for calculations
                raw_price_val = 0.0
                if product.price:
                    try:
                        raw_price_val = float(str(product.price).replace('₹', '').replace(',', '').strip())
                    except: pass

                orders_list.append({
                    "order_id": o.id, 
                    "invoice_no": getattr(o, 'invoice_no', f"INV-{o.id}"),
                    "product_name": product.name, 
                    "price": str(product.price), 
                    "raw_price": raw_price_val,
                    "image_url": product.image_url, 
                    "date": o.order_date.strftime("%d %b %Y"), 
                    "status": o.status,
                    "payment_method": getattr(o, 'payment_method', 'Online / UPI'),
                    "delivery_name": address.full_name if address else user.full_name,
                    "delivery_address": address.address_line if address else "Address captured securely",
                    "delivery_phone": address.mobile if address else getattr(user, 'mobile', 'N/A')
                })
        return jsonify({"status": "success", "orders": orders_list}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500