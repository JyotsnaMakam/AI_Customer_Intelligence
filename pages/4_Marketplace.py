import streamlit as st
import pandas as pd
import sqlite3
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

st.title("🛒 Module 3: AI-Powered Marketplace")

def get_user_persona():
    # 1. Connect to SQL to get YOUR data
    conn = sqlite3.connect('data/customer_intelligence.db')
    sql_df = pd.read_sql_query("SELECT * FROM users ORDER BY id DESC LIMIT 1", conn)
    conn.close()
    
    if sql_df.empty:
        return None, None

    # 2. Load the Kaggle data to 'train' the logic
    df = pd.read_csv("data/customer_data.csv", sep=None, engine='python')
    df_numeric = df.select_dtypes(include=['number']).dropna()
    if 'ID' in df_numeric.columns:
        df_numeric = df_numeric.drop(columns=['ID'])

    # 3. Match the math from the previous pages
    scaler = StandardScaler()
    scaled_base = scaler.fit_transform(df_numeric)
    pca = PCA(n_components=3)
    pca_base = pca.fit_transform(scaled_base)
    kmeans = KMeans(n_clusters=4, random_state=42)
    kmeans.fit(pca_base)

    # 4. Predict YOUR persona
    # Fill missing columns with averages so the math works
    for col in df_numeric.columns:
        if col not in sql_df.columns:
            sql_df[col] = df_numeric[col].mean()
            
    user_scaled = scaler.transform(sql_df[df_numeric.columns])
    user_pca = pca.transform(user_scaled)
    cluster_id = kmeans.predict(user_pca)[0]
    
    return sql_df['name'].iloc[0], cluster_id

name, cluster = get_user_persona()

if name:
    st.write(f"### Welcome back, {name}!")
    
    # Define what each cluster gets recommended
    recommendations = {
        0: {"label": "💎 Platinum Elite", "items": ["Fine Vintage Wine", "Organic Wagyu Beef", "Premium Caviar"]},
        1: {"label": "👔 Professional", "items": ["Smart Home Assistant", "Coffee Subscription", "Ergonomic Chair"]},
        2: {"label": "🛒 Value Seeker", "items": ["Family-Sized Pasta Pack", "Bulk Detergent", "Daily Vitamin Set"]},
        3: {"label": "🎓 Budget Student", "items": ["Instant Noodle Bundle", "Study Lamp", "Portable Power Bank"]}
    }

    my_group = recommendations.get(cluster)
    st.info(f"AI Analysis: You are in the **{my_group['label']}** segment.")
    
    st.write("#### 🎯 Recommended for Your Lifestyle:")
    cols = st.columns(3)
    for i, item in enumerate(my_group['items']):
        cols[i].metric("Deal", item)
        cols[i].button(f"Buy {item}", key=i)
else:
    st.warning("Please go to the **Registration** page and sign up first to see your persona!")