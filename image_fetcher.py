# image_fetcher.py
import requests
import urllib.parse
import re
import os
import json

# Load the API key from your .env file
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")

def fetch_dynamic_image(search_name):
    """
    Enterprise-Grade Image Fetcher using Google Images API (via Serper.dev).
    100% reliable, no 403 scraping blocks.
    """
    if not search_name or search_name.strip() == "":
        return "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&q=80"

    # 1. Clean the name so Google Search understands it perfectly
    clean_name = re.sub(r'\(.*?\)', '', search_name).strip()
    clean_name = re.sub(r'\d+GB|\d+TB|\d+\+\d+GB|\d+ Go', '', clean_name, flags=re.IGNORECASE).strip()
    clean_name = re.sub(r'5G|4G', '', clean_name, flags=re.IGNORECASE).strip()
    clean_name = re.sub(r'\s+', ' ', clean_name).strip()

    print(f"🔍 Searching Google Images for: {clean_name}")
    
    # Query optimized for clear product photos
    query = f"{clean_name} smartphone official render white background"

    if SERPER_API_KEY:
        try:
            url = "https://google.serper.dev/images"
            payload = json.dumps({
                "q": query,
                "num": 5  # Fetch top 5 results to find the best one
            })
            headers = {
                'X-API-KEY': SERPER_API_KEY,
                'Content-Type': 'application/json'
            }
            
            # Make the API call
            response = requests.post(url, headers=headers, data=payload, timeout=8)
            
            if response.status_code == 200:
                data = response.json()
                images = data.get("images", [])
                
                for img in images:
                    img_url = img.get("imageUrl")
                    
                    if img_url:
                        # Skip bad websites (like youtube thumbnails)
                        if any(bad in img_url.lower() for bad in ['youtube', 'icon', 'logo', 'avatar', 'gsmarena']):
                            continue
                            
                        # 🚀 PROXY THE URL: We STILL need to proxy it because 
                        # Android Coil will still get 403 Forbidden from Flipkart/Amazon servers!
                        proxy_url = f"https://external-content.duckduckgo.com/iu/?u={urllib.parse.quote(img_url)}"
                        
                        print(f"✅ Image Found via API & Proxied: {proxy_url}")
                        return proxy_url
                        
            else:
                print(f"❌ Serper API Error: {response.text}")

        except Exception as e:
            print(f"❌ Image Fetch Error: {e}")
    else:
        print("⚠️ SERPER_API_KEY is missing in .env! Add it to fetch real images.")

    print("⚠️ Falling back to Unsplash generic image.")
    return "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&q=80"