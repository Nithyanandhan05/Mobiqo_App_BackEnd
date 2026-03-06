# warranty.py
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta, date
from werkzeug.utils import secure_filename
import os

from models import db, Warranty, Product, User

warranty_bp = Blueprint('warranty', __name__)

# ==========================================
# FIREBASE PUSH NOTIFICATION HELPER
# ==========================================
def send_push_notification(user_id, title, body):
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
# HELPER TO DYNAMICALLY OVERRIDE STATUS
# ==========================================
def get_dynamic_status(w):
    db_status = w.status or "Secure"
    if db_status in ["Pending", "Rejected"]:
        return db_status

    if w.expiry_date:
        today = datetime.now().date()
        safe_expiry = w.expiry_date
        
        if isinstance(safe_expiry, datetime):
            safe_expiry = safe_expiry.date()
        elif isinstance(safe_expiry, str):
            # FIXED: Robust parsing for both "YYYY-MM-DD" and "Mar 06, 2026"
            try: safe_expiry = datetime.strptime(safe_expiry.split()[0], "%Y-%m-%d").date()
            except: 
                try: safe_expiry = datetime.strptime(safe_expiry, "%b %d, %Y").date()
                except: pass

        if isinstance(safe_expiry, date):
            days = (safe_expiry - today).days
            if days < 0:
                return "Expired"
            elif days <= 30:
                return "Alert"
    return "Secure"

# ==========================================
# 1. GET ALL USER WARRANTIES
# ==========================================
@warranty_bp.route('/my_warranties', methods=['GET'])
@warranty_bp.route('/api/my_warranties', methods=['GET'])
@jwt_required()
def get_my_warranties():
    try:
        user_id = get_jwt_identity()
        warranties = Warranty.query.filter_by(user_id=user_id).order_by(Warranty.id.desc()).all()
        
        device_list = []
        for w in warranties:
            expiry_str = w.expiry_date.strftime("%b %d, %Y") if hasattr(w.expiry_date, 'strftime') else str(w.expiry_date)
            device_list.append({
                "id": w.id,
                "name": w.device_name,
                "status": get_dynamic_status(w),
                "expiry": expiry_str
            })
            
        return jsonify({
            "status": "success",
            "devices": device_list,
            "ai_recommendation": {
                "message": "Your devices are protected! Extend your warranty before it expires to maintain full coverage."
            }
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# 2. GET ALERTS
# ==========================================
@warranty_bp.route('/alerts', methods=['GET'])
@warranty_bp.route('/api/alerts', methods=['GET'])
@jwt_required()
def get_alerts():
    try:
        user_id = get_jwt_identity()
        warranties = Warranty.query.filter_by(user_id=user_id).order_by(Warranty.id.desc()).all()

        device_list = []
        for w in warranties:
            expiry_str = w.expiry_date.strftime("%b %d, %Y") if hasattr(w.expiry_date, 'strftime') else str(w.expiry_date)
            device_list.append({
                "id": w.id,
                "name": w.device_name,
                "status": get_dynamic_status(w),
                "expiry": expiry_str
            })

        return jsonify({
            "status": "success",
            "devices": device_list
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# 3. GET SPECIFIC WARRANTY DETAILS
# ==========================================
@warranty_bp.route('/warranties/<int:id>', methods=['GET'])
@warranty_bp.route('/api/warranties/<int:id>', methods=['GET'])
@jwt_required()
def get_warranty_detail(id):
    try:
        user_id = get_jwt_identity()
        w = Warranty.query.filter_by(id=id, user_id=user_id).first()
        if not w: return jsonify({"status": "error", "message": "Warranty not found"}), 404
            
        purchase_str = w.purchase_date.strftime("%b %d, %Y") if hasattr(w.purchase_date, 'strftime') else "N/A"
        expiry_str = w.expiry_date.strftime("%b %d, %Y") if hasattr(w.expiry_date, 'strftime') else "N/A"
        
        months_left = "Expired"
        progress = 0.0
        
        if w.expiry_date:
            today = datetime.now().date()
            safe_expiry = w.expiry_date
            
            if isinstance(safe_expiry, datetime): safe_expiry = safe_expiry.date()
            elif isinstance(safe_expiry, str):
                try: safe_expiry = datetime.strptime(safe_expiry.split()[0], "%Y-%m-%d").date()
                except: 
                    try: safe_expiry = datetime.strptime(safe_expiry, "%b %d, %Y").date()
                    except: pass

            if isinstance(safe_expiry, date):
                days = (safe_expiry - today).days
                
                if days < 0:
                    months_left = "Expired"
                    progress = 0.0
                elif days == 0:
                    months_left = "Expiring Today"
                    progress = 0.02
                elif days == 1:
                    months_left = "Expiring Tomorrow"
                    progress = 0.05
                elif days < 30:
                    months_left = f"{days} Days Left"
                    progress = max(0.1, days / 365.0)
                else:
                    months = days // 30
                    months_left = f"{months} Month{'s' if months > 1 else ''} Left"
                    progress = min(1.0, days / 365.0)

        invoice_name = "Invoice_Document.pdf"
        if w.invoice_url: invoice_name = w.invoice_url.split('/')[-1]

        data = {
            "id": w.id, "device_name": w.device_name, "device_type": w.device_type or "Smartphone",
            "purchase_date": purchase_str, "expiry_date": expiry_str, "status": get_dynamic_status(w),
            "progress": progress, "months_left": months_left, "invoice_name": invoice_name,
            "history": [
                {"title": "Warranty Registered", "date": purchase_str, "desc": "Your warranty was successfully registered.", "is_last": False},
                {"title": "Coverage Active", "date": purchase_str, "desc": "Your device is fully covered.", "is_last": True}
            ]
        }
        
        if w.status in ["Pending", "Rejected"]:
            data["history"][1]["is_last"] = False 
            data["history"].append({
                "title": "Claim Submitted",
                "date": datetime.now().strftime("%b %d, %Y"),
                "desc": f"Claim issue: {w.claim_issue_type}. Status: {w.status}",
                "is_last": True
            })
        
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# 4. ADD NEW WARRANTY DEVICE
# ==========================================
@warranty_bp.route('/warranties/add', methods=['POST'])
@warranty_bp.route('/api/warranties/add', methods=['POST'])
@jwt_required()
def add_warranty():
    try:
        user_id = get_jwt_identity()
        data = request.get_json(silent=True) or {}
        
        expiry_str = data.get('expiry_date')
        if expiry_str: expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
        else: expiry_date = (datetime.now() + timedelta(days=365)).date()
            
        purchase_date = datetime.now().date()
        
        new_warranty = Warranty(
            user_id=user_id, device_name=data.get('device_name', 'Unknown Device'),
            device_type=data.get('brand', 'Smartphone'), purchase_date=purchase_date,
            expiry_date=expiry_date, status="Pending", 
            claim_issue_type="New Registration", 
            claim_description="Please verify the invoice and approve this new device warranty."
        )
        db.session.add(new_warranty)
        db.session.commit()

        send_push_notification(
            user_id, 
            "Warranty Registered 📱", 
            f"Your warranty for {new_warranty.device_name} has been submitted for approval."
        )

        return jsonify({"status": "success", "message": "Sent for Approval!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# 5. EXTEND WARRANTY
# ==========================================
@warranty_bp.route('/warranties/<int:id>/extend', methods=['POST'])
@warranty_bp.route('/api/warranties/<int:id>/extend', methods=['POST'])
@jwt_required()
def extend_warranty(id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json(silent=True) or {}
        
        duration_months = int(data.get('duration_months', 12))
        warranty = Warranty.query.filter_by(id=id, user_id=user_id).first()
        if not warranty: return jsonify({"status": "error", "message": "Warranty not found"}), 404

        extra_days = duration_months * 30
        
        if warranty.expiry_date:
            safe_expiry = warranty.expiry_date if isinstance(warranty.expiry_date, datetime) else datetime.combine(warranty.expiry_date, datetime.min.time())
            warranty.expiry_date = safe_expiry + timedelta(days=extra_days)
            if warranty.status in ["Expired", "Alert"]: warranty.status = "Secure"

        db.session.commit()
        
        final_date = warranty.expiry_date.strftime("%b %d, %Y") if hasattr(warranty.expiry_date, 'strftime') else "N/A"

        send_push_notification(
            user_id, 
            "Warranty Extended 🛡️", 
            f"Success! Your {warranty.device_name} warranty is now covered until {final_date}."
        )

        return jsonify({"status": "success", "message": f"Warranty extended!", "new_expiry": final_date}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# 6. CLAIM WARRANTY
# ==========================================
@warranty_bp.route('/warranties/<int:id>/claim', methods=['POST'])
@warranty_bp.route('/api/warranties/<int:id>/claim', methods=['POST'])
@jwt_required()
def claim_warranty(id):
    try:
        user_id = get_jwt_identity()
        warranty = Warranty.query.filter_by(id=id, user_id=user_id).first()
        if not warranty: return jsonify({"status": "error", "message": "Warranty not found"}), 404
            
        issue_type = request.form.get('issue_type', 'Others')
        description = request.form.get('description', '')
        service_mode = request.form.get('service_mode', 'center')
        
        warranty.status = "Pending"
        warranty.claim_issue_type = f"{issue_type} ({service_mode})"
        warranty.claim_description = description
        
        if 'invoice_image' in request.files:
            file = request.files['invoice_image']
            filename = secure_filename(f"claim_{id}_invoice_{file.filename}")
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            warranty.claim_invoice_url = f"/static/uploads/{filename}"

        if 'device_image' in request.files:
            file = request.files['device_image']
            filename = secure_filename(f"claim_{id}_device_{file.filename}")
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            warranty.claim_device_url = f"/static/uploads/{filename}"

        db.session.commit()

        send_push_notification(
            user_id, 
            "Claim Submitted 📝", 
            f"Your claim for {warranty.device_name} ({issue_type}) is under review."
        )

        return jsonify({"status": "success", "message": "Claim submitted successfully. Our team will review it."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500