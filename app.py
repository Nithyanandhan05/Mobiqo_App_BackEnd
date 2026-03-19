# app.py
import os
from dotenv import load_dotenv
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets

# --- LOAD ENV VARS FIRST BEFORE IMPORTING BLUEPRINTS ---
# This safely loads your hidden keys from the .env file
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

from models import db, User, Product, Order, Address, SavedPaymentMethod, NotificationPreference, PrivacySetting, AiSearchLog, AiSetting, Warranty
from payment import payment_bp
from warranty import warranty_bp
from orders import orders_bp
from compare import compare_bp
from admin import admin_bp 
from scanner import scanner_bp
from utils import send_universal_push_notification

# --- LOAD SMARTPHONE DATASET ---
try:
    phone_df = pd.read_csv("smartphones_dataset.csv")
    print(f"✅ Smartphone dataset loaded! Total phones: {len(phone_df)}")
except Exception as e:
    phone_df = None
    print(f"⚠️ Could not load smartphone dataset: {e}")
try:
    phone_model     = joblib.load('phone_model.pkl')
    enc_brand       = joblib.load('encoder_brand.pkl')
    enc_bestfor     = joblib.load('encoder_bestfor.pkl')
    enc_5g          = joblib.load('encoder_5g.pkl')
    print("✅ Local AI Model loaded! No API key needed.")
except Exception as e:
    phone_model = None
    print(f"⚠️ Local AI model not found: {e} — Will use Gemini API as backup.")
    
app = Flask(__name__)
CORS(app)

# --- CONFIGURATION (SECURELY HIDDEN) ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/smartelectro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "smart-electro-ai-super-secure-secret-key-2026")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "smart-electro-ai-super-secure-jwt-key-2026")
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

# --- AI SETUP (SECURELY HIDDEN) ---
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
# REAL EMAIL CONFIGURATION & OTP STORE (SECURELY HIDDEN)
# ==========================================
registration_otps = {} 
SENDER_EMAIL = os.getenv("EMAIL_USER", "mobiqoapp@gmail.com")  
SENDER_PASSWORD = os.getenv("EMAIL_PASS", "") 

def send_real_email(receiver_email, otp):
    if not SENDER_PASSWORD:
        print("❌ Email failed: No password provided in .env")
        return False
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
        
        if not email: return jsonify({"status": "error", "message": "Email is required"}), 400
        if User.query.filter_by(email=email).first(): return jsonify({"status": "error", "message": "Email already exists"}), 400
            
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
        if registration_otps.get(email) == otp: return jsonify({"status": "success", "message": "Verified"}), 200
        return jsonify({"status": "error", "message": "Invalid OTP"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

password_reset_tokens = {} 
password_reset_otps = {}

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        if not email: return jsonify({"status": "error", "message": "Email required"}), 400
        user = User.query.filter_by(email=email).first()
        if not user: return jsonify({"status": "error", "message": "No account found"}), 404
            
        otp = str(random.randint(100000, 999999))
        password_reset_otps[email] = otp
        if send_real_email(email, otp): return jsonify({"status": "success", "message": "OTP sent"}), 200
        return jsonify({"status": "error", "message": "Email failed."}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/reset_password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        otp = data.get('otp', '').strip()
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
    if not SENDER_PASSWORD: return False
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
        admin = db.session.get(User, admin_id)
        if not admin or admin.email != 'admin@gmail.com': return jsonify({"status": "error", "message": "Unauthorized"}), 403
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        user = User.query.filter_by(email=email).first()
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
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        token = data.get('token', '').strip()
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

def save_product_if_not_exists(phone_data):
    if not phone_data or 'name' not in phone_data: return None
    product = Product.query.filter_by(name=phone_data['name']).first()
    if not product:
        raw_price = str(phone_data.get('price', '0')).replace('₹', '').replace(',', '').strip()
        try: numeric_price = float(raw_price)
        except: numeric_price = 0.0

        product = Product(
            name=phone_data['name'], price=numeric_price, image_url=phone_data.get('image_url', ''), 
            battery_spec=phone_data.get('battery_spec', 'Standard'), display_spec=phone_data.get('display_spec', 'Standard'), 
            processor_spec=phone_data.get('processor_spec', 'Standard'), camera_spec=phone_data.get('camera_spec', 'Standard')
        )
        db.session.add(product)
        db.session.commit()
    return product.id

def get_offline_recommendation(budget):
    return {
        "top_match": { "name": "Samsung Galaxy S23 FE (8GB RAM, 128GB)", "search_name": "Samsung Galaxy S23 FE", "price": f"₹{budget}", "match_percent": "95%", "battery_spec": "4500mAh", "display_spec": "120Hz Dynamic AMOLED", "processor_spec": "Exynos 2200", "camera_spec": "50MP OIS Triple Camera" },
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
        if User.query.filter_by(email=clean_email).first(): return jsonify({"status":"error", "message": "Email exists"}), 400
        hashed = bcrypt.generate_password_hash(data.get('password', '').strip()).decode('utf-8')
        new_user = User(full_name=data.get('full_name', '').strip(), email=clean_email, mobile=data.get('mobile', '').strip(), password=hashed)
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
        data = request.get_json()
        clean_email = data.get('email', '').strip().lower()
        user = User.query.filter_by(email=clean_email).first()
        if user and bcrypt.check_password_hash(user.password, data.get('password', '').strip()):
            return jsonify({
                "status": "success", "token": create_access_token(identity=str(user.id)),
                "user_name": user.full_name, "is_admin": user.email == 'admin@gmail.com'
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
        user = User.query.get(user_id)
        if not bcrypt.check_password_hash(user.password, data.get('current_password', '').strip()): return jsonify({"status": "error", "message": "Incorrect password"}), 401
        user.password = bcrypt.generate_password_hash(data.get('new_password', '').strip()).decode('utf-8')
        db.session.commit()
        return jsonify({"status": "success", "message": "Password updated"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/auth/logout-all', methods=['POST'])
@jwt_required()
def logout_all(): return jsonify({"status": "success", "message": "Logged out."}), 200

# ==========================================
# 2. PROFILE & SETTINGS
# ==========================================
@app.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if not user: return jsonify({"status": "error", "message": "Not found"}), 404
        profile_data = {
            "full_name": user.full_name, "email": user.email, "mobile": user.mobile,
            "total_orders": Order.query.filter_by(user_id=user_id).count(), 
            "saved_addresses": Address.query.filter_by(user_id=user_id).count(),
            "active_warranties": 3, "ai_searches": 42
        }
        return jsonify({"status": "success", "profile": profile_data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def build_detailed_analysis(top, budget_num, usage, brand, storage, battery, notes):
    name        = f"{top['brand']} {top['model']}"
    price       = int(top['price'])
    ram         = int(top['ram'])
    stor        = int(top['storage'])
    bat         = int(top['battery'])
    cam         = int(top['camera_mp'])
    processor   = str(top['processor'])
    rating      = float(top['rating'])
    best_for    = str(top['best_for'])
    has_5g      = str(top.get('5g_support', 'No'))
    display     = float(top.get('display_inches', 6.5))
    savings     = budget_num - price
    
    usage_lower = str(usage).lower()
    usage_praise = {
        'gaming':   f"For gaming, the {processor} chipset ensures smooth frame rates with minimal lag, and {ram}GB RAM means you can run multiple apps and games without slowdowns.",
        'camera':   f"For photography, the {cam}MP main camera captures sharp, detailed shots in all lighting conditions.",
        'battery':  f"Built for all-day use, the massive {bat}mAh battery will easily last through a full day of heavy usage without needing a top-up.",
        'business': f"For business use, the {ram}GB RAM handles multitasking effortlessly.",
        'student':  f"Perfect for students — the large {display}\" display is great for reading and note-taking.",
        'media':    f"The large {display}\" display paired with the powerful {processor} makes this an excellent choice for streaming videos and social media.",
    }
    usage_text = usage_praise.get(usage_lower, f"As a general-purpose phone, it handles everyday tasks smoothly thanks to {ram}GB RAM and the {processor}.")
    value_text = f"At ₹{price:,}, it fits perfectly within your ₹{budget_num:,} budget." if savings >= 0 else f"At ₹{price:,}, it's a strong flagship choice that justifies the price."
    connectivity = "It also supports 5G connectivity." if has_5g == 'Yes' else "It connects reliably on 4G LTE networks."
    storage_text = f"With {stor}GB of onboard storage, you'll have plenty of room."
    rating_text = f"Rated ⭐{rating}/5 by users."
    
    return f"Based on your budget of ₹{budget_num:,}, our AI recommends the {name} as the best match. {usage_text} The {cam}MP camera system captures stunning photos, while the {bat}mAh battery ensures you stay powered. {storage_text} {connectivity} {value_text} {rating_text}"

# ==========================================
# 3. AI RECOMMENDATION ENGINE (MULTI-BRAND SUPPORT)
# ==========================================
@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        budget  = data.get('budget', 30000)
        brand   = data.get('brand', 'Any')
        usage   = data.get('usage', 'General')
        storage = data.get('storage', '128GB')
        battery = data.get('battery', 'Standard')
        notes   = data.get('notes', '')
        wants_5g = '5g' in str(notes).lower() or '5g' in str(usage).lower()
 
        try: budget_num = int(float(str(budget).replace('₹', '').replace(',', '').strip()))
        except: budget_num = 30000
 
        try: storage_num = int(''.join(filter(str.isdigit, str(storage)))) or 128
        except: storage_num = 128

        def format_phone_name(row):
            brand_str = str(row['brand']).strip()
            model_str = str(row['model']).strip()
            base_name = model_str if model_str.lower().startswith(brand_str.lower()) else f"{brand_str} {model_str}"
            search_name_clean = base_name

            if str(row.get('5g_support', 'No')).lower() in ['yes', 'true', '1', 'y'] and '5g' not in base_name.lower():
                base_name += " 5G"

            try: ram_val = int(float(row.get('ram', 8)))
            except: ram_val = 8
            
            try: storage_val = int(float(row.get('storage', 128)))
            except: storage_val = 128

            return f"{base_name} ({ram_val}GB RAM, {storage_val}GB)", search_name_clean

        result_json = None
 
        if phone_model is not None and phone_df is not None:
            try:
                brands_list = []
                if brand and brand.lower() not in ['any', 'all', '']:
                    brands_list = [b.strip().lower() for b in str(brand).split(',')]
                    first_brand_for_ai = brands_list[0]
                    brand_enc = enc_brand.transform([first_brand_for_ai])[0] if first_brand_for_ai in enc_brand.classes_ else 0
                else:
                    brand_enc = 0
 
                five_g_enc = enc_5g.transform(['Yes' if wants_5g else 'No'])[0]
 
                model_input = pd.DataFrame([{
                    'price': budget_num, 'ram': 8, 'storage': storage_num,
                    'battery': 5000 if battery == 'Standard' else 6000,
                    'camera_mp': 50, '5g_encoded': five_g_enc, 'brand_encoded': brand_enc
                }])
 
                predicted_enc   = phone_model.predict(model_input)[0]
                predicted_usage = enc_bestfor.inverse_transform([predicted_enc])[0]
 
                filtered = phone_df[(phone_df['price'] >= budget_num * 0.7) & (phone_df['price'] <= budget_num * 1.1)].copy()
 
                if brands_list:
                    brand_match = filtered[filtered['brand'].str.lower().isin(brands_list)]
                    if not brand_match.empty: filtered = brand_match
                    else:
                        fallback_match = phone_df[phone_df['brand'].str.lower().isin(brands_list)].copy()
                        if not fallback_match.empty: filtered = fallback_match
 
                usage_match = filtered[filtered['best_for'].str.lower() == predicted_usage.lower()]
                if not usage_match.empty: filtered = usage_match
 
                filtered = filtered.drop_duplicates(subset=['brand', 'model']).sort_values('rating', ascending=False)
 
                if not filtered.empty:
                    top = filtered.iloc[0]
                    alts = filtered.iloc[1:3]
                    top_display_name, top_search_name = format_phone_name(top)
 
                    result_json = {
                        "top_match": {
                            "name": top_display_name, "search_name": top_search_name, "price": f"₹{int(top['price']):,}",
                            "match_percent": f"{int(top['rating'] * 20)}%", "battery_spec": f"{int(top['battery'])}mAh",
                            "display_spec": f"{top['display_inches']} inch Display", "processor_spec": str(top['processor']),
                            "camera_spec": f"{int(top['camera_mp'])}MP Camera"
                        },
                        "alternatives": [],
                        "analysis": build_detailed_analysis(top, budget_num, usage, brand, storage, battery, notes)
                    }
                    
                    for _, r in alts.iterrows():
                        alt_display_name, alt_search_name = format_phone_name(r)
                        result_json["alternatives"].append({
                            "name": alt_display_name, "search_name": alt_search_name,
                            "price": f"₹{int(r['price']):,}", "match_percent": f"{int(r['rating'] * 18)}%"
                        })
            except Exception as e:
                print(f"Local AI error: {e}")
                result_json = None
 
        if result_json is None:
            print("⚡ Falling back to Gemini API...")
            try:
                phone_context = ""
                if phone_df is not None:
                    filtered = phone_df[(phone_df['price'] >= budget_num * 0.7) & (phone_df['price'] <= budget_num * 1.1)].head(10)
                    if not filtered.empty:
                        phone_context = f"Here are phones from our database:\n{filtered[['brand','model','price','ram','storage','battery','camera_mp','processor','best_for','rating']].to_string(index=False)}"
 
                prompt = f"""
                You are a smartphone expert. Customer Requirements: Budget: ₹{budget_num}, Brand: {brand}, Usage: {usage}, Storage: {storage}.
                Return STRICT JSON ONLY representing top match and 2 alternatives.
                """
                response = client.models.generate_content(
                    model='gemini-2.5-flash', contents=prompt,
                    config=types.GenerateContentConfig(tools=[{"google_search": {}}], temperature=0.2)
                )
                clean_text = response.text.replace("```json", "").replace("```", "").strip()
                result_json = json.loads(re.search(r'\{.*\}', clean_text, re.DOTALL).group(0))
            except Exception as e:
                result_json = get_offline_recommendation(budget_num)
 
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
                alt_search = alt.get('search_name', alt.get('name', ''))
                alt['image_url'] = fetch_dynamic_image(alt_search)
                alt['id'] = save_product_if_not_exists(alt)
 
        try:
            db.session.add(AiSearchLog(query=f"Budget:{budget}, Brand:{brand}, Usage:{usage}, Storage:{storage}"))
            db.session.commit()
        except: pass
 
        return jsonify({"status": "success", "data": result_json}), 200
 
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/products', methods=['GET'])
def all_products():
    try:
        products = Product.query.order_by(Product.id.desc()).limit(10).all()
        return jsonify({"status": "success", "products": [{"id": p.id, "name": p.name, "price": p.price, "image_url": p.image_url} for p in products]}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# 4. ADDRESS ROUTES (CRASH FIX INCLUDED)
# ==========================================
@app.route('/add_address', methods=['POST'])
@jwt_required()
def add_address():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        existing = Address.query.filter_by(user_id=user_id).first()
        is_default = True if not existing else False
        new_addr = Address(
            user_id=user_id, 
            full_name=data.get('full_name'), 
            mobile=str(data.get('mobile', '')), 
            pincode=str(data.get('pincode', '')), 
            city=data.get('city'), 
            address_line=data.get('address_line'), 
            is_default=is_default
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
        addrs = Address.query.filter_by(user_id=user_id).all()
        res = [{
            "id": a.id, 
            "full_name": a.full_name, 
            "mobile": str(a.mobile), 
            "pincode": str(a.pincode), 
            "city": a.city, 
            "address_line": a.address_line, 
            "is_default": bool(a.is_default) 
        } for a in addrs]
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
        address.mobile = str(data.get('mobile', address.mobile))
        address.pincode = str(data.get('pincode', address.pincode))
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
        result = [{"id": m.id, "method_type": m.method_type, "details": m.details, "expiry": m.expiry, "is_primary": bool(m.is_primary)} for m in methods]
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
            details=data.get('details'), expiry=data.get('expiry'), is_primary=bool(data.get('is_primary', False))
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
# 6. FCM TOKENS
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
            if platform == 'web': user.fcm_token_web = token
            else: user.fcm_token_android = token
            db.session.commit()
            return jsonify({"status": "success", "message": f"{platform.title()} FCM Token updated"}), 200
        return jsonify({"status": "error", "message": "Invalid token"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# APP RUNNER
# ==========================================
if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)