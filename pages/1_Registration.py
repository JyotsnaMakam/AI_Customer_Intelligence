import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Registration", layout="wide")
st.title("📝 User Registration & Management")

def get_connection():
    return sqlite3.connect('data/customer_intelligence.db')

# --- STEP 1: INITIALIZE SESSION STATE ---
if 'edit_id' not in st.session_state:
    st.session_state.edit_id = None
if 'edit_name' not in st.session_state:
    st.session_state.edit_name = ""
if 'edit_age' not in st.session_state:
    st.session_state.edit_age = 18
if 'edit_income' not in st.session_state:
    st.session_state.edit_income = 0

# --- STEP 2: FORM UI ---
with st.expander("👤 Register or Edit User", expanded=True):
    # CRITICAL: We use 'key' instead of 'value' to ensure two-way syncing
    st.text_input("Name", key="edit_name")
    st.number_input("Age", min_value=0, key="edit_age")
    st.number_input("Annual Income ($)", min_value=0, key="edit_income")

    # --- BUTTON LOGIC WITH UNIQUE KEYS ---
    if st.session_state.edit_id:
        # We use a unique key 'update_btn' to avoid ID conflicts
        if st.button("Update Details ✅", type="primary", key="update_btn"):
            conn = get_connection()
            c = conn.cursor()
            c.execute("UPDATE users SET name=?, age=?, income=? WHERE id=?", 
                      (st.session_state.edit_name, st.session_state.edit_age, 
                       st.session_state.edit_income, st.session_state.edit_id))
            conn.commit()
            conn.close()
            
            # Reset State
            st.session_state.edit_id = None
            st.session_state.edit_name = ""
            st.session_state.edit_age = 18
            st.session_state.edit_income = 0
            
            st.success("Record Updated!")
            st.rerun()
    else:
        # We use a unique key 'register_btn' to avoid ID conflicts
        if st.button("Register User", key="register_btn"):
            if st.session_state.edit_name.strip() == "":
                st.error("Please enter a name.")
            else:
                conn = get_connection()
                c = conn.cursor()
                c.execute("INSERT INTO users (name, age, income) VALUES (?,?,?)", 
                          (st.session_state.edit_name, st.session_state.edit_age, 
                           st.session_state.edit_income))
                conn.commit()
                conn.close()
                
                # Clear State
                st.session_state.edit_name = ""
                st.session_state.edit_age = 18
                st.session_state.edit_income = 0
                
                st.success("User Registered!")
                st.rerun()
        else:
            if st.button("Register User"):
            # Validation: Only proceed if a name is actually typed in
             if name_input.strip() == "":
                st.error("Please enter a name before registering.")
             else:
                conn = get_connection()
                c = conn.cursor()
                c.execute("INSERT INTO users (name, age, income) VALUES (?,?,?)", 
                          (name_input, age_input, income_input))
                conn.commit()
                conn.close()
                
                # Clear form only after a successful registration
                st.session_state.edit_name = ""
                st.session_state.edit_age = 18
                st.session_state.edit_income = 0
                
                st.success(f"Successfully registered {name_input}!")
                st.rerun()
# --- STEP 3: SEARCH & TABLE ---
st.subheader("🔎 Search Database")
search = st.text_input("Filter by name...")

conn = get_connection()
query = "SELECT * FROM users"
if search:
    query = f"SELECT * FROM users WHERE name LIKE '%{search}%'"
df = pd.read_sql_query(query, conn)
conn.close()

# TABLE HEADERS
h_cols = st.columns([1, 2, 1, 2, 1.5, 1.5])
h_cols[0].markdown("**ID**")
h_cols[1].markdown("**Name**")
h_cols[2].markdown("**Age**")
h_cols[3].markdown("**Income**")
h_cols[4].markdown("**Edit**")
h_cols[5].markdown("**Delete**")

# DATA ROWS
for _, row in df.iterrows():
    r_cols = st.columns([1, 2, 1, 2, 1.5, 1.5])
    r_cols[0].write(row['id'])
    r_cols[1].write(row['name'])
    r_cols[2].write(row['age'])
    r_cols[3].write(f"${row['income']:,}")
    
    if r_cols[4].button("Edit 📝", key=f"edit_{row['id']}"):
        st.session_state.edit_id = row['id']
        st.session_state.edit_name = row['name']
        st.session_state.edit_age = int(row['age'])
        st.session_state.edit_income = int(row['income'])
        st.rerun()

    if r_cols[5].button("Del 🗑️", key=f"del_{row['id']}"):
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE id=?", (row['id'],))
        conn.commit()
        conn.close()
        st.rerun()