# orders.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import random
import string

# Import database, models, and notification helper
from models import db, Order, Product, Warranty, User
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
        user = db.session.get(User, user_id)
        product_id = request.get_json().get('product_id')
        
        if not product_id: 
            return jsonify({"status": "error", "message": "Product ID required"}), 400
            
        product = db.session.get(Product, product_id)
        if not product:
            return jsonify({"status": "error", "message": "Product not found"}), 404

        invoice_no = generate_invoice_id()

        # 1. Create the Order
        new_order = Order(
            user_id=user_id, 
            product_id=product_id,
            invoice_no=invoice_no,
            status="Paid",
            order_date=datetime.now()
        )
        db.session.add(new_order)
        
        # 2. Auto-Register Warranty
        expiry_date = datetime.now() + timedelta(days=365)
        device_type = 'Smartphone'
        name_lower = product.name.lower()
        if 'macbook' in name_lower or 'laptop' in name_lower:
            device_type = 'Laptop'
        elif any(x in name_lower for x in ['headphone', 'airpods', 'buds', 'sony']):
            device_type = 'Headphones'

        auto_warranty = Warranty(
            user_id=user_id,
            device_name=product.name,
            device_type=device_type,
            expiry_date=expiry_date,
            status="Secure"
        )
        db.session.add(auto_warranty)
        db.session.commit()

        # 🚀 TRIGGER NOTIFICATION
        send_universal_push_notification(
            user, 
            "Order Confirmed! 🎉", 
            f"Your order for {product.name} was placed successfully. Invoice: {invoice_no}"
        )
        
        return jsonify({
            "status": "success", 
            "message": "Order placed and Warranty auto-registered!", 
            "order_id": new_order.id,
            "invoice_no": invoice_no
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"\n[CRITICAL CHECKOUT ERROR]: {str(e)}\n") 
        return jsonify({"status": "error", "message": "Database error while placing order."}), 500

@orders_bp.route('/my_orders', methods=['GET'])
@jwt_required()
def my_orders():
    try:
        user_id = get_jwt_identity()
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.order_date.desc()).all()
        orders_list = []
        for o in orders:
            product = db.session.get(Product, o.product_id)
            if product:
                orders_list.append({
                    "order_id": o.id, 
                    "invoice_no": getattr(o, 'invoice_no', 'N/A'),
                    "product_name": product.name, 
                    "price": product.price, 
                    "image_url": product.image_url, 
                    "date": o.order_date.strftime("%d %b %Y"), 
                    "status": o.status
                })
        return jsonify({"status": "success", "orders": orders_list}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500