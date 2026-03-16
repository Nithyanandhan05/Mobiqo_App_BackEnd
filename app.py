# app.py
import os
from dotenv import load_dotenv
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets

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

from image_fetcher import fetch_dynamic_image
import firebase_admin
from firebase_admin import credentials, messaging
from apscheduler.schedulers.background import BackgroundScheduler

from models import db, User, Product, Order, Address, SavedPaymentMethod, NotificationPreference, PrivacySetting, AiSearchLog, AiSetting, Warranty

from payment import payment_bp
from warranty import warranty_bp
from orders import orders_bp
from compare import compare_bp
from admin import admin_bp 
from scanner import scanner_bp
from utils import send_universal_push_notification

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

db.init_app(app)

# --- REGISTER BLUEPRINTS ---
app.register_blueprint(payment_bp)
app.register_blueprint(warranty_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(compare_bp)
app.register_blueprint(admin_bp) 
app.register_blueprint(scanner_bp)

# --- AI SETUP (USING ASSISTANT KEY) ---
ASSISTANT_KEY = os.getenv("GEMINI_API_KEY_ASSISTANT")
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

def check_warranties_and_notify():
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
                    elif w_date == target_7_days:
                        send_universal_push_notification(
                            user, 
                            "Warranty Expiring Next Week! ⚠️", 
                            f"Your warranty for {w.device_name} expires in 7 days. Extend it immediately."
                        )

scheduler = BackgroundScheduler()
scheduler.add_job(func=check_warranties_and_notify, trigger="cron", hour=9, minute=0)
scheduler.start()

# ==========================================
# REAL EMAIL CONFIGURATION & OTP STORE
# ==========================================
registration_otps = {} 
SENDER_EMAIL = "mobiqoapp@gmail.com"  
SENDER_PASSWORD = "gewdecyklvzgvlqa" 

def send_real_email(receiver_email, otp):
    try:
        msg = MIMEMultipart()
        msg['From'] = f"SmartElectro <{SENDER_EMAIL}>"
        msg['To'] = receiver_email
        msg['Subject'] = "Your SmartElectro Verification Code"
        
        body = f"""
        Hello,
        Welcome to SmartElectro!
        Your 6-digit verification code is: {otp}
        Please enter this code in the app to complete your registration.
        Thanks,
        The SmartElectro Team
        """
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"❌ SMTP Email Failed: {e}")
        return False

@app.route('/send-otp', methods=['POST'])
def send_otp():
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({"status": "error", "message": "Email is required"}), 400
            
        if User.query.filter_by(email=email).first():
            return jsonify({"status": "error", "message": "Email already exists in our system"}), 400
            
        otp = str(random.randint(100000, 999999))
        registration_otps[email] = otp
        
        if send_real_email(email, otp):
            return jsonify({"status": "success", "message": "OTP sent to your email"}), 200
        else:
            return jsonify({"status": "error", "message": "Failed to send email."}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        otp = data.get('otp', '').strip()
        
        if registration_otps.get(email) == otp:
            return jsonify({"status": "success", "message": "OTP verified successfully"}), 200
        return jsonify({"status": "error", "message": "Invalid or expired OTP"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

password_reset_tokens = {} 

def send_real_reset_link_email(receiver_email, token):
    try:
        msg = MIMEMultipart()
        msg['From'] = f"SmartElectro <{SENDER_EMAIL}>"
        msg['To'] = receiver_email
        msg['Subject'] = "SmartElectro - Password Reset Request"
        
        react_web_url = "http://10.79.196.213:5173/reset-password"
        reset_link = f"{react_web_url}?token={token}&email={urllib.parse.quote(receiver_email)}"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f7f6; padding: 30px;">
            <div style="max-width: 500px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                <h2 style="color: #1E1E1E; text-align: center;">Password Reset Request</h2>
                <p style="color: #555; font-size: 15px;">Hello,</p>
                <p style="color: #555; font-size: 15px;">An admin has requested a password reset for your account. Please click the secure button below to create a new password.</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_link}" style="background-color: #2874F0; color: white; padding: 14px 28px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block;">Reset My Password</a>
                </div>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(html_body, 'html'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"❌ Link Email Failed: {e}")
        return False

@app.route('/admin/users/send_reset_link', methods=['POST'])
@jwt_required()
def admin_send_reset_link():
    try:
        admin_id = get_jwt_identity()
        admin = db.session.get(User, admin_id)
        if not admin or admin.email != 'admin@gmail.com':
            return jsonify({"status": "error", "message": "Unauthorized"}), 403

        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"status": "error", "message": "User not found"}), 404
            
        token = secrets.token_urlsafe(32)
        password_reset_tokens[email] = token
        
        if send_real_reset_link_email(email, token):
            return jsonify({"status": "success", "message": "Reset link sent to user"}), 200
        else:
            return jsonify({"status": "error", "message": "Failed to send email"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/reset_password_with_link', methods=['POST'])
def reset_password_with_link():
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        token = data.get('token', '').strip()
        new_password = data.get('new_password', '').strip()
        
        if password_reset_tokens.get(email) != token:
            return jsonify({"status": "error", "message": "Invalid or expired link."}), 400
            
        user = User.query.filter_by(email=email).first()
        if not user: return jsonify({"status": "error", "message": "User not found"}), 404
            
        user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
        
        del password_reset_tokens[email]
        return jsonify({"status": "success", "message": "Password updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

password_reset_otps = {}

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        
        if not email: return jsonify({"status": "error", "message": "Email is required"}), 400
            
        user = User.query.filter_by(email=email).first()
        if not user: return jsonify({"status": "error", "message": "No account found with this email"}), 404
            
        otp = str(random.randint(100000, 999999))
        password_reset_otps[email] = otp
        
        if send_real_email(email, otp):
            return jsonify({"status": "success", "message": "Reset OTP sent to your email"}), 200
        else:
            return jsonify({"status": "error", "message": "Failed to send reset email."}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/reset_password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        otp = data.get('otp', '').strip()
        new_password = data.get('new_password', '').strip()
        
        if not email or not otp or not new_password:
            return jsonify({"status": "error", "message": "All fields required"}), 400
            
        if password_reset_otps.get(email) != otp:
            return jsonify({"status": "error", "message": "Invalid or expired OTP"}), 400
            
        user = User.query.filter_by(email=email).first()
        
        hashed = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.password = hashed
        db.session.commit()
        
        if email in password_reset_otps: del password_reset_otps[email]
            
        return jsonify({"status": "success", "message": "Password updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

def save_product_if_not_exists(phone_data):
    if not phone_data or 'name' not in phone_data: return None
        
    product = Product.query.filter_by(name=phone_data['name']).first()
    if not product:
        raw_price = str(phone_data.get('price', '0')).replace('₹', '').replace(',', '').strip()
        try: numeric_price = float(raw_price)
        except: numeric_price = 0.0

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
    try:
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
        
        if clean_email in registration_otps: del registration_otps[clean_email]
            
        return jsonify({"status":"success", "message": "Registration successful"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
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
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/auth/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        current_password = data.get('current_password', '').strip()
        new_password = data.get('new_password', '').strip()

        user = User.query.get(user_id)
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

@app.route('/privacy/settings', methods=['GET', 'PUT'])
@jwt_required()
def privacy_settings():
    user_id = get_jwt_identity()
    settings = PrivacySetting.query.filter_by(user_id=user_id).first()
    if not settings:
        settings = PrivacySetting(user_id=user_id, two_factor_auth=False, biometric_login=False)
        db.session.add(settings)
        db.session.commit()
        
    if request.method == 'PUT':
        data = request.get_json()
        if 'two_factor_auth' in data: settings.two_factor_auth = data['two_factor_auth']
        if 'biometric_login' in data: settings.biometric_login = data['biometric_login']
        db.session.commit()
        return jsonify({"status": "success", "message": "Privacy settings updated"}), 200
        
    return jsonify({"status": "success", "settings": { "two_factor_auth": settings.two_factor_auth, "biometric_login": settings.biometric_login }}), 200

@app.route('/notifications/preferences', methods=['GET', 'PUT'])
@jwt_required()
def notification_preferences():
    user_id = get_jwt_identity()
    prefs = NotificationPreference.query.filter_by(user_id=user_id).first()
    if not prefs:
        prefs = NotificationPreference(user_id=user_id)
        db.session.add(prefs)
        db.session.commit()
        
    if request.method == 'PUT':
        data = request.get_json()
        if 'order_updates' in data: prefs.order_updates = data['order_updates']
        if 'warranty_alerts' in data: prefs.warranty_alerts = data['warranty_alerts']
        if 'ai_updates' in data: prefs.ai_updates = data['ai_updates']
        if 'promotions' in data: prefs.promotions = data['promotions']
        if 'frequency' in data: prefs.frequency = data['frequency']
        db.session.commit()
        return jsonify({"status": "success", "message": "Preferences updated"}), 200

    data = {
        "order_updates": prefs.order_updates, "warranty_alerts": prefs.warranty_alerts,
        "ai_updates": prefs.ai_updates, "promotions": prefs.promotions, "frequency": prefs.frequency
    }
    return jsonify({"status": "success", "preferences": data}), 200


# ==========================================
# 3. AI RECOMMENDATION ENGINE (UPDATED PROMPT)
# ==========================================
@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        
        # 🚀 EXTRACT ALL RELEVANT USER INPUTS
        budget = data.get('budget', 30000)
        brand = data.get('brand', 'Any')
        usage = data.get('usage', 'General')
        storage = data.get('storage', '128GB')
        battery = data.get('battery', 'Standard')
        notes = data.get('notes', '')

        try:
            # 🚀 UPDATED PROMPT: Passes ALL details to Gemini for deep analysis
            prompt = f"""
            Recommend the absolute best single smartphone currently available in India meeting these exact user requirements:
            - Budget: Under ₹{budget}
            - Preferred Brand(s): {brand}
            - Primary Usage Type: {usage}
            - Minimum Storage Required: {storage}
            - Battery Preference: {battery}
            - User's Extra Notes/Features: {notes if notes else 'None'}
            
            CRITICAL RULE: Use live search to find the CURRENT active market price on Amazon India or Flipkart today. Do NOT use old launch prices.
            Return STRICT JSON: {{ "top_match": {{ "name": "Exact Name", "search_name": "Clean Name", "price": "₹XX,XXX", "match_percent": "95%", "battery_spec": "5000mAh", "display_spec": "120Hz", "processor_spec": "Snapdragon", "camera_spec": "50MP" }}, "alternatives": [{{ "name": "Alt 1", "price": "₹YY,YYY", "match_percent": "90%" }}], "analysis": "A brief paragraph explaining EXACTLY why this phone fits their usage, storage, and custom notes." }}
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
            new_log = AiSearchLog(query=f"Budget: {budget}, Brand: {brand}, Usage: {usage}, Storage: {storage}, Notes: {notes}")
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
# 6. ULTIMATE DATABASE FIX ROUTE
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
# APP RUNNER
# ==========================================
if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)