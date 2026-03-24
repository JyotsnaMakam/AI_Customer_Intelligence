import streamlit as st
import sqlite3

def save_user(name, age, income):
    conn = sqlite3.connect('data/customer_intelligence.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, age, income) VALUES (?, ?, ?)", (name, age, income))
    conn.commit()
    user_id = c.lastrowid
    conn.close()
    return user_id

st.title("📝 User Registration")

# Initialize session state for editing
if 'registered' not in st.session_state:
    st.session_state.registered = False

if not st.session_state.registered:
    with st.form("reg_form"):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=18, max_value=100)
        income = st.number_input("Annual Income ($)", min_value=0)
        submit = st.form_submit_button("Register")
        
        if submit:
            user_id = save_user(name, age, income)
            st.session_state.user_id = user_id
            st.session_state.user_name = name
            st.session_state.registered = True
            st.rerun()
else:
    st.success(f"Welcome, {st.session_state.user_name}! You are registered.")
    
    # The Edit Icon/Button
    if st.button("Edit Information 📝"):
        # This logic would point to an update query
        st.session_state.registered = False
        st.rerun()