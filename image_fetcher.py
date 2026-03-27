# image_fetcher.py
# Fetches phone images using ONLY Serper API (Google Images)
# No hardcoded URLs — everything fetched live from Google

import requests
import urllib.parse
import re
import os
import json

SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")

# ==========================================
# BRAND FALLBACK — used only if Serper fails
# ==========================================
def _brand_fallback(search_name):
    name_lower = str(search_name).lower()
    fallbacks = {
        'apple':    "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=500&q=80",
        'iphone':   "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=500&q=80",
        'samsung':  "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=500&q=80",
        'oneplus':  "https://images.unsplash.com/photo-1585060544812-6b45742d762f?w=500&q=80",
        'xiaomi':   "https://images.unsplash.com/photo-1567581935884-3349723552ca?w=500&q=80",
        'poco':     "https://images.unsplash.com/photo-1567581935884-3349723552ca?w=500&q=80",
        'redmi':    "https://images.unsplash.com/photo-1567581935884-3349723552ca?w=500&q=80",
        'realme':   "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&q=80",
        'vivo':     "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&q=80",
        'oppo':     "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&q=80",
        'motorola': "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500&q=80",
        'nothing':  "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&q=80",
        'google':   "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&q=80",
        'pixel':    "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&q=80",
        'iqoo':     "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&q=80",
        'asus':     "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&q=80",
        'sony':     "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&q=80",
        'nokia':    "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&q=80",
        'lava':     "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&q=80",
        'infinix':  "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&q=80",
        'tecno':    "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&q=80",
    }
    for brand, url in fallbacks.items():
        if brand in name_lower:
            return url
    return "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&q=80"


def fetch_dynamic_image(search_name):
    """
    Fetches the best product image for a phone using Serper API (Google Images).

    Flow:
    1. Clean phone name (remove RAM/storage/5G suffixes)
    2. Search Google Images via Serper API
    3. Filter for portrait/square product shots only
    4. Proxy via DuckDuckGo to prevent 403 errors on Android
    5. Fall back to brand Unsplash image if all searches fail
    """

    if not search_name or str(search_name).strip() == "":
        return _brand_fallback("")

    # ==========================================
    # STEP 1: CLEAN THE PHONE NAME
    # Remove (8GB RAM, 256GB), 5G, 4G etc.
    # so Google gets a clean model name
    # ==========================================
    clean_name = str(search_name).strip()
    clean_name = re.sub(r'\(.*?\)', '', clean_name).strip()          # Remove (8GB RAM, 256GB)
    clean_name = re.sub(r'\d+GB|\d+TB|\d+\+\d+GB', '', clean_name, flags=re.IGNORECASE).strip()
    clean_name = re.sub(r'\b5G\b|\b4G\b', '', clean_name, flags=re.IGNORECASE).strip()
    clean_name = re.sub(r'\s+', ' ', clean_name).strip()

    # ==========================================
    # STEP 2: NO API KEY — USE FALLBACK
    # ==========================================
    if not SERPER_API_KEY:
        print(f"⚠️ No SERPER_API_KEY set. Using brand fallback for: {clean_name}")
        return _brand_fallback(clean_name)

    # ==========================================
    # STEP 3: SERPER API SEARCH
    # Try 3 queries from most specific to general
    # ==========================================
    queries = [
        f"{clean_name} smartphone official product image white background",
        f"{clean_name} phone buy india official image",
        f"{clean_name} smartphone",
    ]

    # Domains that give wrong/bad images
    bad_domains = [
        'youtube', 'facebook', 'instagram', 'twitter', 'tiktok',
        'pinterest', 'reddit', 'gsmarena', 'phonearena', 'logo',
        'icon', 'banner', 'wallpaper', 'meme', 'thumbnail',
        'advertisement', 'tracking', 'pixel', 'analytics',
        'whatsapp', 'telegram', 'snapchat', 'linkedin',
    ]

    for query in queries:
        try:
            response = requests.post(
                "https://google.serper.dev/images",
                headers={
                    'X-API-KEY':    SERPER_API_KEY,
                    'Content-Type': 'application/json'
                },
                data=json.dumps({
                    "q":   query,
                    "num": 10,
                    "gl":  "in",   # India region for better results
                    "hl":  "en"
                }),
                timeout=8
            )

            if response.status_code != 200:
                continue

            images = response.json().get("images", [])

            for img in images:
                img_url = img.get("imageUrl", "")

                # Must be a valid http URL
                if not img_url or not img_url.startswith("http"):
                    continue

                # Skip bad domains
                if any(bad in img_url.lower() for bad in bad_domains):
                    continue

                # Check image dimensions if available
                width  = img.get("imageWidth",  0)
                height = img.get("imageHeight", 0)

                if width > 0 and height > 0:
                    # Skip landscape images (phones are portrait or square)
                    if width > height * 1.4:
                        continue
                    # Skip tiny images (icons/thumbnails)
                    if width < 80 or height < 80:
                        continue

                # ==========================================
                # STEP 4: PROXY VIA DUCKDUCKGO
                # Android Coil gets 403 Forbidden when
                # loading images directly from Amazon/Flipkart.
                # DuckDuckGo proxies the image without this block.
                # Search = Google (Serper) | Delivery = DuckDuckGo
                # ==========================================
                proxy_url = (
                    f"https://external-content.duckduckgo.com/iu/"
                    f"?u={urllib.parse.quote(img_url, safe='')}"
                    f"&f=1&nofb=1"
                )
                return proxy_url

        except Exception as e:
            continue

    # ==========================================
    # STEP 5: BRAND FALLBACK
    # ==========================================
    return _brand_fallback(clean_name)