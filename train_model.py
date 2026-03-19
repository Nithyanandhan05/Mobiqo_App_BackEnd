# train_model.py
# ✅ Run this file ONCE to train your AI model
# Command: python train_model.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

print("🚀 Starting AI Model Training...")

# ==========================================
# STEP 1: LOAD YOUR DATASET
# ==========================================
df = pd.read_csv("smartphones_dataset.csv")
print(f"✅ Dataset loaded!")

# ==========================================
# STEP 2: CLEAN THE DATA
# ==========================================

# Fill any empty values
df['brand']    = df['brand'].fillna('Unknown')
df['best_for'] = df['best_for'].fillna('all-rounder')
df['5g_support'] = df['5g_support'].fillna('No')
df['rating']   = df['rating'].fillna(4.0)
df['price']    = df['price'].fillna(20000)
df['ram']      = df['ram'].fillna(6)
df['storage']  = df['storage'].fillna(128)
df['battery']  = df['battery'].fillna(5000)
df['camera_mp']= df['camera_mp'].fillna(50)

print("✅ Data cleaned!")

# ==========================================
# STEP 3: ENCODE TEXT COLUMNS TO NUMBERS
# (AI only understands numbers, not words)
# ==========================================

le_brand   = LabelEncoder()
le_bestfor = LabelEncoder()
le_5g      = LabelEncoder()

df['brand_encoded']   = le_brand.fit_transform(df['brand'])
df['bestfor_encoded'] = le_bestfor.fit_transform(df['best_for'])
df['5g_encoded']      = le_5g.fit_transform(df['5g_support'])

print("✅ Text columns converted to numbers!")

# ==========================================
# STEP 4: DEFINE FEATURES (INPUTS TO AI)
# ==========================================

# These are what the USER gives us
# AI uses these to find the best phone
feature_columns = [
    'price',        # User's budget
    'ram',          # RAM needed
    'storage',      # Storage needed
    'battery',      # Battery needed
    'camera_mp',    # Camera needed
    '5g_encoded',   # 5G yes/no
    'brand_encoded' # Brand preference
]

# This is what AI will PREDICT (the best_for category)
target_column = 'bestfor_encoded'

X = df[feature_columns]  # Inputs
y = df[target_column]    # Output to predict

print(f"✅ Features ready! Training on {len(X)} phones...")

# ==========================================
# STEP 5: TRAIN THE AI MODEL
# ==========================================

model = RandomForestClassifier(
    n_estimators=200,   # 200 decision trees (more = smarter)
    max_depth=15,       # How deep each tree can go
    random_state=42     # Keeps results consistent
)

model.fit(X, y)
print("✅ AI Model trained successfully!")

# ==========================================
# STEP 6: SAVE THE MODEL & ENCODERS
# ==========================================

joblib.dump(model,     'phone_model.pkl')
joblib.dump(le_brand,  'encoder_brand.pkl')
joblib.dump(le_bestfor,'encoder_bestfor.pkl')
joblib.dump(le_5g,     'encoder_5g.pkl')

print("✅ Model saved as 'phone_model.pkl'!")
print("✅ Encoders saved!")

# ==========================================
# STEP 7: TEST THE MODEL QUICKLY
# ==========================================

print("\n🧪 Quick Test:")
print("User wants: Budget ₹20000, 8GB RAM, 256GB storage, Gaming, Samsung, 5G")

test_input = pd.DataFrame([{
    'price':    20000,
    'ram':      8,
    'storage':  256,
    'battery':  5000,
    'camera_mp':50,
    '5g_encoded':   le_5g.transform(['Yes'])[0],
    'brand_encoded': le_brand.transform(['Samsung'])[0]
              if 'Samsung' in le_brand.classes_
              else 0
}])

predicted_encoded = model.predict(test_input)[0]
predicted_usage   = le_bestfor.inverse_transform([predicted_encoded])[0]
print(f"🤖 AI Prediction: Best phone category = '{predicted_usage}'")

# Show top 3 matching phones from dataset
matched = df[df['bestfor_encoded'] == predicted_encoded]
matched = matched[
    (matched['price'] >= 16000) &
    (matched['price'] <= 22000)
].head(3)

if not matched.empty:
    print("\n📱 Top matching phones from your dataset:")
    for _, row in matched.iterrows():
        print(f"   → {row['brand']} {row['model']} | ₹{row['price']} | {row['best_for']} | ⭐{row['rating']}")
else:
    print("No exact match found in test, but model is working!")

print("\n🎉 Training Complete! Your AI is ready.")
print("📁 Files created:")
print("   → phone_model.pkl     (main AI model)")
print("   → encoder_brand.pkl   (brand encoder)")
print("   → encoder_bestfor.pkl (usage encoder)")
print("   → encoder_5g.pkl      (5G encoder)")
print("\n▶️  Next: Copy these .pkl files to your Flask project folder")
print("▶️  Then update your app.py to use local AI instead of Gemini API!")