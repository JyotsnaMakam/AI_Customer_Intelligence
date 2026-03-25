import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="User Registration", layout="wide")
st.title("📝 User Registration & Management")

def get_connection():
    return sqlite3.connect('data/customer_intelligence.db')

# --- 1. INITIALIZE SESSION STATE ---
if 'edit_id' not in st.session_state:
    st.session_state.edit_id = None
if 'reg_name' not in st.session_state:
    st.session_state.reg_name = ""
if 'reg_age' not in st.session_state:
    st.session_state.reg_age = 18
if 'reg_income' not in st.session_state:
    st.session_state.reg_income = 0

# Function to clear the form fields
def clear_form():
    st.session_state.edit_id = None
    st.session_state.reg_name = ""
    st.session_state.reg_age = 18
    st.session_state.reg_income = 0

# --- 2. REGISTRATION / EDIT FORM ---
with st.expander("👤 Register or Edit User", expanded=True):
    # Use 'key' to link widgets directly to session state
    st.text_input("Name", key="reg_name")
    st.number_input("Age", min_value=0, key="reg_age")
    st.number_input("Annual Income ($)", min_value=0, key="reg_income")

    col1, col2 = st.columns([1, 5])
    
    with col1:
        if st.session_state.edit_id is not None:
            # UPDATE LOGIC
            if st.button("Update ✅", type="primary", key="btn_update"):
                conn = get_connection()
                c = conn.cursor()
                c.execute("UPDATE users SET name=?, age=?, income=? WHERE id=?", 
                          (st.session_state.reg_name, st.session_state.reg_age, 
                           st.session_state.reg_income, st.session_state.edit_id))
                conn.commit()
                conn.close()
                st.success("Record updated successfully!")
                clear_form() # This clears the textboxes
                st.rerun()
        else:
            # REGISTER LOGIC
            if st.button("Register", type="primary", key="btn_register"):
                if st.session_state.reg_name.strip() == "":
                    st.error("Please enter a name.")
                else:
                    conn = get_connection()
                    c = conn.cursor()
                    c.execute("INSERT INTO users (name, age, income) VALUES (?,?,?)", 
                              (st.session_state.reg_name, st.session_state.reg_age, 
                               st.session_state.reg_income))
                    conn.commit()
                    conn.close()
                    st.success("User registered successfully!")
                    clear_form() # This clears the textboxes
                    st.rerun()
    
    with col2:
        if st.button("Clear / Cancel ✖️", key="btn_clear"):
            clear_form()
            st.rerun()

# --- 3. DATABASE DISPLAY ---
st.subheader("🔎 Database Records")
conn = get_connection()
df = pd.read_sql_query("SELECT * FROM users", conn)
conn.close()

# Table with Edit/Delete buttons
cols = st.columns([1, 2, 1, 2, 1, 1])
cols[0].write("**ID**")
cols[1].write("**Name**")
cols[2].write("**Age**")
cols[3].write("**Income**")
cols[4].write("**Edit**")
cols[5].write("**Delete**")

for i, row in df.iterrows():
    r_cols = st.columns([1, 2, 1, 2, 1, 1])
    r_cols[0].write(row['id'])
    r_cols[1].write(row['name'])
    r_cols[2].write(row['age'])
    r_cols[3].write(f"${row['income']:,}")
    
    # EDIT BUTTON: Loads data into the form above
    if r_cols[4].button("Edit", key=f"edit_{row['id']}"):
        st.session_state.edit_id = row['id']
        st.session_state.reg_name = row['name']
        st.session_state.reg_age = int(row['age'])
        st.session_state.reg_income = int(row['income'])
        st.rerun()

    # DELETE BUTTON
    if r_cols[5].button("Del", key=f"del_{row['id']}"):
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE id=?", (row['id'],))
        conn.commit()
        conn.close()
        st.rerun()