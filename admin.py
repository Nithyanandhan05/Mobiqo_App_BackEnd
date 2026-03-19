# admin.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta, date
from utils import send_universal_push_notification
from models import db, User, Order, Product, Warranty, Address, AiSearchLog, AiSetting
from flask_jwt_extended import jwt_required, get_jwt_identity
admin_bp = Blueprint('admin', __name__)

# ==========================================
# FIREBASE PUSH NOTIFICATION HELPER
# ==========================================
def send_push_notification(user_id, title, body):
    """Helper function to send Firebase push notifications."""
    try:
        user = db.session.get(User, user_id)
        if user and getattr(user, 'fcm_token', None):
            from firebase_admin import messaging
            msg = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                token=user.fcm_token
            )
            messaging.send(msg)
            print(f"✅ FCM SUCCESS: '{title}' sent to {user.full_name}")
        else:
            print("❌ FCM FAILED: No FCM token or user found.")
    except Exception as e:
        print(f"❌ FCM CRASH: {e}")

# ==========================================
# ULTRA-SAFE FORMATTING & STATUS HELPERS
# ==========================================
def format_price_safely(raw_price, decimals=2):
    if raw_price is None: return "₹0.00" if decimals > 0 else "₹0"
    try:
        clean_price = str(raw_price).replace('₹', '').replace(',', '').strip()
        if not clean_price: return "₹0.00" if decimals > 0 else "₹0"
        num_price = float(clean_price)
        if decimals == 0: return f"₹{num_price:,.0f}"
        return f"₹{num_price:,.2f}"
    except Exception: 
        return f"₹{raw_price}"

def format_date_safely(raw_date):
    if not raw_date: return "N/A"
    
    # If it's already a datetime or date object
    if hasattr(raw_date, 'strftime'):
        try:
            return raw_date.strftime("%b %d, %Y")
        except Exception:
            return str(raw_date)
            
    # If it's a string, try parsing multiple formats
    if isinstance(raw_date, str):
        raw_date = raw_date.strip()
        # Try YYYY-MM-DD
        try: 
            return datetime.strptime(raw_date.split(' ')[0], "%Y-%m-%d").strftime("%b %d, %Y")
        except Exception: pass
        # Try Mar 06, 2026
        try: 
            return datetime.strptime(raw_date, "%b %d, %Y").strftime("%b %d, %Y")
        except Exception: pass
        
    return str(raw_date)

def get_dynamic_status(w):
    db_status = getattr(w, 'status', 'Secure')
    if not db_status: db_status = "Secure"
    
    # Do not override pending/rejected statuses
    if str(db_status).strip().lower() in ["pending", "rejected"]: 
        return db_status

    safe_expiry = getattr(w, 'expiry_date', None)
    if not safe_expiry: return "Secure"

    try:
        today = datetime.now().date()
        
        if isinstance(safe_expiry, datetime): 
            safe_expiry = safe_expiry.date()
        elif isinstance(safe_expiry, str):
            try: safe_expiry = datetime.strptime(safe_expiry.split(' ')[0], "%Y-%m-%d").date()
            except Exception: 
                try: safe_expiry = datetime.strptime(safe_expiry, "%b %d, %Y").date()
                except Exception: pass

        if isinstance(safe_expiry, date):
            days = (safe_expiry - today).days
            if days < 0: return "Expired"
            elif days <= 30: return "Alert"
    except Exception as e:
        print(f"Error calculating dynamic status: {e}")
        
    return "Secure"

# ==========================================
# 1. ADMIN DASHBOARD STATS
# ==========================================
@admin_bp.route('/admin/dashboard', methods=['GET'])
@admin_bp.route('/api/admin/dashboard', methods=['GET'])
@jwt_required()
def get_admin_dashboard():
    try:
        total_users = User.query.count()
        total_orders = Order.query.count()
        
        try: active_warranties = Warranty.query.filter_by(status='Secure').count()
        except Exception: active_warranties = 0
            
        try: ai_searches = AiSearchLog.query.count() 
        except Exception: ai_searches = 0
        
        recent_orders = Order.query.order_by(Order.id.desc()).limit(3).all()
        orders_data = []
        
        for o in recent_orders:
            prod = db.session.get(Product, o.product_id) if o.product_id else None
            orders_data.append({
                "id": o.id,
                "name": str(prod.name) if prod and prod.name else "Unknown Product",
                "price": format_price_safely(prod.price, decimals=0) if prod else "₹0", 
                "status": str(o.status) if o.status else "Pending"
            })

        return jsonify({
            "status": "success",
            "stats": {
                "total_users": str(total_users),
                "total_orders": str(total_orders),
                "active_warranties": str(active_warranties),
                "ai_searches": str(ai_searches),
                "pending_claims": str(Warranty.query.filter_by(status='Pending').count()),
                "revenue": "₹" + str(total_orders * 1500) 
            },
            "recent_claims": [], 
            "recent_orders": orders_data, # FIXED: Added this back to the JSON payload
            "trending_queries": [{"query": "Best gaming phone under 30k", "count": "142"}]
        }), 200
    except Exception as e:
        print(f"ADMIN DASHBOARD ERROR: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# 2. ORDER MANAGEMENT
# ==========================================
@admin_bp.route('/admin/orders', methods=['GET'])
@admin_bp.route('/api/admin/orders', methods=['GET'])
@jwt_required()
def get_all_orders():
    try:
        orders = Order.query.order_by(Order.id.desc()).all()
        orders_data = []
        
        for o in orders:
            prod = db.session.get(Product, o.product_id) if o.product_id else None
            user = db.session.get(User, o.user_id) if o.user_id else None
            
            address_line = "742 Evergreen Terrace, Springfield"
            if o.user_id:
                address = Address.query.filter_by(user_id=o.user_id, is_default=True).first()
                if not address:
                    address = Address.query.filter_by(user_id=o.user_id).first()
                if address and address.address_line:
                    address_line = str(address.address_line)
            
            inv_no = getattr(o, 'invoice_no', None)
            track_no = getattr(o, 'tracking_number', "")
            
            orders_data.append({
                "id": o.id,
                "invoice_no": str(inv_no) if inv_no else f"#ORD-{o.id}",
                "customer_name": str(user.full_name) if user and user.full_name else "Guest User",
                "product_name": str(prod.name) if prod and prod.name else "Legacy Product",
                "sku": f"SKU-{prod.id}-2026" if prod else f"SKU-GEN-{o.id}",
                "price": format_price_safely(prod.price, decimals=2) if prod else "₹0.00",
                "status": str(o.status) if o.status else "Pending",
                "tracking_number": str(track_no) if track_no else "",
                "address": address_line
            })
            
        return jsonify({"status": "success", "orders": orders_data}), 200
    except Exception as e:
        print(f"ADMIN ORDERS GET ERROR: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Replace ONLY the update_order function in your admin.py file with this:

@admin_bp.route('/admin/orders/<int:order_id>', methods=['PUT'])
@admin_bp.route('/api/admin/orders/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    try:
        data = request.get_json(silent=True) or {}
        order = db.session.get(Order, order_id)
        if not order: return jsonify({"status": "error", "message": "Order not found"}), 404
        
        old_status = order.status
        if 'status' in data: order.status = str(data['status'])
        if 'tracking_number' in data: order.tracking_number = str(data['tracking_number'])
        
        product_name = "your item"
        prod = None
        if order.product_id:
            prod = db.session.get(Product, order.product_id)
            if prod: product_name = prod.name

        # 🚀 WARRANTY GENERATION ON DELIVERY 🚀
        if order.status == "Delivered" and old_status != "Delivered":
            existing_w = Warranty.query.filter_by(user_id=order.user_id, product_id=order.product_id).first()
            if not existing_w and prod:
                dev_type = 'Laptop' if 'laptop' in prod.name.lower() or 'macbook' in prod.name.lower() else 'Smartphone'
                new_warranty = Warranty(
                    user_id=order.user_id, product_id=prod.id, device_name=prod.name, 
                    device_type=dev_type, purchase_date=datetime.now().date(), 
                    expiry_date=datetime.now().date() + timedelta(days=365), status="Secure"
                )
                db.session.add(new_warranty)

        db.session.commit()

        # 🚀 DYNAMIC MODERN TRACKING NOTIFICATIONS
        if order.user_id and old_status != order.status:
            user = db.session.get(User, order.user_id)
            if order.status == "Shipped":
                title, body = "🚚 Order Shipped!", f"Good news! Your {product_name} has been packed and dispatched."
            elif order.status == "Out for Delivery":
                title, body = "🛵 Arriving Today!", f"Get ready! Your {product_name} is out for delivery. Keep your phone handy."
            elif order.status == "Delivered":
                title, body = "✅ Package Delivered", f"Your {product_name} was delivered. Your 1-Year Warranty is now active. Enjoy!"
            else:
                title, body = "📦 Order Update", f"Your order status has been updated to: {order.status}."
                
            send_universal_push_notification(user, title, body)

        return jsonify({"status": "success", "message": "Order updated"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
# ==========================================
# 3. WARRANTY MANAGEMENT (ADMIN)
# ==========================================
@admin_bp.route('/admin/warranties', methods=['GET'])
@admin_bp.route('/api/admin/warranties', methods=['GET'])
@jwt_required()
def get_admin_warranties():
    try:
        user_id = get_jwt_identity()
        admin_user = User.query.get(user_id)
        
        # Verify Admin Access
        if not admin_user or admin_user.email != 'admin@gmail.com':
            return jsonify({"status": "error", "message": "Unauthorized access"}), 403

        warranties = Warranty.query.order_by(Warranty.id.desc()).all()
        w_list = []
        
        for w in warranties:
            # 🚀 Fetch the User to get Email and Phone
            owner = User.query.get(w.user_id)
            
            # 🚀 Fetch the Product to get the Device Image
            product = Product.query.filter_by(name=w.device_name).first()
            
            # Safely format dates
            p_date = w.purchase_date.strftime('%b %d, %Y') if getattr(w, 'purchase_date', None) else "N/A"
            e_date = w.expiry_date.strftime('%b %d, %Y') if getattr(w, 'expiry_date', None) else "Unknown"

            w_list.append({
                "id": w.id,
                "user_name": owner.full_name if owner else "Unknown User",
                "user_email": owner.email if owner else "N/A",          # Now sending email
                "user_phone": owner.mobile if owner else "N/A",         # Now sending phone
                "device_name": w.device_name,
                "device_type": getattr(w, 'device_type', 'Electronics'),
                "purchase_date": p_date,                                # Now sending purchase date
                "expiry_date": e_date,
                "status": w.status,
                "product_image_url": product.image_url if product else None, # Now sending image
                "claim_reason": getattr(w, 'claim_description', getattr(w, 'claim_issue_type', None)),
                "claim_invoice_url": getattr(w, 'claim_invoice_url', None),
                "claim_device_url": getattr(w, 'claim_device_url', None)
            })

        return jsonify({"status": "success", "warranties": w_list}), 200
        
    except Exception as e:
        print(f"Error fetching admin warranties: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
@admin_bp.route('/admin/warranties/<int:warranty_id>/approve', methods=['PUT'])
@admin_bp.route('/api/admin/warranties/<int:warranty_id>/approve', methods=['PUT'])
@jwt_required()
def approve_warranty(warranty_id):
    try:
        data = request.get_json(silent=True) or {}
        action = data.get('action', '').lower() 
        warranty = db.session.get(Warranty, warranty_id)
        if not warranty: return jsonify({"status": "error", "message": "Warranty not found"}), 404
            
        warranty.status = "Secure" if action == "approve" else "Rejected"
        db.session.commit()

        if warranty.user_id:
            user = db.session.get(User, warranty.user_id)
            status_emoji = "✅" if action == "approve" else "❌"
            send_universal_push_notification(
                user,
                f"Warranty Claim {action.capitalize()}d {status_emoji}",
                f"Your claim for {warranty.device_name} has been {action}d."
            )
        return jsonify({"status": "success", "message": f"Warranty {action}d"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
# ==========================================
# 4. PAYMENT MANAGEMENT (ADMIN) - NEW!
# ==========================================
@admin_bp.route('/admin/payments', methods=['GET'])
@admin_bp.route('/api/admin/payments', methods=['GET'])
@jwt_required()
def get_payments():
    try:
        orders = Order.query.order_by(Order.id.desc()).all()
        payments_data = []
        for o in orders:
            user = db.session.get(User, o.user_id) if o.user_id else None
            prod = db.session.get(Product, o.product_id) if o.product_id else None
            
            payments_data.append({
                "id": o.id,
                "user_name": str(user.full_name) if user and user.full_name else "Guest",
                "transaction_id": getattr(o, 'invoice_no', f"TXN-{o.id}892"),
                "amount": format_price_safely(prod.price) if prod else "₹0",
                "order_id": f"#ORD-{o.id}",
                "status": str(o.status) if o.status else "Pending"
            })
        return jsonify({"status": "success", "payments": payments_data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@admin_bp.route('/admin/payments/<int:payment_id>/refund', methods=['PUT'])
@admin_bp.route('/api/admin/payments/<int:payment_id>/refund', methods=['PUT'])
@jwt_required()
def refund_payment(payment_id):
    try:
        # Using Order ID as Payment ID for this example
        order = db.session.get(Order, payment_id)
        if not order: return jsonify({"status": "error", "message": "Transaction not found"}), 404
        
        order.status = "Refunded"
        db.session.commit()
        return jsonify({"status": "success", "message": "Refund processed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# 5. USER MANAGEMENT (ADMIN)
# ==========================================
@admin_bp.route('/admin/users', methods=['GET'])
@admin_bp.route('/api/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        users = User.query.order_by(User.id.desc()).all()
        user_data = []
        
        for u in users:
            if u.email == 'admin@gmail.com': 
                continue
                
            total_orders = Order.query.filter_by(user_id=u.id).count()
            total_warranties = Warranty.query.filter_by(user_id=u.id).count()
            
            user_data.append({
                "id": u.id,
                "full_name": str(u.full_name) if u.full_name else "Unknown User",
                "email": str(u.email) if u.email else "No Email",
                "reg_date": format_date_safely(u.reg_date),
                "is_blocked": bool(u.is_blocked),
                "total_orders": total_orders,
                "total_warranties": total_warranties
            })
            
        return jsonify({
            "status": "success", 
            "total_users": len(user_data),
            "users": user_data
        }), 200
    except Exception as e:
        print(f"USER MANAGEMENT GET ERROR: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@admin_bp.route('/admin/users/<int:user_id>', methods=['GET'])
@admin_bp.route('/api/admin/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_profile(user_id):
    # FIXED: Added missing user profile endpoint
    try:
        user = db.session.get(User, user_id)
        if not user: return jsonify({"status": "error", "message": "User not found"}), 404

        orders = Order.query.filter_by(user_id=user.id).all()
        warranties = Warranty.query.filter_by(user_id=user.id).all()

        order_data = []
        for o in orders:
            prod = db.session.get(Product, o.product_id) if o.product_id else None
            order_data.append({
                "id": o.id,
                "product_name": str(prod.name) if prod and prod.name else "Unknown",
                "price": format_price_safely(prod.price) if prod else "₹0",
                "status": str(o.status),
                "date": format_date_safely(getattr(o, 'created_at', None)) 
            })

        warranty_data = []
        for w in warranties:
            warranty_data.append({
                "id": w.id,
                "device_name": str(w.device_name),
                "status": get_dynamic_status(w),
                "expiry_date": format_date_safely(w.expiry_date)
            })

        return jsonify({
            "status": "success",
            "user": {
                "id": user.id,
                "full_name": str(user.full_name) if user.full_name else "Unknown",
                "email": str(user.email) if user.email else "N/A",
                "mobile": str(getattr(user, 'phone', 'N/A')), 
                "reg_date": format_date_safely(user.reg_date),
                "is_blocked": bool(user.is_blocked)
            },
            "orders": order_data,
            "warranties": warranty_data
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@admin_bp.route('/admin/users/<int:user_id>/toggle_block', methods=['PUT'])
@admin_bp.route('/api/admin/users/<int:user_id>/toggle_block', methods=['PUT'])
@jwt_required()
def toggle_user_block(user_id):
    try:
        user = db.session.get(User, user_id)
        if not user: return jsonify({"status": "error", "message": "User not found"}), 404
        if user.email == 'admin@gmail.com':
            return jsonify({"status": "error", "message": "Cannot block Enterprise Admin"}), 403
            
        user.is_blocked = not user.is_blocked
        db.session.commit()
        
        status_msg = "Blocked" if user.is_blocked else "Unblocked"
        return jsonify({"status": "success", "message": f"User {status_msg} successfully", "is_blocked": user.is_blocked}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500# ==========================================
# 6. PRODUCT INVENTORY MANAGEMENT
# ==========================================
@admin_bp.route('/admin/products', methods=['GET', 'POST'])
@admin_bp.route('/api/admin/products', methods=['GET', 'POST'])
@jwt_required()
def admin_products():
    if request.method == 'GET':
        try:
            products = Product.query.order_by(Product.id.desc()).all()
            prod_list = []
            for p in products:
                prod_list.append({
                    "id": p.id,
                    "name": str(p.name) if p.name else "Unknown",
                    "price": str(p.price) if p.price else "?0",
                    "image_url": str(p.image_url) if p.image_url else "",
                    "stock": p.stock if p.stock is not None else 0,
                    "category": str(p.category) if p.category else "Electronics",
                    "battery_spec": str(p.battery_spec) if p.battery_spec else "",
                    "display_spec": str(p.display_spec) if p.display_spec else "",
                    "processor_spec": str(p.processor_spec) if p.processor_spec else "",
                    "camera_spec": str(p.camera_spec) if p.camera_spec else ""
                })
            return jsonify({"status": "success", "products": prod_list}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
            
    elif request.method == 'POST':
        try:
            data = request.get_json(silent=True) or {}
            new_prod = Product(
                name=data.get('name', ''),
                price=data.get('price', ''),
                image_url=data.get('image_url', ''),
                battery_spec=data.get('battery_spec', ''),
                display_spec=data.get('display_spec', ''),
                processor_spec=data.get('processor_spec', ''),
                camera_spec=data.get('camera_spec', ''),
                stock=int(data.get('stock', 50)),
                category=data.get('category', 'Electronics')
            )
            db.session.add(new_prod)
            db.session.commit()
            return jsonify({"status": "success", "message": "Product created successfully!"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500

@admin_bp.route('/admin/products/<int:product_id>', methods=['GET'])
@admin_bp.route('/api/admin/products/<int:product_id>', methods=['GET'])
@jwt_required()
def get_admin_product(product_id):
    try:
        p = db.session.get(Product, product_id)
        if not p:
            return jsonify({"status": "error", "message": "Product not found"}), 404
        
        prod_data = {
            "id": p.id,
            "name": str(p.name) if p.name else "Unknown",
            "price": str(p.price) if p.price else "?0",
            "image_url": str(p.image_url) if p.image_url else "",
            "stock": p.stock if p.stock is not None else 0,
            "category": str(p.category) if p.category else "Electronics",
            "battery_spec": str(p.battery_spec) if p.battery_spec else "",
            "display_spec": str(p.display_spec) if p.display_spec else "",
            "processor_spec": str(p.processor_spec) if p.processor_spec else "",
            "camera_spec": str(p.camera_spec) if p.camera_spec else ""
        }
        return jsonify({"status": "success", "product": prod_data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@admin_bp.route('/admin/products/<int:product_id>', methods=['PUT', 'DELETE'])
@admin_bp.route('/api/admin/products/<int:product_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def edit_admin_product(product_id):
    try:
        p = db.session.get(Product, product_id)
        if not p:
            return jsonify({"status": "error", "message": "Product not found"}), 404
            
        if request.method == 'DELETE':
            # Order.product_id is NOT NULL so we can't set it to NULL via ORM.
            # Use raw SQL to temporarily disable FK checks, delete, then re-enable.
            try:
                # Nullable FK (Warranty) - safe to null first
                Warranty.query.filter_by(product_id=product_id).update({"product_id": None})
                db.session.flush()
                # Disable FK checks, delete product row, re-enable
                db.session.execute(db.text("SET FOREIGN_KEY_CHECKS=0"))
                db.session.execute(db.text("DELETE FROM product WHERE id = :pid"), {"pid": product_id})
                db.session.execute(db.text("SET FOREIGN_KEY_CHECKS=1"))
                db.session.commit()
                return jsonify({"status": "success", "message": "Product deleted"}), 200
            except Exception as del_err:
                db.session.rollback()
                db.session.execute(db.text("SET FOREIGN_KEY_CHECKS=1"))
                return jsonify({"status": "error", "message": str(del_err)}), 500
            
        data = request.get_json(silent=True) or {}
        if 'name' in data: p.name = data['name']
        if 'price' in data: p.price = data['price']
        if 'image_url' in data: p.image_url = data['image_url']
        if 'battery_spec' in data: p.battery_spec = data['battery_spec']
        if 'display_spec' in data: p.display_spec = data['display_spec']
        if 'processor_spec' in data: p.processor_spec = data['processor_spec']
        if 'camera_spec' in data: p.camera_spec = data['camera_spec']
        if 'stock' in data: p.stock = int(data['stock'])
        if 'category' in data: p.category = data['category']
        
        db.session.commit()
        return jsonify({"status": "success", "message": "Product updated"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# 7. AI SETTINGS & LOGS (ADMIN)
# ==========================================
@admin_bp.route('/admin/ai_settings', methods=['GET'])
@admin_bp.route('/api/admin/ai_settings', methods=['GET'])
@jwt_required()
def get_ai_settings():
    try:
        # Get or create AiSetting
        settings = AiSetting.query.first()
        if not settings:
            settings = AiSetting()
            db.session.add(settings)
            db.session.commit()
            
        # Get latest AI Search Logs
        logs = AiSearchLog.query.order_by(AiSearchLog.id.desc()).limit(20).all()
        logs_data = []
        for log in logs:
            logs_data.append({
                "log_id": f"SEQ-{log.id:04d}",
                "date": log.timestamp.strftime('%b %d, %H:%M') if log.timestamp else "Unknown",
                "match_percent": log.match_percent or 95,
                "preferences": str(log.preferences or getattr(log, 'query', 'Unknown Query')),
                "product": str(log.recommended_product or "Generic AI Pick")
            })

        data = {
            "is_enabled": settings.is_enabled,
            "gaming": settings.gaming_weight,
            "camera": settings.camera_weight,
            "battery": settings.battery_weight,
            "budget": settings.budget_weight,
            "engine_mode": settings.engine_mode,
            "logs": logs_data
        }
        
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        print(f"Error fetching AI settings: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@admin_bp.route('/admin/ai_settings', methods=['PUT'])
@admin_bp.route('/api/admin/ai_settings', methods=['PUT'])
@jwt_required()
def update_ai_settings():
    try:
        data = request.get_json(silent=True) or {}
        settings = AiSetting.query.first()
        if not settings:
            settings = AiSetting()
            db.session.add(settings)
            
        if 'is_enabled' in data: settings.is_enabled = bool(data['is_enabled'])
        if 'gaming' in data: settings.gaming_weight = int(data['gaming'])
        if 'camera' in data: settings.camera_weight = int(data['camera'])
        if 'battery' in data: settings.battery_weight = int(data['battery'])
        if 'budget' in data: settings.budget_weight = int(data['budget'])
        if 'engine_mode' in data: settings.engine_mode = str(data['engine_mode'])
        
        db.session.commit()
        return jsonify({"status": "success", "message": "AI Settings updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating AI settings: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500 