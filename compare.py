# compare.py
from flask import Blueprint, request, jsonify
from google import genai
from google.genai import types
import requests
import os
import json
import re

# --- IMPORT THE NEW IMAGE FETCHER ---
from image_fetcher import fetch_dynamic_image
from models import db, Product, CompareDeviceCache

compare_bp = Blueprint('compare', __name__)

# Initialize AI client
os.environ["GOOGLE_API_KEY"] = "AIzaSyDvZKjR23wPKymFekXR2ZAhc0fZT8hp2XM" 
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

# ==========================================
# CACHE CONVERSION HELPERS
# ==========================================
def cache_to_dict(cache_obj):
    return {
        "id": cache_obj.id, # Added ID mapping
        "name": cache_obj.name,
        "price": cache_obj.price,
        "spec_score": cache_obj.spec_score,
        "release_date": cache_obj.release_date,
        "performance": {"processor": cache_obj.processor, "cores": cache_obj.cores, "ram": cache_obj.ram},
        "display": {"type": cache_obj.disp_type, "resolution": cache_obj.disp_res, "refresh_rate": cache_obj.disp_refresh, "size": cache_obj.disp_size},
        "camera": {"rear_main": cache_obj.cam_main, "rear_secondary": cache_obj.cam_sec, "rear_tertiary": cache_obj.cam_tert, "front": cache_obj.cam_front},
        "battery": {"capacity": cache_obj.bat_capacity, "charging": cache_obj.bat_charging},
        "storage": {"internal": cache_obj.storage_internal, "type": cache_obj.storage_type},
        "pros": json.loads(cache_obj.pros) if cache_obj.pros else [],
        "cons": json.loads(cache_obj.cons) if cache_obj.cons else [],
        "antutu_score": cache_obj.antutu_score or "N/A",
        "battery_life": cache_obj.battery_life or "N/A",
        "expert_score": cache_obj.expert_score or "N/A",
        "image_url": cache_obj.image_url
    }

def dict_to_cache(query, data):
    return CompareDeviceCache(
        search_query=query,
        name=data.get("name", "Unknown"),
        price=data.get("price", "₹30,000"),
        spec_score=data.get("spec_score", "85/100"),
        release_date=data.get("release_date", "2023"),
        processor=data.get("performance", {}).get("processor", ""),
        cores=data.get("performance", {}).get("cores", ""),
        ram=data.get("performance", {}).get("ram", ""),
        disp_type=data.get("display", {}).get("type", ""),
        disp_res=data.get("display", {}).get("resolution", ""),
        disp_refresh=data.get("display", {}).get("refresh_rate", ""),
        disp_size=data.get("display", {}).get("size", ""),
        cam_main=data.get("camera", {}).get("rear_main", ""),
        cam_sec=data.get("camera", {}).get("rear_secondary", ""),
        cam_tert=data.get("camera", {}).get("rear_tertiary", ""),
        cam_front=data.get("camera", {}).get("front", ""),
        bat_capacity=data.get("battery", {}).get("capacity", ""),
        bat_charging=data.get("battery", {}).get("charging", ""),
        storage_internal=data.get("storage", {}).get("internal", ""),
        storage_type=data.get("storage", {}).get("type", ""),
        pros=json.dumps(data.get("pros", [])),
        cons=json.dumps(data.get("cons", [])),
        antutu_score=data.get("antutu_score", "N/A"),
        battery_life=data.get("battery_life", "N/A"),
        expert_score=data.get("expert_score", "N/A"),
        image_url=data.get("image_url", fetch_dynamic_image(data.get("name", "")))
    )

def save_or_update_product(phone_data):
    if not phone_data or 'name' not in phone_data:
        return -1
    
    raw_price = str(phone_data.get('price', '0')).replace('₹', '').replace(',', '').strip()
    try: numeric_price = float(raw_price)
    except: numeric_price = 0.0

    battery_val = phone_data.get('battery', {}).get('capacity', 'Standard')
    display_val = phone_data.get('display', {}).get('type', 'Standard')
    processor_val = phone_data.get('performance', {}).get('processor', 'Standard')
    camera_val = phone_data.get('camera', {}).get('rear_main', 'Standard')

    product = Product.query.filter_by(name=phone_data['name']).first()
    if not product:
        product = Product(
            name=phone_data['name'], 
            price=numeric_price,
            image_url=phone_data.get('image_url', ''), 
            battery_spec=battery_val,
            display_spec=display_val, 
            processor_spec=processor_val,
            camera_spec=camera_val
        )
        db.session.add(product)
    else:
        product.price = numeric_price
        product.battery_spec = battery_val
        product.display_spec = display_val
        product.processor_spec = processor_val
        product.camera_spec = camera_val

    db.session.commit()
    return product.id

# ==========================================
# 1. INSTANT INTERNET SEARCH
# ==========================================
@compare_bp.route('/search_devices', methods=['GET'])
def search_devices():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({"status": "success", "results": []}), 200

    try:
        # FIXED: Allow 'a' to pull actual trending phones instead of returning empty
        if query.lower() == 'a':
            search_url = "https://duckduckgo.com/ac/?q=top+flagship+smartphone"
        else:
            search_url = f"https://duckduckgo.com/ac/?q={query}+smartphone"
            
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers)
        suggestions = response.json()

        results = []
        banned_words = ['case', 'cover', 'price', 'review', 'vs']
        
        for item in suggestions:
            phrase = item['phrase'].replace(' smartphone', '').title()
            if any(b in phrase.lower() for b in banned_words):
                continue
                
            image_url = fetch_dynamic_image(phrase)

            product = Product.query.filter_by(name=phrase).first()
            if not product:
                product = Product(
                    name=phrase, price=0.0, image_url=image_url,
                    battery_spec="Standard", display_spec="Standard",
                    processor_spec="Standard", camera_spec="Standard"
                )
                db.session.add(product)
                db.session.commit()

            results.append({
                "id": product.id,
                "name": phrase,
                "price": "Compare to reveal",
                "match_percent": "Live Web",
                "specs": "Internet Data Source",
                "category": "Web Search",
                "image_url": image_url
            })
            
            if len(results) >= 5: break

        return jsonify({"status": "success", "results": results}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": "Failed to search devices"}), 500

# ==========================================
# 2. AI LIVE-WEB FETCH (INDIVIDUAL)
# ==========================================
def fetch_single_device_from_ai(device_name):
    prompt = f"""
    Search the internet for the exact specifications of the smartphone: "{device_name}".
    CRITICAL RULES:
    1. "price" MUST be the CURRENT Indian Rupee market price on Amazon/Flipkart (e.g. "₹74,999"). Do NOT use the old launch price. If the phone is on sale, give the sale price. Do NOT put "0", "₹0", or "N/A"
    2. Provide exactly 3 "pros" and 3 "cons".
    Return STRICT JSON exactly matching this structure:
    {{
        "name": "Exact Name",
        "price": "₹XX,XXX",
        "spec_score": "92/100",
        "release_date": "Month Year",
        "performance": {{"processor": "...", "cores": "...", "ram": "..."}},
        "display": {{"type": "...", "resolution": "...", "refresh_rate": "...", "size": "..."}},
        "camera": {{"rear_main": "...", "rear_secondary": "...", "rear_tertiary": "...", "front": "..."}},
        "battery": {{"capacity": "...", "charging": "..."}},
        "storage": {{"internal": "...", "type": "..."}},
        "pros": ["Pro 1", "Pro 2", "Pro 3"],
        "cons": ["Con 1", "Con 2", "Con 3"],
        "antutu_score": "...",
        "battery_life": "...",
        "expert_score": ".../5"
    }}
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
    device_data = json.loads(re.search(r'\{.*\}', clean_text, re.DOTALL).group(0))
    
    if device_data.get('price') in ["0", "₹0", "₹0.00", "N/A"]:
        device_data['price'] = "₹24,999" 

    device_data['image_url'] = fetch_dynamic_image(device_data.get('name', device_name))
    return device_data

# ==========================================
# 3. COMPARE & CACHE ROUTE
# ==========================================
@compare_bp.route('/compare_devices', methods=['POST'])
def compare_devices():
    try:
        data = request.get_json()
        dev1_query = data.get('device1', 'Device 1').strip().lower()
        dev2_query = data.get('device2', 'Device 2').strip().lower()

        d1_cache = CompareDeviceCache.query.filter_by(search_query=dev1_query).first()
        if d1_cache:
            device1_data = cache_to_dict(d1_cache)
        else:
            device1_data = fetch_single_device_from_ai(dev1_query)
            db.session.add(dict_to_cache(dev1_query, device1_data))

        d2_cache = CompareDeviceCache.query.filter_by(search_query=dev2_query).first()
        if d2_cache:
            device2_data = cache_to_dict(d2_cache)
        else:
            device2_data = fetch_single_device_from_ai(dev2_query)
            db.session.add(dict_to_cache(dev2_query, device2_data))

        db.session.commit()

        # Update the Product Inventory & Get Real IDs
        device1_data['id'] = save_or_update_product(device1_data)
        device2_data['id'] = save_or_update_product(device2_data)

        name1 = device1_data.get('name', 'Device 1')
        name2 = device2_data.get('name', 'Device 2')
        analysis = f"Comparing the {name1} and {name2}. Both offer competitive specifications. Review the detailed breakdown above to see which best matches your specific needs."

        return jsonify({
            "status": "success",
            "data": {
                "device1": device1_data,
                "device2": device2_data,
                "ai_analysis": analysis
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"AI Compare Error: {e}")
        return jsonify({"status": "error", "message": "Failed to generate comparison"}), 500