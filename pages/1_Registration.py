import streamlit as st
import sqlite3
import pandas as pd

# --- DATABASE FUNCTIONS ---
def get_db_connection():
    return sqlite3.connect('data/customer_intelligence.db')

def update_user(user_id, name, age, income):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""UPDATE users SET name=?, age=?, income=? WHERE id=?""", 
              (name, age, income, user_id))
    conn.commit()
    conn.close()

def save_new_user(name, age, income):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO users (name, age, income) VALUES (?, ?, ?)", (name, age, income))
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return new_id

# --- INTERFACE ---
st.title("📝 Customer Portal")

# 1. Initialize session state
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# 2. Logic to pre-fill the form
# If we are in edit mode, we pull the current values from the session
default_name = st.session_state.get('user_name', "")
default_age = st.session_state.get('user_age', 18)
default_income = st.session_state.get('user_income', 0)

# 3. THE FORM
with st.form("user_form"):
    st.subheader("Edit Profile" if st.session_state.edit_mode else "Register New Account")
    
    new_name = st.text_input("Full Name", value=default_name)
    new_age = st.number_input("Age", min_value=18, max_value=100, value=default_age)
    new_income = st.number_input("Annual Income ($)", min_value=0, value=default_income)
    
    submit_label = "Update Details" if st.session_state.edit_mode else "Register"
    submitted = st.form_submit_button(submit_label)

    if submitted:
        if st.session_state.edit_mode:
            # UPDATE existing user
            update_user(st.session_state.user_id, new_name, new_age, new_income)
            st.success("Profile Updated!")
        else:
            # SAVE new user
            u_id = save_new_user(new_name, new_age, new_income)
            st.session_state.user_id = u_id
            st.success("Registration Successful!")
        
        # Save values to session so they "stick" in the textboxes
        st.session_state.user_name = new_name
        st.session_state.user_age = new_age
        st.session_state.user_income = new_income
        st.session_state.edit_mode = True # Switch to edit mode after registering
        st.rerun()

# 4. THE ACTION BUTTONS
st.divider()
col1, col2 = st.columns(2)

with col1:
    if st.button("Edit My Info 📝"):
        st.session_state.edit_mode = True
        st.rerun()

with col2:
    if st.button("View All Registered Users 📊"):
        conn = get_db_connection()
        all_users = pd.read_sql_query("SELECT id, name, age, income FROM users", conn)
        conn.close()
        st.write("### Database Records")
        st.dataframe(all_users)