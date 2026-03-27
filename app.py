# app.py — FULL CORRECTED VERSION
# Fix 1: Added phone_model, enc_brand, enc_bestfor, enc_5g loaders
# Fix 2: /recommend now uses build_model_input() + USAGE_TO_CATEGORY
# Fix 3: Added missing React Web Dashboard routes (/privacy_settings, /notifications)

import os
from dotenv import load_dotenv
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets

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
import pandas as pd
import joblib
import numpy as np

from image_fetcher import fetch_dynamic_image
import firebase_admin
from firebase_admin import credentials, messaging
from apscheduler.schedulers.background import BackgroundScheduler

from models import db, User, Product, Order, Address, SavedPaymentMethod, NotificationPreference, PrivacySetting, AiSearchLog, AiSetting, Warranty, Payment, Notification
from payment import payment_bp
from warranty import warranty_bp
from orders import orders_bp
from compare import compare_bp
from admin import admin_bp
from scanner import scanner_bp
from utils import send_universal_push_notification

# ==========================================
# LOAD SMARTPHONE DATASET
# ==========================================
try:
    phone_df = pd.read_csv("smartphones_dataset.csv")
    print(f"✅ Smartphone dataset loaded! Total phones: {len(phone_df)}")
except Exception as e:
    phone_df = None
    print(f"⚠️ Could not load smartphone dataset: {e}")

# ==========================================
# LOAD ALL AI MODEL FILES
# ==========================================
try:
    phone_model = joblib.load('phone_model.pkl')
    enc_brand   = joblib.load('encoder_brand.pkl')
    enc_bestfor = joblib.load('encoder_bestfor.pkl')
    enc_5g      = joblib.load('encoder_5g.pkl')
    print("✅ Local AI Model loaded!")
except Exception as e:
    phone_model = None
    print(f"❌ Local AI model failed to load: {e}")

try:
    feature_columns = joblib.load('feature_columns.pkl')
    print("✅ Feature columns loaded!")
except Exception:
    feature_columns = [
        'price', 'ram', 'storage', 'battery', 'camera_mp',
        '5g_encoded', 'brand_encoded',
        'battery_score', 'camera_score', 'performance_score',
        'price_tier', 'rating',
    ]
    print("⚠️ feature_columns.pkl not found — using defaults")

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/smartelectro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "smart-electro-ai-super-secure-secret-key-2026")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "smart-electro-ai-super-secure-jwt-key-2026")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

app.register_blueprint(payment_bp)
app.register_blueprint(warranty_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(compare_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(scanner_bp)

ASSISTANT_KEY = os.getenv("GEMINI_API_KEY_ASSISTANT")
client = genai.Client(api_key=ASSISTANT_KEY) if ASSISTANT_KEY else None

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# ==========================================
# FIREBASE SETUP
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
        today          = datetime.now().date()
        target_30_days = today + timedelta(days=30)
        target_7_days  = today + timedelta(days=7)
        all_warranties = Warranty.query.all()
        for w in all_warranties:
            if w.expiry_date:
                w_date = w.expiry_date.date() if isinstance(w.expiry_date, datetime) else w.expiry_date
                user   = db.session.get(User, w.user_id)
                if user:
                    if w_date == target_30_days:
                        send_universal_push_notification(user, "Warranty Expiring in 1 Month! 📅", f"Your warranty for {w.device_name} expires in 30 days. Renew now to stay covered.")
                    elif w_date == target_7_days:
                        send_universal_push_notification(user, "Warranty Expiring Next Week! ⚠️", f"Your warranty for {w.device_name} expires in 7 days. Extend it immediately.")

scheduler = BackgroundScheduler()
scheduler.add_job(func=check_warranties_and_notify, trigger="cron", hour=9, minute=0)
scheduler.start()

# ==========================================
# EMAIL CONFIG
# ==========================================
registration_otps   = {}
password_reset_otps = {}
password_reset_tokens = {}

SENDER_EMAIL    = "mobiqoapp@gmail.com"
SENDER_PASSWORD = "gewdecyklvzgvlqa"

def send_real_email(receiver_email, otp):
    try:
        msg = MIMEMultipart()
        msg['From']    = f"SmartElectro <{SENDER_EMAIL}>"
        msg['To']      = receiver_email
        msg['Subject'] = "Your SmartElectro Verification Code"
        body = f"""
        Hello,
        Welcome to SmartElectro!
        Your 6-digit verification code is: {otp}
        Please enter this code in the app to complete your registration or password reset.
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
        data  = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        if not email: return jsonify({"status": "error", "message": "Email is required"}), 400
        if User.query.filter_by(email=email).first(): return jsonify({"status": "error", "message": "Email already exists"}), 400
        otp = str(random.randint(100000, 999999))
        registration_otps[email] = otp
        if send_real_email(email, otp): return jsonify({"status": "success", "message": "OTP sent to your email"}), 200
        return jsonify({"status": "error", "message": "Failed to send email."}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    try:
        data  = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        otp   = data.get('otp', '').strip()
        if registration_otps.get(email) == otp: return jsonify({"status": "success", "message": "Verified"}), 200
        return jsonify({"status": "error", "message": "Invalid OTP"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    try:
        data  = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        if not email: return jsonify({"status": "error", "message": "Email required"}), 400
        user = User.query.filter_by(email=email).first()
        if not user: return jsonify({"status": "success", "message": "Email not found in our system"}), 200
        otp = str(random.randint(100000, 999999))
        password_reset_otps[email] = otp
        if send_real_email(email, otp): return jsonify({"status": "success", "message": "OTP sent"}), 200
        return jsonify({"status": "error", "message": "Email failed."}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/reset_password', methods=['POST'])
def reset_password():
    try:
        data         = request.get_json() or {}
        email        = data.get('email', '').strip().lower()
        otp          = data.get('otp', '').strip()
        new_password = data.get('new_password', '').strip()
        if not email or not otp or not new_password: return jsonify({"status": "error", "message": "Missing fields"}), 400
        if password_reset_otps.get(email) != otp: return jsonify({"status": "error", "message": "Invalid OTP"}), 400
        user = User.query.filter_by(email=email).first()
        user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
        if email in password_reset_otps: del password_reset_otps[email]
        return jsonify({"status": "success", "message": "Password updated"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

def send_real_reset_link_email(receiver_email, token):
    try:
        msg           = MIMEMultipart()
        msg['From']   = f"SmartElectro <{SENDER_EMAIL}>"
        msg['To']     = receiver_email
        msg['Subject']= "SmartElectro - Password Reset Request"
        react_web_url = "http://10.79.196.213:5173/reset-password"
        reset_link    = f"{react_web_url}?token={token}&email={urllib.parse.quote(receiver_email)}"
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f7f6; padding: 30px;">
            <div style="max-width: 500px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                <h2 style="color: #1E1E1E; text-align: center;">Password Reset Request</h2>
                <p style="color: #555; font-size: 15px;">An admin requested a password reset for your account.</p>
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
        admin    = db.session.get(User, admin_id)
        if not admin or admin.email != 'admin@gmail.com': return jsonify({"status": "error", "message": "Unauthorized"}), 403
        data  = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        user  = User.query.filter_by(email=email).first()
        if not user: return jsonify({"status": "error", "message": "User not found"}), 404
        token = secrets.token_urlsafe(32)
        password_reset_tokens[email] = token
        if send_real_reset_link_email(email, token): return jsonify({"status": "success", "message": "Reset link sent"}), 200
        return jsonify({"status": "error", "message": "Failed to send email"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/reset_password_with_link', methods=['POST'])
def reset_password_with_link():
    try:
        data         = request.get_json() or {}
        email        = data.get('email', '').strip().lower()
        token        = data.get('token', '').strip()
        new_password = data.get('new_password', '').strip()
        if password_reset_tokens.get(email) != token: return jsonify({"status": "error", "message": "Invalid link"}), 400
        user = User.query.filter_by(email=email).first()
        if not user: return jsonify({"status": "error", "message": "User not found"}), 404
        user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
        del password_reset_tokens[email]
        return jsonify({"status": "success", "message": "Password updated"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def save_product_if_not_exists(phone_data):
    """
    Safely saves a device to DB. Extracts numerical price via regex, 
    and ensures specs are preserved if provided. Updates price if 0.
    """
    if not phone_data or 'name' not in phone_data: return None
    
    # Safely extract numeric price
    raw_price = str(phone_data.get('price', '0'))
    digits_only = re.sub(r'[^\d.]', '', raw_price)
    try:    numeric_price = float(digits_only) if digits_only else 0.0
    except: numeric_price = 0.0

    product = Product.query.filter_by(name=phone_data['name']).first()
    
    if not product:
        product = Product(
            name=phone_data['name'], 
            price=numeric_price,
            image_url=phone_data.get('image_url', ''),
            battery_spec=phone_data.get('battery_spec', '5000mAh Battery'),
            display_spec=phone_data.get('display_spec', '6.5 inch Display'),
            processor_spec=phone_data.get('processor_spec', 'Octa-Core Processor'),
            camera_spec=phone_data.get('camera_spec', '50MP Camera')
        )
        db.session.add(product)
        db.session.commit()
    else:
        # Update price if it was previously saved as 0
        if product.price == 0.0 and numeric_price > 0:
            product.price = numeric_price
            db.session.commit()
            
    return product.id

def get_offline_recommendation(budget):
    return {
        "top_match": {
            "name": "Samsung Galaxy A35 5G",
            "search_name": "Samsung Galaxy A35 5G",
            "price": f"₹{budget}", "match_percent": "90%",
            "battery_spec": "5000mAh", "display_spec": "6.6 inch 120Hz",
            "processor_spec": "Exynos 1380", "camera_spec": "50MP Camera"
        },
        "alternatives": [],
        "analysis": "Showing offline fallback. Please check your internet connection."
    }

def clean_phone_name(brand, model):
    brand = str(brand).strip()
    model = str(model).strip()
    if model.lower().startswith(brand.lower()):
        return model
    return f"{brand} {model}"

def format_phone_name(row):
    base_name   = clean_phone_name(str(row['brand']), str(row['model']))
    search_name = base_name
    if str(row.get('5g_support', 'No')).lower() in ['yes', 'true', '1', 'y'] and '5g' not in base_name.lower():
        base_name += " 5G"
    try:    ram_val     = int(float(row.get('ram',     8)))
    except: ram_val     = 8
    try:    storage_val = int(float(row.get('storage', 128)))
    except: storage_val = 128
    return f"{base_name} ({ram_val}GB RAM, {storage_val}GB)", search_name

def build_model_input(budget_num, storage_num, battery_str, wants_5g, brand_enc, ram=8, camera_mp=50, rating=4.2):
    battery_mah   = 6000 if battery_str == 'Massive' else 5000
    battery_score = 3 if battery_mah >= 6000 else 2
    camera_score  = 3 if camera_mp >= 108 else (2 if camera_mp >= 50 else 1)
    perf_score    = 3 if ram >= 12 else (2 if ram >= 8 else 1)
    price_tier    = (1 if budget_num < 12000 else
                     2 if budget_num < 20000 else
                     3 if budget_num < 35000 else
                     4 if budget_num < 60000 else 5)
    five_g_enc = enc_5g.transform(['Yes' if wants_5g else 'No'])[0]
    return pd.DataFrame([{
        'price':             budget_num,
        'ram':               ram,
        'storage':           storage_num,
        'battery':           battery_mah,
        'camera_mp':         camera_mp,
        '5g_encoded':        five_g_enc,
        'brand_encoded':     brand_enc,
        'battery_score':     battery_score,
        'camera_score':      camera_score,
        'performance_score': perf_score,
        'price_tier':        price_tier,
        'rating':            rating,
    }])[feature_columns]

USAGE_TO_CATEGORY = {
    'gaming':   ['gaming',      'all-rounder'],
    'camera':   ['camera',      'all-rounder'],
    'battery':  ['battery',     'all-rounder'],
    'business': ['all-rounder', 'flagship',    'battery'],
    'student':  ['budget',      'all-rounder', 'battery'],
    'media':    ['all-rounder', 'battery',     'camera'],
    'general':  ['all-rounder', 'gaming',      'camera'],
    'flagship': ['flagship',    'all-rounder'],
    'budget':   ['budget',      'all-rounder'],
}

def build_detailed_analysis(top, budget_num, usage, brand, storage, battery, notes):
    name      = clean_phone_name(str(top['brand']), str(top['model']))
    price     = int(top['price'])
    ram       = int(top['ram'])
    stor      = int(top['storage'])
    bat       = int(top['battery'])
    cam       = int(top['camera_mp'])
    processor = str(top['processor'])
    rating    = float(top['rating'])
    has_5g    = str(top.get('5g_support', 'No'))
    display   = float(top.get('display_inches', 6.5))
    savings   = budget_num - price

    usage_praise = {
        'gaming':   f"For gaming, the {processor} chipset ensures smooth frame rates with minimal lag, and {ram}GB RAM means you can run multiple apps and games without slowdowns.",
        'camera':   f"For photography, the {cam}MP main camera captures sharp, detailed shots in all lighting conditions.",
        'battery':  f"Built for all-day use, the massive {bat}mAh battery will easily last through a full day of heavy usage without needing a top-up.",
        'business': f"For business use, the {ram}GB RAM handles multitasking effortlessly.",
        'student':  f"Perfect for students — the large {display}\" display is great for reading and note-taking.",
        'media':    f"The large {display}\" display paired with the powerful {processor} makes this an excellent choice for streaming.",
    }
    usage_text   = usage_praise.get(str(usage).lower(), f"As a general-purpose phone, it handles everyday tasks smoothly thanks to {ram}GB RAM and the {processor}.")
    value_text   = f"At ₹{price:,}, it fits within your ₹{budget_num:,} budget." if savings >= 0 else f"At ₹{price:,}, it's a strong choice that justifies the price."
    connectivity = "It also supports 5G connectivity." if has_5g == 'Yes' else "It connects reliably on 4G LTE networks."

    return (
        f"Based on your budget of ₹{budget_num:,}, our AI recommends the {name} as the best match. "
        f"{usage_text} "
        f"The {cam}MP camera system captures stunning photos, while the {bat}mAh battery ensures you stay powered. "
        f"With {stor}GB of onboard storage, you'll have plenty of room. "
        f"{connectivity} {value_text} Rated ⭐{rating}/5 by users."
    )

# ==========================================
# 1. AUTHENTICATION & SECURITY ROUTES
# ==========================================
@app.route('/register', methods=['POST'])
def register():
    try:
        data        = request.get_json()
        clean_email = data.get('email', '').strip().lower()
        if User.query.filter_by(email=clean_email).first(): return jsonify({"status":"error", "message": "Email exists"}), 400
        hashed   = bcrypt.generate_password_hash(data.get('password', '').strip()).decode('utf-8')
        new_user = User(full_name=data.get('full_name','').strip(), email=clean_email, mobile=data.get('mobile','').strip(), password=hashed)
        db.session.add(new_user)
        db.session.commit()
        if clean_email in registration_otps: del registration_otps[clean_email]
        return jsonify({"status":"success", "message": "Registered"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data        = request.get_json()
        clean_email = data.get('email', '').strip().lower()
        user        = User.query.filter_by(email=clean_email).first()
        if user and bcrypt.check_password_hash(user.password, data.get('password','').strip()):
            return jsonify({
                "status":    "success",
                "token":     create_access_token(identity=str(user.id)),
                "user_name": user.full_name,
                "is_admin":  user.email == 'admin@gmail.com'
            }), 200
        return jsonify({"status":"error", "message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/auth/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    try:
        user_id = get_jwt_identity()
        data    = request.get_json()
        user    = User.query.get(user_id)
        if not bcrypt.check_password_hash(user.password, data.get('current_password','').strip()):
            return jsonify({"status": "error", "message": "Incorrect password"}), 401
        user.password = bcrypt.generate_password_hash(data.get('new_password','').strip()).decode('utf-8')
        db.session.commit()
        return jsonify({"status": "success", "message": "Password updated"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/auth/logout-all', methods=['POST'])
@jwt_required()
def logout_all(): 
    try:
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if user:
            # Wipe FCM Push Notification Tokens so active sessions are terminated globally
            user.fcm_token_android = None
            user.fcm_token_web = None
            db.session.commit()
        return jsonify({"status": "success", "message": "Logged out from all devices."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/auth/delete-account', methods=['DELETE'])
@jwt_required()
def delete_account():
    try:
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        
        if not user:
            return jsonify({"status": "error", "message": "User not found"}), 404
        
        # 1. First, delete dependencies (Payments depend on Orders)
        orders = Order.query.filter_by(user_id=user_id).all()
        order_ids = [o.id for o in orders]
        if order_ids:
            Payment.query.filter(Payment.order_id.in_(order_ids)).delete(synchronize_session=False)
            Order.query.filter_by(user_id=user_id).delete(synchronize_session=False)

        # 2. Safely wipe all other User footprint using synchronize_session=False for bulk deletes
        Address.query.filter_by(user_id=user_id).delete(synchronize_session=False)
        SavedPaymentMethod.query.filter_by(user_id=user_id).delete(synchronize_session=False)
        NotificationPreference.query.filter_by(user_id=user_id).delete(synchronize_session=False)
        PrivacySetting.query.filter_by(user_id=user_id).delete(synchronize_session=False)
        Warranty.query.filter_by(user_id=user_id).delete(synchronize_session=False)
        Notification.query.filter_by(user_id=user_id).delete(synchronize_session=False)
        
        # Also clean up AI Search logs associated with this user
        AiSearchLog.query.filter_by(user_id=str(user_id)).delete(synchronize_session=False)

        # 3. Finally, delete the actual User account
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({"status": "success", "message": "Account successfully wiped."}), 200

    except Exception as e:
        db.session.rollback()
        print(f"❌ DELETE ACCOUNT ERROR: {e}") # This will print the exact issue to your VS Code terminal if it ever fails again
        return jsonify({"status": "error", "message": str(e)}), 500
# ==========================================
# 2. PROFILE & SETTINGS
# ==========================================
@app.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        user    = db.session.get(User, user_id)
        if not user: return jsonify({"status": "error", "message": "Not found"}), 404
        return jsonify({"status": "success", "profile": {
            "full_name":         user.full_name,
            "email":             user.email,
            "mobile":            user.mobile,
            "total_orders":      Order.query.filter_by(user_id=user_id).count(),
            "saved_addresses":   Address.query.filter_by(user_id=user_id).count(),
            "active_warranties": 3,
            "ai_searches":       42
        }}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/privacy_settings', methods=['GET', 'PUT'])
@jwt_required()
def privacy_settings():
    user_id  = get_jwt_identity()
    settings = PrivacySetting.query.filter_by(user_id=user_id).first()
    if not settings:
        settings = PrivacySetting(user_id=user_id, two_factor_auth=False, biometric_login=False)
        db.session.add(settings)
        db.session.commit()
    if request.method == 'PUT':
        data = request.get_json()
        if 'two_factor_auth' in data: settings.two_factor_auth = data['two_factor_auth']
        if 'biometric_login'  in data: settings.biometric_login  = data['biometric_login']
        db.session.commit()
        return jsonify({"status": "success", "message": "Privacy settings updated"}), 200
    return jsonify({"status": "success", "settings": {
        "two_factor_auth": settings.two_factor_auth,
        "biometric_login": settings.biometric_login
    }}), 200

@app.route('/notifications/preferences', methods=['GET', 'PUT'])
@jwt_required()
def notification_preferences():
    user_id = get_jwt_identity()
    prefs   = NotificationPreference.query.filter_by(user_id=user_id).first()
    if not prefs:
        prefs = NotificationPreference(user_id=user_id)
        db.session.add(prefs)
        db.session.commit()
    if request.method == 'PUT':
        data = request.get_json()
        if 'order_updates'   in data: prefs.order_updates   = data['order_updates']
        if 'warranty_alerts' in data: prefs.warranty_alerts = data['warranty_alerts']
        if 'ai_updates'      in data: prefs.ai_updates      = data['ai_updates']
        if 'promotions'      in data: prefs.promotions      = data['promotions']
        if 'frequency'       in data: prefs.frequency       = data['frequency']
        db.session.commit()
        return jsonify({"status": "success", "message": "Preferences updated"}), 200
    return jsonify({"status": "success", "preferences": {
        "order_updates":   prefs.order_updates,
        "warranty_alerts": prefs.warranty_alerts,
        "ai_updates":      prefs.ai_updates,
        "promotions":      prefs.promotions,
        "frequency":       prefs.frequency
    }}), 200

@app.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    try:
        mock_notifications = [
            {
                "id": 101,
                "title": "Welcome to SmartElectro AI!",
                "message": "Your personal AI assistant is ready to help you find the best devices.",
                "created_at": (datetime.now() - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M")
            },
            {
                "id": 102,
                "title": "Security Alert",
                "message": "A new login was detected from your account today.",
                "created_at": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
            }
        ]
        return jsonify({"status": "success", "notifications": mock_notifications}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/notifications/<int:notif_id>/read', methods=['PUT'])
@jwt_required()
def mark_notification_read(notif_id):
    return jsonify({"status": "success", "message": "Notification marked as read"}), 200

# ==========================================
# 3. AI RECOMMENDATION ENGINE
# ==========================================
@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data     = request.get_json()
        budget   = data.get('budget',  30000)
        brand    = data.get('brand',   'Any')
        usage    = data.get('usage',   'General')
        storage  = data.get('storage', '128GB')
        battery  = data.get('battery', 'Standard')
        notes    = data.get('notes',   '')
        wants_5g = '5g' in str(notes).lower() or '5g' in str(usage).lower()

        try:    budget_num  = int(float(str(budget).replace('₹','').replace(',','').strip()))
        except: budget_num  = 30000
        try:    storage_num = int(''.join(filter(str.isdigit, str(storage)))) or 128
        except: storage_num = 128

        brand_list = []
        if brand and brand.lower() not in ['any', 'all', '']:
            brand_list = [b.strip().lower() for b in str(brand).split(',') if b.strip()]

        result_json = None

        if phone_model is not None and phone_df is not None:
            try:
                brand_enc = 0
                if brand_list:
                    cap = brand_list[0].capitalize()
                    if cap in enc_brand.classes_:
                        brand_enc = enc_brand.transform([cap])[0]

                model_input   = build_model_input(budget_num, storage_num, battery, wants_5g, brand_enc)
                ml_pred_enc   = phone_model.predict(model_input)[0]
                ml_pred_usage = enc_bestfor.inverse_transform([ml_pred_enc])[0]

                usage_key           = str(usage).lower().strip()
                priority_categories = list(USAGE_TO_CATEGORY.get(usage_key, ['all-rounder']))
                if ml_pred_usage not in priority_categories:
                    priority_categories.append(ml_pred_usage)

                filtered_base = phone_df[
                    (phone_df['price'] >= budget_num * 0.7) &
                    (phone_df['price'] <= budget_num * 1.1)
                ].copy()

                if brand_list:
                    brand_match = filtered_base[filtered_base['brand'].str.lower().isin(brand_list)]
                    if not brand_match.empty:
                        filtered_base = brand_match
                    else:
                        wider = phone_df[phone_df['brand'].str.lower().isin(brand_list)].copy()
                        if not wider.empty:
                            filtered_base = wider

                final_filtered = pd.DataFrame()
                for cat in priority_categories:
                    cat_match = filtered_base[filtered_base['best_for'].str.lower() == cat.lower()]
                    if not cat_match.empty:
                        final_filtered = cat_match
                        break

                if final_filtered.empty:
                    final_filtered = filtered_base

                final_filtered = (
                    final_filtered
                    .sort_values('rating', ascending=False)
                    .drop_duplicates(subset=['brand', 'model'])
                )

                if not final_filtered.empty:
                    top  = final_filtered.iloc[0]
                    alts = final_filtered[final_filtered['model'] != top['model']].head(2)
                    top_display, top_search = format_phone_name(top)

                    result_json = {
                        "top_match": {
                            "name":           top_display,
                            "search_name":    top_search,
                            "price":          f"₹{int(top['price']):,}",
                            "match_percent":  f"{int(top['rating'] * 20)}%",
                            "battery_spec":   f"{int(top['battery'])}mAh",
                            "display_spec":   f"{top['display_inches']} inch Display",
                            "processor_spec": str(top['processor']),
                            "camera_spec":    f"{int(top['camera_mp'])}MP Camera",
                        },
                        "alternatives": [],
                        "analysis": build_detailed_analysis(top, budget_num, usage, brand, storage, battery, notes)
                    }

                    # --- FIXED: Alternatives now include specs ---
                    for _, r in alts.iterrows():
                        alt_display, alt_search = format_phone_name(r)
                        result_json["alternatives"].append({
                            "name":          alt_display,
                            "search_name":   alt_search,
                            "price":         f"₹{int(r['price']):,}",
                            "match_percent": f"{int(r['rating'] * 18)}%",
                            "battery_spec":  f"{int(r.get('battery', 5000))}mAh",
                            "display_spec":  f"{r.get('display_inches', 6.5)} inch Display",
                            "processor_spec": str(r.get('processor', 'Octa-Core')),
                            "camera_spec":   f"{int(r.get('camera_mp', 50))}MP Camera"
                        })

            except Exception as e:
                print(f"Local AI error: {e}")
                result_json = None

        if result_json is None:
            try:
                phone_context = ""
                if phone_df is not None:
                    usage_cats = USAGE_TO_CATEGORY.get(str(usage).lower(), ['all-rounder'])
                    fallback   = phone_df[
                        (phone_df['price']    >= budget_num * 0.7) &
                        (phone_df['price']    <= budget_num * 1.1) &
                        (phone_df['best_for'].str.lower().isin(usage_cats))
                    ].drop_duplicates(subset=['brand','model']).head(10)
                    if not fallback.empty:
                        phone_context = f"Phones from our database:\n{fallback[['brand','model','price','ram','storage','battery','camera_mp','processor','best_for','rating']].to_string(index=False)}"

                # --- FIXED: Gemini prompt forces alternative specs ---
                prompt = f"""You are a smartphone expert for SmartElectro India.
{phone_context}
User: Budget ₹{budget_num}, Brand: {brand}, Usage: {usage}, Storage: {storage}, Battery: {battery}.
Recommend the BEST phone specifically for {usage}. Alternatives must be DIFFERENT phones.
Return STRICT JSON only:
{{"top_match":{{"name":"...","search_name":"...","price":"₹X","match_percent":"X%","battery_spec":"...","display_spec":"...","processor_spec":"...","camera_spec":"..."}},"alternatives":[{{"name":"...","search_name":"...","price":"₹X","match_percent":"X%","battery_spec":"...","display_spec":"...","processor_spec":"...","camera_spec":"..."}},{{"name":"...","search_name":"...","price":"₹X","match_percent":"X%","battery_spec":"...","display_spec":"...","processor_spec":"...","camera_spec":"..."}}],"analysis":"..."}}"""
                response = client.models.generate_content(
                    model='gemini-2.5-flash', contents=prompt,
                    config=types.GenerateContentConfig(tools=[{"google_search": {}}], temperature=0.2)
                )
                clean_text  = response.text.replace("```json","").replace("```","").strip()
                result_json = json.loads(re.search(r'\{.*\}', clean_text, re.DOTALL).group(0))
            except Exception as e:
                print(f"Gemini error: {e}")
                result_json = get_offline_recommendation(budget_num)

        if 'top_match' in result_json:
            top_search = result_json['top_match'].get('search_name', result_json['top_match'].get('name','Phone'))
            result_json['top_match']['image_url']  = fetch_dynamic_image(top_search)
            result_json['top_match']['id']         = save_product_if_not_exists(result_json['top_match'])
            safe_b = urllib.parse.quote(top_search.split()[0] if top_search else "Phone")
            result_json['top_match']['image_urls'] = [
                result_json['top_match']['image_url'],
                f"https://ui-avatars.com/api/?name={safe_b}&background=F4FAFF&color=2962FF&size=512&font-size=0.3"
            ]

        if 'alternatives' in result_json:
            for alt in result_json['alternatives']:
                alt_s            = alt.get('search_name', alt.get('name',''))
                alt['image_url'] = fetch_dynamic_image(alt_s)
                alt['id']        = save_product_if_not_exists(alt)

        try:
            db.session.add(AiSearchLog(query=f"Budget:{budget},Brand:{brand},Usage:{usage},Storage:{storage}"))
            db.session.commit()
        except: pass

        return jsonify({"status": "success", "data": result_json}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/products', methods=['GET'])
def all_products():
    try:
        products = Product.query.order_by(Product.id.desc()).limit(50).all()
        return jsonify({"status": "success", "products": [
            {"id": p.id, "name": p.name, "price": p.price, "image_url": p.image_url} for p in products
        ]}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/product_specs', methods=['GET'])
def get_product_specs():
    try:
        name = request.args.get('name')
        if not name:
            return jsonify({"status": "error", "message": "Name required"}), 400
        
        p = Product.query.filter(Product.name.ilike(f"%{name}%")).first()
        if p:
            return jsonify({
                "status": "success",
                "battery_spec": p.battery_spec or "Standard Battery",
                "display_spec": p.display_spec or "Standard Display",
                "processor_spec": p.processor_spec or "Standard Processor",
                "camera_spec": p.camera_spec or "Standard Camera"
            }), 200
        return jsonify({"status": "error", "message": "Product not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# 4. ADDRESSES
# ==========================================
@app.route('/add_address', methods=['POST'])
@jwt_required()
def add_address():
    try:
        user_id  = get_jwt_identity()
        data     = request.get_json()
        existing = Address.query.filter_by(user_id=user_id).first()
        new_addr = Address(
            user_id=user_id, full_name=data.get('full_name'),
            mobile=str(data.get('mobile','')), pincode=str(data.get('pincode','')),
            city=data.get('city'), address_line=data.get('address_line'),
            is_default=True if not existing else False
        )
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
        addrs   = Address.query.filter_by(user_id=user_id).all()
        return jsonify({"status": "success", "addresses": [{
            "id": a.id, "full_name": a.full_name, "mobile": str(a.mobile),
            "pincode": str(a.pincode), "city": a.city,
            "address_line": a.address_line, "is_default": bool(a.is_default)
        } for a in addrs]}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/update_address/<int:id>', methods=['PUT'])
@jwt_required()
def update_address(id):
    try:
        user_id = get_jwt_identity()
        data    = request.get_json()
        address = Address.query.filter_by(id=id, user_id=user_id).first()
        if not address: return jsonify({"status":"error", "message":"Address not found"}), 404
        address.full_name    = data.get('full_name',    address.full_name)
        address.mobile       = str(data.get('mobile',   address.mobile))
        address.pincode      = str(data.get('pincode',  address.pincode))
        address.city         = data.get('city',         address.city)
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
# 5. PAYMENT METHODS
# ==========================================
@app.route('/payment_methods', methods=['GET'])
@jwt_required()
def get_payment_methods():
    try:
        user_id = get_jwt_identity()
        methods = SavedPaymentMethod.query.filter_by(user_id=user_id).all()
        return jsonify({"status": "success", "methods": [
            {"id": m.id, "method_type": m.method_type, "details": m.details,
             "expiry": m.expiry, "is_primary": bool(m.is_primary)} for m in methods
        ]}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/add_payment_method', methods=['POST'])
@jwt_required()
def add_payment_method():
    try:
        user_id    = get_jwt_identity()
        data       = request.get_json()
        new_method = SavedPaymentMethod(
            user_id=user_id, method_type=data.get('method_type'),
            details=data.get('details'), expiry=data.get('expiry'),
            is_primary=bool(data.get('is_primary', False))
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
        method  = SavedPaymentMethod.query.filter_by(id=id, user_id=user_id).first()
        if method:
            db.session.delete(method)
            db.session.commit()
            return jsonify({"status": "success", "message": "Removed successfully"}), 200
        return jsonify({"status": "error", "message": "Not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# 6. FCM TOKENS
# ==========================================
@app.route('/update_fcm_token', methods=['POST'])
@jwt_required()
def update_fcm_token():
    try:
        user_id  = get_jwt_identity()
        data     = request.get_json()
        token    = data.get('fcm_token') or data.get('token')
        platform = data.get('platform', 'android').lower()
        user     = db.session.get(User, user_id)
        if user and token:
            if platform == 'web': user.fcm_token_web     = token
            else:                 user.fcm_token_android = token
            db.session.commit()
            return jsonify({"status": "success", "message": f"{platform.title()} FCM Token updated"}), 200
        return jsonify({"status": "error", "message": "Invalid token"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# APP RUNNER
# ==========================================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)