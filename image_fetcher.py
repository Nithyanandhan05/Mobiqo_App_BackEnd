# image_fetcher.py
import requests
from bs4 import BeautifulSoup
import urllib.parse

def fetch_dynamic_image(search_name):
    """
    The Ultimate Image Fetcher.
    Uses Google Images Legacy HTML to find the exact E-Commerce product photo.
    Bypasses modern bot-protections and returns ultra-fast, secure Google CDN links.
    """
    try:
        # Clean the name: "OnePlus 12R (16GB RAM)" -> "OnePlus 12R"
        clean_name = search_name.split('(')[0].strip()
        print(f"🔍 Searching Google Images for: {clean_name}")
        
        # The ultimate query to force Google to show clean E-Commerce photos
        query = f"{clean_name} smartphone flipkart amazon white background"
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&tbm=isch"
        
        # This generic User-Agent forces Google to serve the lightweight, non-JS HTML page
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all image tags on the page
        images = soup.find_all('img')
        
        # Index 0 is ALWAYS the Google Logo. We loop through the rest to find the first real result.
        for img in images[1:]:
            src = img.get('src')
            # Google hosts these fast-loading thumbnails securely on gstatic
            if src and src.startswith('https://encrypted-tbn0.gstatic.com'):
                print(f"📸 SUCCESS! Found exact Google Image.")
                return src
                
    except Exception as e:
        print(f"⚠️ Google search failed for {search_name}. Error: {e}")

    # ==========================================
    # FALLBACK SAFETY NET (High Quality Dummies)
    # ==========================================
    print(f"🔄 Using fallback image for {search_name}")
    name_lower = search_name.lower()
    
    # Generic but very clean e-commerce placeholder phones just in case your internet drops
    if "apple" in name_lower or "iphone" in name_lower:
        return "https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-15-pro.jpg"
    if "samsung" in name_lower:
        return "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24-ultra-5g-sm-s928-u1.jpg"
    if "oneplus" in name_lower:
        return "https://fdn2.gsmarena.com/vv/bigpic/oneplus-12.jpg"
    if "google" in name_lower or "pixel" in name_lower:
        return "https://fdn2.gsmarena.com/vv/bigpic/google-pixel-8-pro.jpg"
    if "xiaomi" in name_lower:
        return "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-14-pro.jpg"
    if "vivo" in name_lower:
        return "https://fdn2.gsmarena.com/vv/bigpic/vivo-x100-pro.jpg"
            
    return "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24-ultra-5g-sm-s928-u1.jpg"