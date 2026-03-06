# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the database object
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    mobile = db.Column(db.String(15))
    password = db.Column(db.String(200))
    reg_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_blocked = db.Column(db.Boolean, default=False)
    fcm_token = db.Column(db.String(255), nullable=True)
    
    # OTP Columns for Password Reset
    reset_otp = db.Column(db.String(10), nullable=True)
    otp_expiry = db.Column(db.DateTime, nullable=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    price = db.Column(db.String(50))
    image_url = db.Column(db.Text)
    battery_spec = db.Column(db.String(100))
    display_spec = db.Column(db.String(100))
    processor_spec = db.Column(db.String(100))
    camera_spec = db.Column(db.String(100))
    stock = db.Column(db.Integer, default=50)
    category = db.Column(db.String(100), default="Electronics")

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="Order Placed")
    invoice_no = db.Column(db.String(20), unique=True, nullable=True)
    payment_method = db.Column(db.String(50), default="Cash On Delivery")

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    address_line = db.Column(db.String(500), nullable=False)
    is_default = db.Column(db.Boolean, default=False)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    payment_method = db.Column(db.String(50))
    amount = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100), unique=True)
    
    # Razorpay tracking columns
    razorpay_order_id = db.Column(db.String(100), nullable=True)
    razorpay_signature = db.Column(db.String(255), nullable=True)
    
    status = db.Column(db.String(50), default="Completed")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SavedPaymentMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    method_type = db.Column(db.String(50), nullable=False)
    details = db.Column(db.String(255), nullable=False)
    expiry = db.Column(db.String(10), nullable=True)
    is_primary = db.Column(db.Boolean, default=False)

class NotificationPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    order_updates = db.Column(db.Boolean, default=True)
    warranty_alerts = db.Column(db.Boolean, default=True)
    ai_updates = db.Column(db.Boolean, default=True)
    promotions = db.Column(db.Boolean, default=False)
    frequency = db.Column(db.String(50), default="Daily summary")

class PrivacySetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    two_factor_auth = db.Column(db.Boolean, default=False)
    biometric_login = db.Column(db.Boolean, default=False)
    data_sharing = db.Column(db.Boolean, default=True)
    profile_visibility = db.Column(db.String(50), default="Public")

class Warranty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    device_name = db.Column(db.String(100), nullable=False)
    device_type = db.Column(db.String(50), nullable=True)
    purchase_date = db.Column(db.Date, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="Secure")
    invoice_url = db.Column(db.String(255), nullable=True)
    claim_issue_type = db.Column(db.String(100), nullable=True)
    claim_description = db.Column(db.Text, nullable=True)
    claim_invoice_url = db.Column(db.String(255), nullable=True)
    claim_device_url = db.Column(db.String(255), nullable=True)
    service_mode = db.Column(db.String(100), nullable=True)

class AiSearchLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=True)
    preferences = db.Column(db.String(255), nullable=True)
    recommended_product = db.Column(db.String(255), nullable=True)
    match_percent = db.Column(db.Integer, default=95)
    timestamp = db.Column(db.DateTime, default=db.func.now())

class AiSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_enabled = db.Column(db.Boolean, default=True)
    gaming_weight = db.Column(db.Integer, default=85)
    camera_weight = db.Column(db.Integer, default=60)
    battery_weight = db.Column(db.Integer, default=45)
    budget_weight = db.Column(db.Integer, default=70)
    engine_mode = db.Column(db.String(50), default="Hybrid Mode")

class CompareDeviceCache(db.Model):
    __tablename__ = 'compare_device_cache'
    id = db.Column(db.Integer, primary_key=True)
    search_query = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100))
    price = db.Column(db.String(50))
    spec_score = db.Column(db.String(20))
    release_date = db.Column(db.String(50))
    processor = db.Column(db.String(100))
    cores = db.Column(db.String(100))
    ram = db.Column(db.String(50))
    disp_type = db.Column(db.String(100))
    disp_res = db.Column(db.String(100))
    disp_refresh = db.Column(db.String(50))
    disp_size = db.Column(db.String(50))
    cam_main = db.Column(db.String(100))
    cam_sec = db.Column(db.String(100))
    cam_tert = db.Column(db.String(100))
    cam_front = db.Column(db.String(100))
    bat_capacity = db.Column(db.String(50))
    bat_charging = db.Column(db.String(50))
    storage_internal = db.Column(db.String(50))
    storage_type = db.Column(db.String(50))
    pros = db.Column(db.Text) 
    cons = db.Column(db.Text)
    antutu_score = db.Column(db.String(50))
    battery_life = db.Column(db.String(50))
    expert_score = db.Column(db.String(50))
    image_url = db.Column(db.String(255))

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255))
    message = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)