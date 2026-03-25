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

# --- 2. THE RESET FUNCTION ---
# This is used as a callback to clear the form safely
def reset_callback():
    st.session_state.edit_id = None
    # We clear the widget values by resetting their keys
    st.session_state["reg_name"] = ""
    st.session_state["reg_age"] = 18
    st.session_state["reg_income"] = 0

# --- 3. REGISTRATION / EDIT FORM ---
with st.expander("👤 Register or Edit User", expanded=True):
    # We use keys to link these directly to session state
    name_input = st.text_input("Name", key="reg_name")
    age_input = st.number_input("Age", min_value=0, key="reg_age")
    income_input = st.number_input("Annual Income ($)", min_value=0, key="reg_income")

    col1, col2 = st.columns([1, 5])
    
    with col1:
        if st.session_state.edit_id is not None:
            # UPDATE LOGIC
            if st.button("Update ✅", type="primary", key="btn_update"):
                conn = get_connection()
                c = conn.cursor()
                c.execute("UPDATE users SET name=?, age=?, income=? WHERE id=?", 
                          (name_input, age_input, income_input, st.session_state.edit_id))
                conn.commit()
                conn.close()
                st.success("Record updated!")
                # Call reset directly and rerun
                reset_callback()
                st.rerun()
        else:
            # REGISTER LOGIC
            if st.button("Register", type="primary", key="btn_register"):
                if name_input.strip() == "":
                    st.error("Please enter a name.")
                else:
                    conn = get_connection()
                    c = conn.cursor()
                    c.execute("INSERT INTO users (name, age, income) VALUES (?,?,?)", 
                              (name_input, age_input, income_input))
                    conn.commit()
                    conn.close()
                    st.success("User registered!")
                    reset_callback()
                    st.rerun()
    
    with col2:
        # Use on_click to trigger the reset safely
        st.button("Clear / Cancel ✖️", key="btn_clear", on_click=reset_callback)

# --- 4. DATABASE DISPLAY ---
st.subheader("🔎 Database Records")
conn = get_connection()
df = pd.read_sql_query("SELECT * FROM users", conn)
conn.close()

# Header Row
h_cols = st.columns([1, 2, 1, 2, 1, 1])
h_cols[0].write("**ID**")
h_cols[1].write("**Name**")
h_cols[2].write("**Age**")
h_cols[3].write("**Income**")
h_cols[4].write("**Edit**")
h_cols[5].write("**Delete**")

# Data Rows
for i, row in df.iterrows():
    r_cols = st.columns([1, 2, 1, 2, 1, 1])
    r_cols[0].write(row['id'])
    r_cols[1].write(row['name'])
    r_cols[2].write(row['age'])
    r_cols[3].write(f"${row['income']:,}")
    
    # EDIT BUTTON
    if r_cols[4].button("Edit", key=f"edit_{row['id']}"):
        st.session_state.edit_id = row['id']
        # Set values so they appear in the text boxes
        st.session_state["reg_name"] = row['name']
        st.session_state["reg_age"] = int(row['age'])
        st.session_state["reg_income"] = int(row['income'])
        st.rerun()

    # DELETE BUTTON
    if r_cols[5].button("Del", key=f"del_{row['id']}"):
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE id=?", (row['id'],))
        conn.commit()
        conn.close()
        st.rerun()