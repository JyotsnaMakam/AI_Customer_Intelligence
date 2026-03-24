import streamlit as st
import sqlite3
import pandas as pd

st.title("📝 User Registration & Management")

def get_connection():
    return sqlite3.connect('data/customer_intelligence.db')

# --- SESSION STATE FOR EDITING ---
if 'edit_id' not in st.session_state:
    st.session_state.edit_id = None
if 'edit_name' not in st.session_state:
    st.session_state.edit_name = ""
if 'edit_age' not in st.session_state:
    st.session_state.edit_age = 18
if 'edit_income' not in st.session_state:
    st.session_state.edit_income = 0

# --- FORM UI ---
with st.expander("👤 Register or Edit User", expanded=True):
    name_input = st.text_input("Name", value=st.session_state.edit_name)
    age_input = st.number_input("Age", min_value=0, value=st.session_state.edit_age)
    income_input = st.number_input("Annual Income ($)", min_value=0, value=st.session_state.edit_income)

    if st.session_state.edit_id:
        if st.button("Update Details ✅", type="primary"):
            conn = get_connection()
            c = conn.cursor()
            c.execute("UPDATE users SET name=?, age=?, income=? WHERE id=?", 
                      (name_input, age_input, income_input, st.session_state.edit_id))
            conn.commit()
            conn.close()
            st.success("User updated!")
            st.session_state.edit_id = None # Reset
            st.rerun()
    else:
        if st.button("Register User"):
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO users (name, age, income) VALUES (?,?,?)", (name_input, age_input, income_input))
            conn.commit()
            conn.close()
            st.success("User registered!")
            st.rerun()

# --- DATABASE TABLE (The Fix for your Error) ---
st.subheader("🔎 Search Database")
search = st.text_input("Type a name to filter...")

conn = get_connection()
query = "SELECT * FROM users"
if search:
    query = f"SELECT * FROM users WHERE name LIKE '%{search}%'"
df = pd.read_sql_query(query, conn)
conn.close()

# HEADER ROW (FIXED: Using bold markdown instead of .bold() function)
h_cols = st.columns([1, 2, 1, 2, 2])
h_cols[0].markdown("**ID**")
h_cols[1].markdown("**Name**")
h_cols[2].markdown("**Age**")
h_cols[3].markdown("**Income**")
h_cols[4].markdown("**Action**")

# DATA ROWS
for _, row in df.iterrows():
    r_cols = st.columns([1, 2, 1, 2, 2])
    r_cols[0].write(row['id'])
    r_cols[1].write(row['name'])
    r_cols[2].write(row['age'])
    r_cols[3].write(f"${row['income']:,}")
    
    # When clicked, this fills the form at the top
    if r_cols[4].button("Edit 📝", key=f"btn_{row['id']}"):
        st.session_state.edit_id = row['id']
        st.session_state.edit_name = row['name']
        st.session_state.edit_age = int(row['age'])
        st.session_state.edit_income = int(row['income'])
        st.rerun()