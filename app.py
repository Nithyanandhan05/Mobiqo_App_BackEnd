# app.py
import os
from dotenv import load_dotenv

# --- LOAD ENV VARS FIRST BEFORE IMPORTING BLUEPRINTS ---
load_dotenv()

from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from sqlalchemy import text
from google import genai
from google.genai import types
from werkzeug.utils import secure_filename
import re
import urllib.parse
import json
import time

# --- IMPORT THE NEW IMAGE FETCHER ---
from image_fetcher import fetch_dynamic_image

# --- FIREBASE & SCHEDULER IMPORTS ---
import firebase_admin
from firebase_admin import credentials, messaging
from apscheduler.schedulers.background import BackgroundScheduler

from models import db, User, Product, Order, Address, SavedPaymentMethod, NotificationPreference, PrivacySetting, AiSearchLog, AiSetting, Warranty

from payment import payment_bp
from warranty import warranty_bp
from orders import orders_bp
from compare import compare_bp
from admin import admin_bp 

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/smartelectro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'smart-electro-ai-super-secure-secret-key-2026'
app.config['JWT_SECRET_KEY'] = 'smart-electro-ai-super-secure-jwt-key-2026'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

# --- UPLOAD FOLDER CONFIGURATION ---
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- INITIALIZE DB WITH APP ---
db.init_app(app)

# --- REGISTER BLUEPRINTS ---
app.register_blueprint(payment_bp)
app.register_blueprint(warranty_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(compare_bp)
app.register_blueprint(admin_bp) 

# --- AI SETUP (USING ASSISTANT KEY) ---
ASSISTANT_KEY = os.getenv("GEMINI_API_KEY_ASSISTANT")
# os.getenv prevents KeyError if the .env file is missing
client = genai.Client(api_key=ASSISTANT_KEY) if ASSISTANT_KEY else None

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# ==========================================
# FIREBASE SETUP & UNIVERSAL PUSH SENDER
# ==========================================
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase-adminsdk.json")
        firebase_admin.initialize_app(cred)
        print("✅ Firebase Initialized Successfully!")
except Exception as e:
    print(f"⚠️ Firebase Init Error: {e}")

# ==========================================
# WARRANTY SCHEDULER
# ==========================================
def check_warranties_and_notify():
    """Background task to check for warranties expiring in 30 days and 7 days."""
    with app.app_context():
        print("🔍 Running Daily Warranty Check...")
        today = datetime.now().date()
        target_30_days = today + timedelta(days=30)
        target_7_days = today + timedelta(days=7)
        
        all_warranties = Warranty.query.all()
        
        for w in all_warranties:
            if w.expiry_date:
                w_date = w.expiry_date.date() if isinstance(w.expiry_date, datetime) else w.expiry_date
                user = db.session.get(User, w.user_id)
                
                if user:
                    if w_date == target_30_days:
                        send_universal_push_notification(
                            user, 
                            "Warranty Expiring in 1 Month! 📅", 
                            f"Your warranty for {w.device_name} expires in 30 days. Renew now to stay covered."
                        )
                        print(f"📩 30-Day Alert sent to {user.full_name}")
                        
                    elif w_date == target_7_days:
                        send_universal_push_notification(
                            user, 
                            "Warranty Expiring Next Week! ⚠️", 
                            f"Your warranty for {w.device_name} expires in 7 days. Extend it immediately."
                        )
                        print(f"📩 7-Day Alert sent to {user.full_name}")

# Start the background scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=check_warranties_and_notify, trigger="cron", hour=9, minute=0)
scheduler.start()

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def save_product_if_not_exists(phone_data):
    if not phone_data or 'name' not in phone_data:
        return None
        
    product = Product.query.filter_by(name=phone_data['name']).first()
    if not product:
        raw_price = str(phone_data.get('price', '0')).replace('₹', '').replace(',', '').strip()
        try:
            numeric_price = float(raw_price)
        except:
            numeric_price = 0.0

        product = Product(
            name=phone_data['name'], 
            price=numeric_price,
            image_url=phone_data.get('image_url', ''), 
            battery_spec=phone_data.get('battery_spec', 'Standard'),
            display_spec=phone_data.get('display_spec', 'Standard'), 
            processor_spec=phone_data.get('processor_spec', 'Standard'),
            camera_spec=phone_data.get('camera_spec', 'Standard')
        )
        db.session.add(product)
        db.session.commit()
    return product.id

def get_offline_recommendation(budget):
    return {
        "top_match": {
            "name": "Samsung Galaxy S23 FE", "search_name": "Samsung Galaxy S23 FE",
            "price": f"₹{budget}", "match_percent": "95%", "battery_spec": "4500mAh",
            "display_spec": "120Hz Dynamic AMOLED", "processor_spec": "Exynos 2200", "camera_spec": "50MP OIS Triple Camera"
        },
        "alternatives": [], "analysis": "⚠️ AI QUOTA EXCEEDED: Showing offline fallback recommendation to prevent app crash."
    }

# ==========================================
# 1. AUTHENTICATION & SECURITY
# ==========================================
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    clean_email = data.get('email', '').strip().lower()
    clean_password = data.get('password', '').strip()
    
    if User.query.filter_by(email=clean_email).first():
        return jsonify({"status":"error", "message": "Email already exists"}), 400
        
    hashed = bcrypt.generate_password_hash(clean_password).decode('utf-8')
    new_user = User(
        full_name=data.get('full_name', '').strip(), 
        email=clean_email, 
        mobile=data.get('mobile', '').strip(), 
        password=hashed
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"status":"success"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    clean_email = data.get('email', '').strip().lower()
    clean_password = data.get('password', '').strip()
    
    user = User.query.filter_by(email=clean_email).first()
    if user and bcrypt.check_password_hash(user.password, clean_password):
        token = create_access_token(identity=str(user.id))
        is_admin = True if user.email == 'admin@gmail.com' else False
        return jsonify({
            "status": "success",
            "token": token,
            "user_name": user.full_name,
            "is_admin": is_admin 
        }), 200
        
    return jsonify({"status":"error", "message": "Invalid credentials"}), 401

@app.route('/auth/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        current_password = data.get('current_password', '').strip()
        new_password = data.get('new_password', '').strip()

        user = User.query.get(user_id)
        if not user:
            return jsonify({"status": "error", "message": "User not found"}), 404

        if not bcrypt.check_password_hash(user.password, current_password):
            return jsonify({"status": "error", "message": "Incorrect current password"}), 401

        user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
        return jsonify({"status": "success", "message": "Password updated successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/auth/logout-all', methods=['POST'])
@jwt_required()
def logout_all():
    return jsonify({"status": "success", "message": "Logged out of all other devices."}), 200

@app.route('/auth/delete-account', methods=['DELETE'])
@jwt_required()
def delete_account():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"status": "error", "message": "User not found"}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({"status": "success", "message": "Account deleted successfully."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# 2. PROFILE & SETTINGS
# ==========================================
@app.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if not user: return jsonify({"status": "error", "message": "User not found"}), 404
            
        total_orders = Order.query.filter_by(user_id=user_id).count()
        saved_addresses = Address.query.filter_by(user_id=user_id).count()
        
        profile_data = {
            "full_name": user.full_name, "email": user.email, "mobile": user.mobile,
            "total_orders": total_orders, "saved_addresses": saved_addresses,
            "active_warranties": 3, "ai_searches": 42
        }
        return jsonify({"status": "success", "profile": profile_data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/privacy/settings', methods=['GET'])
@jwt_required()
def get_privacy_settings():
    try:
        user_id = get_jwt_identity()
        settings = PrivacySetting.query.filter_by(user_id=user_id).first()
        if not settings:
            settings = PrivacySetting(user_id=user_id, two_factor_auth=False, biometric_login=False)
            db.session.add(settings)
            db.session.commit()
        data = { "two_factor_auth": settings.two_factor_auth, "biometric_login": settings.biometric_login }
        return jsonify({"status": "success", "settings": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/privacy/settings', methods=['PUT'])
@jwt_required()
def update_privacy_settings():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        settings = PrivacySetting.query.filter_by(user_id=user_id).first()
        if not settings:
            settings = PrivacySetting(user_id=user_id)
            db.session.add(settings)

        if 'two_factor_auth' in data: settings.two_factor_auth = data['two_factor_auth']
        if 'biometric_login' in data: settings.biometric_login = data['biometric_login']
        db.session.commit()
        return jsonify({"status": "success", "message": "Privacy settings updated"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/notifications/preferences', methods=['GET'])
@jwt_required()
def get_notification_preferences():
    try:
        user_id = get_jwt_identity()
        prefs = NotificationPreference.query.filter_by(user_id=user_id).first()
        if not prefs:
            prefs = NotificationPreference(user_id=user_id)
            db.session.add(prefs)
            db.session.commit()
            
        data = {
            "order_updates": prefs.order_updates, "warranty_alerts": prefs.warranty_alerts,
            "ai_updates": prefs.ai_updates, "promotions": prefs.promotions, "frequency": prefs.frequency
        }
        return jsonify({"status": "success", "preferences": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/notifications/preferences', methods=['PUT'])
@jwt_required()
def update_notification_preferences():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        prefs = NotificationPreference.query.filter_by(user_id=user_id).first()
        if not prefs:
            prefs = NotificationPreference(user_id=user_id)
            db.session.add(prefs)

        if 'order_updates' in data: prefs.order_updates = data['order_updates']
        if 'warranty_alerts' in data: prefs.warranty_alerts = data['warranty_alerts']
        if 'ai_updates' in data: prefs.ai_updates = data['ai_updates']
        if 'promotions' in data: prefs.promotions = data['promotions']
        if 'frequency' in data: prefs.frequency = data['frequency']

        db.session.commit()
        return jsonify({"status": "success", "message": "Preferences updated"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# 3. AI RECOMMENDATION ENGINE
# ==========================================
@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        budget = data.get('budget', 30000)
        try:
            prompt = f"""
            Recommend a smartphone currently available in India. Budget ₹{budget}, Brand {data.get('brand', 'Any')}.
            CRITICAL RULE: Use live search to find the CURRENT active market price on Amazon India or Flipkart today. Do NOT use old launch prices.
            Return STRICT JSON: {{ "top_match": {{ "name": "Exact Name", "search_name": "Clean Name", "price": "₹XX,XXX", "match_percent": "95%", "battery_spec": "5000mAh", "display_spec": "120Hz", "processor_spec": "Snapdragon", "camera_spec": "50MP" }}, "alternatives": [{{ "name": "Alt 1", "price": "₹YY,YYY", "match_percent": "90%" }}], "analysis": "Brief paragraph." }}
            """
            
            response = client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[{"google_search": {}}], 
                    temperature=0.2 
                )
            )
            
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            result_json = json.loads(re.search(r'\{.*\}', clean_text, re.DOTALL).group(0))
        except Exception as e:
            print(f"AI Fetch Error: {e}")
            result_json = get_offline_recommendation(budget)

        if 'top_match' in result_json:
            top_search = result_json['top_match'].get('search_name', result_json['top_match'].get('name', 'Phone'))
            result_json['top_match']['image_url'] = fetch_dynamic_image(top_search)
            result_json['top_match']['id'] = save_product_if_not_exists(result_json['top_match'])
            safe_brand = urllib.parse.quote(top_search.split()[0] if top_search else "Phone")
            result_json['top_match']['image_urls'] = [
                result_json['top_match']['image_url'], 
                f"https://ui-avatars.com/api/?name={safe_brand}&background=F4FAFF&color=2962FF&size=512&font-size=0.3"
            ]

        if 'alternatives' in result_json:
            for alt in result_json['alternatives']:
                alt['image_url'] = fetch_dynamic_image(alt.get('name', ''))
                alt['id'] = save_product_if_not_exists(alt)
                
        try:
            new_log = AiSearchLog(query=f"Budget: {budget}, Brand: {data.get('brand', 'Any')}")
            db.session.add(new_log)
            db.session.commit()
        except Exception as e:
            print(f"Failed to log AI search: {e}")

        return jsonify({"status": "success", "data": result_json}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/products', methods=['GET'])
def all_products():
    try:
        products = Product.query.order_by(Product.id.desc()).limit(10).all()
        prod_list = [{"id": p.id, "name": p.name, "price": p.price, "image_url": p.image_url} for p in products]
        return jsonify({"status": "success", "products": prod_list}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# 4. ADDRESSES
# ==========================================
@app.route('/add_address', methods=['POST'])
@jwt_required()
def add_address():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        existing = Address.query.filter_by(user_id=user_id).first()
        is_default = True if not existing else False
        new_addr = Address(user_id=user_id, full_name=data.get('full_name'), mobile=data.get('mobile'), pincode=data.get('pincode'), city=data.get('city'), address_line=data.get('address_line'), is_default=is_default)
        db.session.add(new_addr)
        db.session.commit()
        return jsonify({"status": "success", "message": "Address saved successfully"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get_addresses', methods=['GET'])
@jwt_required()
def get_addresses():
    try:
        user_id = get_jwt_identity()
        addrs = Address.query.filter_by(user_id=user_id).all()
        res = [{"id": a.id, "full_name": a.full_name, "mobile": a.mobile, "pincode": a.pincode, "city": a.city, "address_line": a.address_line, "is_default": a.is_default} for a in addrs]
        return jsonify({"status": "success", "addresses": res}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/update_address/<int:id>', methods=['PUT'])
@jwt_required()
def update_address(id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        address = Address.query.filter_by(id=id, user_id=user_id).first()
        if not address: return jsonify({"status":"error", "message":"Address not found"}), 404
        
        address.full_name = data.get('full_name', address.full_name)
        address.mobile = data.get('mobile', address.mobile)
        address.pincode = data.get('pincode', address.pincode)
        address.city = data.get('city', address.city)
        address.address_line = data.get('address_line', address.address_line)
        db.session.commit()
        return jsonify({"status":"success", "message": "Address updated"}), 200
    except Exception as e: 
        return jsonify({"status":"error", "message":str(e)}), 500

@app.route('/delete_address/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_address(id):
    try:
        user_id = get_jwt_identity()
        address = Address.query.filter_by(id=id, user_id=user_id).first()
        if not address: return jsonify({"status":"error", "message":"Address not found"}), 404
        db.session.delete(address)
        db.session.commit()
        return jsonify({"status":"success", "message": "Address deleted"}), 200
    except Exception as e: 
        return jsonify({"status":"error", "message":str(e)}), 500

# ==========================================
# 5. SAVED PAYMENT METHODS
# ==========================================
@app.route('/payment_methods', methods=['GET'])
@jwt_required()
def get_payment_methods():
    try:
        user_id = get_jwt_identity()
        methods = SavedPaymentMethod.query.filter_by(user_id=user_id).all()
        result = [{"id": m.id, "method_type": m.method_type, "details": m.details, "expiry": m.expiry, "is_primary": m.is_primary} for m in methods]
        return jsonify({"status": "success", "methods": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/add_payment_method', methods=['POST'])
@jwt_required()
def add_payment_method():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_method = SavedPaymentMethod(
            user_id=user_id, method_type=data.get('method_type'),
            details=data.get('details'), expiry=data.get('expiry'), is_primary=data.get('is_primary', False)
        )
        db.session.add(new_method)
        db.session.commit()
        return jsonify({"status": "success", "message": "Payment method saved"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/remove_payment_method/<int:id>', methods=['DELETE'])
@jwt_required()
def remove_payment_method(id):
    try:
        user_id = get_jwt_identity()
        method = SavedPaymentMethod.query.filter_by(id=id, user_id=user_id).first()
        if method:
            db.session.delete(method)
            db.session.commit()
            return jsonify({"status": "success", "message": "Removed successfully"}), 200
        return jsonify({"status": "error", "message": "Not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# 6. ULTIMATE DATABASE FIX ROUTE (UPDATED)
# ==========================================
@app.route('/fix_db', methods=['GET'])
def fix_db():
    try:
        db.create_all()
        
        with db.engine.connect() as conn:
            try: conn.execute(text("ALTER TABLE user ADD COLUMN fcm_token_android VARCHAR(255);"))
            except Exception: pass
            
            try: conn.execute(text("ALTER TABLE user ADD COLUMN fcm_token_web VARCHAR(255);"))
            except Exception: pass
            
            try: conn.execute(text("UPDATE user SET fcm_token_android = fcm_token WHERE fcm_token IS NOT NULL AND fcm_token_android IS NULL;"))
            except Exception: pass
            
            try: conn.execute(text("ALTER TABLE `order` ADD COLUMN invoice_no VARCHAR(20) UNIQUE;"))
            except Exception: pass
            try: conn.execute(text("ALTER TABLE `order` ADD COLUMN tracking_number VARCHAR(100);"))
            except Exception: pass
            try: conn.execute(text("ALTER TABLE warranty ADD COLUMN product_id INT;"))
            except Exception: pass
            try: conn.execute(text("ALTER TABLE warranty ADD COLUMN device_type VARCHAR(50);"))
            except Exception: pass
            try: conn.execute(text("ALTER TABLE warranty ADD COLUMN status VARCHAR(20) DEFAULT 'Secure';"))
            except Exception: pass
            try: conn.execute(text("ALTER TABLE warranty ADD COLUMN invoice_url VARCHAR(255);"))
            except Exception: pass
            try: conn.execute(text("ALTER TABLE warranty ADD COLUMN purchase_date DATE;"))
            except Exception: pass
            try: conn.execute(text("ALTER TABLE warranty ADD COLUMN expiry_date DATE;"))
            except Exception: pass
            try: conn.execute(text("ALTER TABLE warranty ADD COLUMN claim_issue_type VARCHAR(100);"))
            except Exception: pass
            try: conn.execute(text("ALTER TABLE warranty ADD COLUMN claim_description TEXT;"))
            except Exception: pass
            try: conn.execute(text("ALTER TABLE warranty ADD COLUMN claim_invoice_url VARCHAR(255);"))
            except Exception: pass
            try: conn.execute(text("ALTER TABLE warranty ADD COLUMN claim_device_url VARCHAR(255);"))
            except Exception: pass
            try: conn.execute(text("ALTER TABLE warranty ADD COLUMN service_mode VARCHAR(100);"))
            except Exception: pass
            try: conn.execute(text("ALTER TABLE product ADD COLUMN stock INT DEFAULT 50;"))
            except Exception: pass
            try: conn.execute(text("ALTER TABLE product ADD COLUMN category VARCHAR(100) DEFAULT 'Electronics';"))
            except Exception: pass

            conn.commit()
            
        return jsonify({"status": "success", "message": "Database upgraded! Dual FCM tokens ready."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# 7. MAGIC ADMIN CREATOR
# ==========================================
@app.route('/fix_admin', methods=['GET'])
def fix_admin():
    try:
        messy_admins = User.query.filter(User.email.ilike('%admin@gmail.com%')).all()
        for bad_admin in messy_admins:
            db.session.delete(bad_admin)
            
        hashed = bcrypt.generate_password_hash('admin123').decode('utf-8')
        clean_admin = User(
            full_name="Enterprise Admin", 
            email="admin@gmail.com", 
            mobile="9999999999", 
            password=hashed
        )
        db.session.add(clean_admin)
        db.session.commit()
        return jsonify({"status": "success", "message": "Admin account fixed! Email: admin@gmail.com | Password: admin123"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# 8. SAVE FCM TOKEN FOR PUSH NOTIFICATIONS
# ==========================================
@app.route('/update_fcm_token', methods=['POST'])
@jwt_required()
def update_fcm_token():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        token = data.get('fcm_token') or data.get('token')
        platform = data.get('platform', 'android').lower()
        
        user = db.session.get(User, user_id)
        if user and token:
            if platform == 'web':
                user.fcm_token_web = token
            else:
                user.fcm_token_android = token
                
            db.session.commit()
            return jsonify({"status": "success", "message": f"{platform.title()} FCM Token updated successfully"}), 200
            
        return jsonify({"status": "error", "message": "Invalid token or user"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# 9. DIRECT DIAGNOSTIC PUSH TEST
# ==========================================
@app.route('/test_push', methods=['POST'])
@jwt_required()
def test_push():
    """A direct route to instantly test push notifications for the logged-in user."""
    try:
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404

        token_android = getattr(user, 'fcm_token_android', None)
        token_web = getattr(user, 'fcm_token_web', None)

        if not token_android and not token_web:
            return jsonify({
                "status": "error",
                "message": "Python sees NO tokens for this user.",
                "db_email": user.email
            }), 400

        tokens_to_notify = []
        if token_android: tokens_to_notify.append(token_android)
        if token_web: tokens_to_notify.append(token_web)

        success_count = 0
        for token in tokens_to_notify:
            try:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title="Test Notification 🚀", 
                        body="Firebase is working perfectly!"
                    ),
                    token=token
                )
                messaging.send(message)
                success_count += 1
            except Exception as e:
                print(f"⚠️ Error sending to token {token}: {e}")

        if success_count > 0:
            return jsonify({
                "status": "success", 
                "message": f"Notification fired successfully to {success_count} devices!",
                "android_token_used": token_android
            }), 200
        else:
            return jsonify({
                "status": "error", 
                "message": "Firebase rejected the tokens. They might be expired."
            }), 400

    except Exception as e:
        return jsonify({"status": "error", "message": "General Crash: " + str(e)}), 500

# ==========================================
# 10. FORCE WARRANTY NOTIFICATION CHECK
# ==========================================
@app.route('/force_check', methods=['GET'])
def force_check():
    try:
        check_warranties_and_notify()
        return "✅ Warranty check triggered! Check your VS Code terminal and your devices.", 200
    except Exception as e:
        return f"❌ FAILED: {str(e)}", 500

@app.route('/create_compare_cache', methods=['GET'])
def create_compare_cache():
    try:
        db.create_all()
        return "✅ Compare Cache Table Created Successfully!"
    except Exception as e:
        return str(e)

@app.route('/fix_compare_table', methods=['GET'])
def fix_compare_table():
    try:
        from sqlalchemy import text
        with db.engine.connect() as conn:
            try: conn.execute(text("ALTER TABLE compare_device_cache ADD COLUMN antutu_score VARCHAR(50);"))
            except Exception: pass
            try: conn.execute(text("ALTER TABLE compare_device_cache ADD COLUMN battery_life VARCHAR(50);"))
            except Exception: pass
            try: conn.execute(text("ALTER TABLE compare_device_cache ADD COLUMN expert_score VARCHAR(50);"))
            except Exception: pass
            conn.commit()
        return "✅ SUCCESS! The missing columns were added to your database.", 200
    except Exception as e:
        return f"❌ FAILED: {str(e)}", 500

# ==========================================
# APP RUNNER
# ==========================================
if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)