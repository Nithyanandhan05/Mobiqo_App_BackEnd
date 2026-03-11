# scanner.py
from flask import Blueprint, request, jsonify
from google import genai
from google.genai import types
import os
import json
import re
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from image_fetcher import fetch_dynamic_image
from models import db, Product

scanner_bp = Blueprint('scanner', __name__)

# Initialize Gemini Client using the Dedicated Scanner Key
SCANNER_KEY = os.getenv("GEMINI_API_KEY_SCANNER")
client = genai.Client(api_key=SCANNER_KEY) if SCANNER_KEY else None

def safe_get_price(price_val):
    """Safely extracts a numeric price from any string format."""
    if not price_val:
        return 0.0
    try:
        if isinstance(price_val, (float, int)):
            return float(price_val)
        clean_price = str(price_val).replace('₹', '').replace(',', '').strip()
        return float(clean_price) if clean_price else 0.0
    except Exception:
        return 0.0

@scanner_bp.route('/api/scan_device', methods=['POST'])
def scan_device():
    try:
        if not client:
            return jsonify({"status": "error", "message": "Scanner API Key is missing. Check your .env file."}), 500

        if 'image' not in request.files:
            return jsonify({"status": "error", "message": "No image uploaded"}), 400
            
        file = request.files['image']
        img = Image.open(file.stream)
        
        # 1. SUPERCHARGED AI PROMPT FOR HIGH ACCURACY
        prompt = """
        You are an expert smartphone identifier. Analyze this image meticulously to determine the EXACT smartphone model.
        
        CRITICAL IDENTIFICATION RULES:
        1. Examine the camera module shape, number of lenses, and flash placement very closely.
        2. Look for any brand logos, text, or distinctive design patterns on the back panel.
        3. If the screen is visible and showing text (like an 'About Phone' screen or an e-commerce page), read the model name directly from the screen.
        4. Distinguish carefully between base, 'Lite', 'Pro', 'Plus', or 'Ultra' variants based on visual hardware cues (e.g., extra lenses usually mean Pro/Ultra).
        
        Once identified, use your Google Search tool to find its CURRENT active market price in India (in INR) and its exact key specifications.
        Do not use placeholder text. Be specific and accurate.
        
        Return STRICT JSON exactly matching this structure:
        {
            "name": "Official Full Name (e.g., OnePlus Nord CE 3 Lite 5G)",
            "price": "₹XX,XXX",
            "battery_spec": "e.g., 5000mAh, 67W Fast Charging",
            "display_spec": "e.g., 6.72 inch IPS LCD, 120Hz",
            "processor_spec": "e.g., Snapdragon 695 5G",
            "camera_spec": "e.g., 108MP Main, 2MP Macro",
            "category": "e.g., Mid-Range Smartphone"
        }
        If you are completely unsure or it's not a phone, return {"name": "Unknown Device", "price": "₹0"}
        """
        
        # Enable the Google Search tool during the vision analysis
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[img, prompt],
            config=types.GenerateContentConfig(
                tools=[{"google_search": {}}], 
                temperature=0.1 # Lowered temperature for less guessing, more precision
            )
        )
        
        # 2. Safely parse the JSON response
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        match = re.search(r'\{.*\}', clean_text, re.DOTALL)
        
        if not match:
            return jsonify({"status": "error", "message": "Could not identify phone from image"}), 404
            
        data = json.loads(match.group(0))
        phone_name = data.get("name", "Unknown Device")
        raw_price_str = data.get("price", "0")
        
        print(f"🤖 Scanner Identified: {phone_name} | Price: {raw_price_str}")
        
        if "Unknown Device" in phone_name or not phone_name:
            return jsonify({"status": "error", "message": "Could not identify phone. Please try scanning the back or 'About Phone' screen."}), 404

        num_price = safe_get_price(raw_price_str)
        battery_spec = data.get("battery_spec", "Standard Battery")
        display_spec = data.get("display_spec", "Standard Display")
        processor_spec = data.get("processor_spec", "Standard Processor")
        camera_spec = data.get("camera_spec", "Standard Camera")
        category_spec = data.get("category", "Smartphone")

        # 3. Save ALL REAL DETAILS in DB for future use
        product = Product.query.filter(Product.name.ilike(f"%{phone_name}%")).first()
        
        if not product:
            image_url = fetch_dynamic_image(phone_name)
            product = Product(
                name=phone_name, 
                price=num_price, 
                image_url=image_url,
                battery_spec=battery_spec, 
                display_spec=display_spec,
                processor_spec=processor_spec, 
                camera_spec=camera_spec,
                category=category_spec
            )
            db.session.add(product)
        else:
            # ---> NEW FIX: Fetch image if the existing database entry is missing it <---
            if not product.image_url or str(product.image_url).strip() == "":
                product.image_url = fetch_dynamic_image(phone_name)
                
            # Update the existing DB product with the fresh live specs and price
            if num_price > 0: product.price = num_price
            if battery_spec != "Standard Battery": product.battery_spec = battery_spec
            if display_spec != "Standard Display": product.display_spec = display_spec
            if processor_spec != "Standard Processor": product.processor_spec = processor_spec
            if camera_spec != "Standard Camera": product.camera_spec = camera_spec

        db.session.commit()
        final_price = safe_get_price(product.price)
            
        return jsonify({
            "status": "success",
            "message": "Device Identified",
            "device": {
                "id": product.id,
                "name": product.name,
                "price": f"₹{final_price:,.0f}" if final_price > 0 else "Compare to reveal",
                "match_percent": "99%",
                "battery_spec": product.battery_spec,
                "display_spec": product.display_spec,
                "processor_spec": product.processor_spec,
                "camera_spec": product.camera_spec,
                "category": product.category,
                "image_url": product.image_url
            }
        }), 200

    except Exception as e:
        print(f"❌ Scanner Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500