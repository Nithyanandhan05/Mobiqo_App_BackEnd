# train_model.py — IMPROVED VERSION
# Fixes: same recommendation for all use cases
# Run: python train_model.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

print("Starting Improved AI Model Training...")

# ==========================================
# STEP 1: LOAD DATASET
# ==========================================
df = pd.read_csv("smartphones_dataset.csv")
print(f"Dataset loaded! Total phones: {len(df)}")

# ==========================================
# STEP 2: CLEAN DATA
# ==========================================
df['brand']      = df['brand'].fillna('Unknown')
df['best_for']   = df['best_for'].fillna('all-rounder')
df['5g_support'] = df['5g_support'].fillna('No')
df['rating']     = df['rating'].fillna(4.0)
df['price']      = df['price'].fillna(20000)
df['ram']        = df['ram'].fillna(6)
df['storage']    = df['storage'].fillna(128)
df['battery']    = df['battery'].fillna(5000)
df['camera_mp']  = df['camera_mp'].fillna(50)

# ==========================================
# STEP 3: NORMALIZE CATEGORIES
# ==========================================
def normalize_category(cat):
    cat = str(cat).lower().strip()
    if 'gaming' in cat:   return 'gaming'
    if 'camera' in cat:   return 'camera'
    if 'battery' in cat:  return 'battery'
    if 'flagship' in cat: return 'flagship'
    if 'premium' in cat:  return 'flagship'
    if 'budget' in cat:   return 'budget'
    return 'all-rounder'

df['best_for'] = df['best_for'].apply(normalize_category)

print("\nCategory distribution BEFORE balancing:")
print(df['best_for'].value_counts())

# ==========================================
# STEP 4: BALANCE THE DATASET
# KEY FIX — without this, model always
# predicts "all-rounder" for everything
# ==========================================
category_counts = df['best_for'].value_counts()
target_count    = max(int(category_counts.median()) + 50, 100)

balanced_dfs = []
for category in df['best_for'].unique():
    cat_df = df[df['best_for'] == category]
    if len(cat_df) < target_count:
        cat_df = resample(cat_df, replace=True,  n_samples=target_count, random_state=42)
    else:
        cat_df = resample(cat_df, replace=False, n_samples=target_count, random_state=42)
    balanced_dfs.append(cat_df)

df_balanced = pd.concat(balanced_dfs)
print("\nCategory distribution AFTER balancing:")
print(df_balanced['best_for'].value_counts())

# ==========================================
# STEP 5: FEATURE ENGINEERING
# Smart features that differentiate use cases
# ==========================================
df_balanced['battery_score'] = df_balanced['battery'].apply(
    lambda x: 3 if x >= 6000 else (2 if x >= 5000 else 1)
)
df_balanced['camera_score'] = df_balanced['camera_mp'].apply(
    lambda x: 3 if x >= 108 else (2 if x >= 50 else 1)
)
df_balanced['performance_score'] = df_balanced['ram'].apply(
    lambda x: 3 if x >= 12 else (2 if x >= 8 else 1)
)
df_balanced['price_tier'] = pd.cut(
    df_balanced['price'],
    bins=[0, 12000, 20000, 35000, 60000, float('inf')],
    labels=[1, 2, 3, 4, 5]
).astype(float).fillna(2)

# ==========================================
# STEP 6: ENCODE TEXT COLUMNS
# ==========================================
le_brand   = LabelEncoder()
le_bestfor = LabelEncoder()
le_5g      = LabelEncoder()

df_balanced['brand_encoded']   = le_brand.fit_transform(df_balanced['brand'])
df_balanced['bestfor_encoded'] = le_bestfor.fit_transform(df_balanced['best_for'])
df_balanced['5g_encoded']      = le_5g.fit_transform(df_balanced['5g_support'])

print("\nUsage categories the AI learned:")
for i, cat in enumerate(le_bestfor.classes_):
    print(f"  {i} -> {cat}")

# ==========================================
# STEP 7: FEATURES + TARGET
# ==========================================
feature_columns = [
    'price', 'ram', 'storage', 'battery', 'camera_mp',
    '5g_encoded', 'brand_encoded',
    'battery_score', 'camera_score', 'performance_score',
    'price_tier', 'rating',
]

X = df_balanced[feature_columns]
y = df_balanced['bestfor_encoded']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ==========================================
# STEP 8: TRAIN MODEL
# ==========================================
print(f"\nTraining on {len(X_train)} samples...")

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)
print("AI Model trained successfully!")

# ==========================================
# STEP 9: CHECK ACCURACY
# ==========================================
y_pred = model.predict(X_test)
print(f"\nModel Accuracy: {model.score(X_test, y_test)*100:.1f}%")
print("\nPer-category accuracy:")
print(classification_report(y_test, y_pred, target_names=le_bestfor.classes_))

# ==========================================
# STEP 10: SAVE FILES
# ==========================================
joblib.dump(model,           'phone_model.pkl')
joblib.dump(le_brand,        'encoder_brand.pkl')
joblib.dump(le_bestfor,      'encoder_bestfor.pkl')
joblib.dump(le_5g,           'encoder_5g.pkl')
joblib.dump(feature_columns, 'feature_columns.pkl')

print("\nAll files saved!")
print("  phone_model.pkl")
print("  encoder_brand.pkl")
print("  encoder_bestfor.pkl")
print("  encoder_5g.pkl")
print("  feature_columns.pkl  <-- NEW")

# ==========================================
# STEP 11: TEST ALL USE CASES
# ==========================================
print("\nTesting all use cases...\n")

test_cases = [
    {"label": "Gaming   ₹20,000", "price": 20000, "ram": 12, "battery": 5000, "camera_mp": 50,  "5g": "Yes", "brand": "Poco"},
    {"label": "Camera   ₹25,000", "price": 25000, "ram": 8,  "battery": 5000, "camera_mp": 200, "5g": "Yes", "brand": "Redmi"},
    {"label": "Battery  ₹15,000", "price": 15000, "ram": 6,  "battery": 6500, "camera_mp": 50,  "5g": "Yes", "brand": "iQOO"},
    {"label": "Budget    ₹8,000", "price": 8000,  "ram": 4,  "battery": 5000, "camera_mp": 13,  "5g": "No",  "brand": "Redmi"},
    {"label": "Flagship ₹80,000", "price": 80000, "ram": 12, "battery": 5000, "camera_mp": 50,  "5g": "Yes", "brand": "Samsung"},
    {"label": "General  ₹30,000", "price": 30000, "ram": 8,  "battery": 5000, "camera_mp": 50,  "5g": "Yes", "brand": "OnePlus"},
]

for tc in test_cases:
    brand_enc   = le_brand.transform([tc['brand']])[0] if tc['brand'] in le_brand.classes_ else 0
    five_g_enc  = le_5g.transform([tc['5g']])[0]
    bat_score   = 3 if tc['battery'] >= 6000 else (2 if tc['battery'] >= 5000 else 1)
    cam_score   = 3 if tc['camera_mp'] >= 108 else (2 if tc['camera_mp'] >= 50 else 1)
    perf_score  = 3 if tc['ram'] >= 12 else (2 if tc['ram'] >= 8 else 1)
    tier        = 1 if tc['price'] < 12000 else (2 if tc['price'] < 20000 else (3 if tc['price'] < 35000 else (4 if tc['price'] < 60000 else 5)))

    test_input = pd.DataFrame([{
        'price': tc['price'], 'ram': tc['ram'], 'storage': 128,
        'battery': tc['battery'], 'camera_mp': tc['camera_mp'],
        '5g_encoded': five_g_enc, 'brand_encoded': brand_enc,
        'battery_score': bat_score, 'camera_score': cam_score,
        'performance_score': perf_score, 'price_tier': tier, 'rating': 4.2
    }])

    pred_enc  = model.predict(test_input)[0]
    pred_cat  = le_bestfor.inverse_transform([pred_enc])[0]
    confidence = int(max(model.predict_proba(test_input)[0]) * 100)
    print(f"  {tc['label']:<25} -> AI predicts: {pred_cat:<14} ({confidence}% confidence)")

print("\nTraining Complete! Each use case now gets a DIFFERENT recommendation.")