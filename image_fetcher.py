# image_fetcher.py
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import json

def fetch_dynamic_image(search_name):
    """
    The Ultimate Dual-Engine Image Scraper.
    Tries Bing Images first for high-res products, falls back to Yahoo if blocked.
    Forces clean, Flipkart/Amazon style e-commerce product shots.
    """
    # 1. Aggressively clean the name so search engines don't get confused
    clean_name = re.sub(r'\(.*?\)', '', search_name).strip()
    clean_name = re.sub(r'\d+GB|\d+TB|\d+\+\d+Gb|\d+ Go', '', clean_name, flags=re.IGNORECASE).strip()
    
    # 🚀 THE FIX: Force Flipkart/Amazon style images (Front view, pure white background)
    query = f"{clean_name} smartphone front view white background amazon flipkart"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }

    # ==========================================
    # ENGINE 1: BING IMAGES (Best Quality)
    # ==========================================
    try:
        print(f"🔍 Searching Bing Images for: {clean_name}")
        bing_url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&form=HDRSC2"
        
        res = requests.get(bing_url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Bing stores high-res image URLs inside a JSON string in the 'm' attribute
        for a in soup.find_all('a', class_='iusc'):
            m_data = a.get('m')
            if m_data:
                img_url = json.loads(m_data).get('murl')
                # Ignore bad domains that block frontend rendering or provide messy images
                bad_domains = ['gsmarena', 'phonearena', 'youtube', 'ui-avatars', 'video', 'pinterest']
                if img_url and img_url.startswith('http') and not any(bad in img_url.lower() for bad in bad_domains):
                    print(f"📸 SUCCESS! Found Flipkart/Amazon style Bing Image.")
                    return img_url
                    
        print("⚠️ Bing returned no valid images. Switching to Yahoo...")
    except Exception as e:
        print(f"⚠️ Bing Search failed: {e}. Switching to Yahoo...")

    # ==========================================
    # ENGINE 2: YAHOO IMAGES (Bulletproof Backup)
    # ==========================================
    try:
        print(f"🔍 Searching Yahoo Images for: {clean_name}")
        yahoo_url = f"https://images.search.yahoo.com/search/images?p={urllib.parse.quote(query)}"
        
        res = requests.get(yahoo_url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        for img in soup.find_all('img'):
            src = img.get('data-src') or img.get('src')
            # Ensure it's a real image and not a tracking pixel or logo
            if src and src.startswith('http') and 'space' not in src and 'logo' not in src.lower():
                print(f"📸 SUCCESS! Found Flipkart/Amazon style Yahoo Image.")
                return src
                
    except Exception as e:
        print(f"⚠️ Yahoo Search failed: {e}")

    # ==========================================
    # GUARANTEED UNBLOCKED FALLBACK
    # ==========================================
    print(f"🔄 Using generic smartphone image for {search_name}")
    # If the phone doesn't exist at all, return a high-quality generic phone photo
    return "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&q=80"