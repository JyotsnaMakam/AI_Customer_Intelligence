import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="AI Marketplace", layout="wide")

def get_connection():
    return sqlite3.connect('data/customer_intelligence.db')

st.title("🛒 Module 3: AI-Powered Marketplace")

# --- 1. FETCH ALL USERS FROM DATABASE ---
conn = get_connection()
df_users = pd.read_sql_query("SELECT * FROM users", conn)
conn.close()

if df_users.empty:
    st.warning("No users found in the database. Please register a user first!")
    st.stop()

# --- 2. USER SELECTION ---
# This replaces the hardcoded "Aravind" name
selected_user_name = st.selectbox("Select User to Login:", df_users['name'].tolist())
user_data = df_users[df_users['name'] == selected_user_name].iloc[0]

user_income = float(user_data['income'])
st.subheader(f"Welcome back, {selected_user_name}! 👋")

# --- 3. DYNAMIC AI SEGMENTATION LOGIC ---
# This is the logic that moves you to 'Elite' based on the 4 crore income
if user_income >= 1000000:  # 1 Million+
    segment_label = "💎 Elite Customer"
    segment_color = "gold"
    recommendations = [
        {"item": "Luxury Private Jet Charter", "price": "$50,000", "desc": "Exclusive travel for elite members."},
        {"item": "Rolex Oyster Perpetual", "price": "$12,000", "desc": "A timeless investment for your collection."},
        {"item": "Premium Real Estate Consultation", "price": "Free", "desc": "VIP access to global properties."}
    ]
elif user_income >= 50000:
    segment_label = "💼 Working Professional"
    segment_color = "blue"
    recommendations = [
        {"item": "Ergonomic Office Chair", "price": "$450", "desc": "Maximize productivity and comfort."},
        {"item": "Noise-Cancelling Headphones", "price": "$299", "desc": "Focus anywhere with top-tier tech."},
        {"item": "Annual Productivity Suite", "price": "$99", "desc": "The tools you need to succeed."}
    ]
else:
    segment_label = "🎓 Budget Student"
    segment_color = "green"
    recommendations = [
        {"item": "Instant Noodle Bundle", "price": "$15", "desc": "Quick meals for late-night study sessions."},
        {"item": "Adjustable Study Lamp", "price": "$25", "desc": "Brighten up your workspace."},
        {"item": "Portable Power Bank", "price": "$40", "desc": "Keep your devices charged on campus."}
    ]

# --- 4. DISPLAY AI ANALYSIS ---
st.info(f"**AI Analysis:** You are in the {segment_label} segment based on your income of **${user_income:,.2f}**.")

# --- 5. DISPLAY RECOMMENDATIONS ---
st.write("### 🎯 Recommended for Your Lifestyle:")
cols = st.columns(3)

for i, rec in enumerate(recommendations):
    with cols[i]:
        with st.container(border=True):
            st.write(f"**{rec['item']}**")
            st.caption(rec['desc'])
            st.markdown(f"**Price:** {rec['price']}")
            if st.button(f"Buy {rec['item']}", key=f"buy_{i}"):
                st.success(f"Added {rec['item']} to cart!")