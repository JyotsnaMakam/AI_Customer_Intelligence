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
if 'default_name' not in st.session_state:
    st.session_state.default_name = ""
if 'default_age' not in st.session_state:
    st.session_state.default_age = 18
if 'default_income' not in st.session_state:
    st.session_state.default_income = 0

# --- 2. REGISTRATION / EDIT FORM ---
# We use st.form to group the inputs together
with st.form("user_form", clear_on_submit=True):
    st.subheader("👤 Register or Edit User")
    
    # We use 'value' instead of 'key' here to prevent the API Exception
    name = st.text_input("Name", value=st.session_state.default_name)
    age = st.number_input("Age", min_value=0, value=st.session_state.default_age)
    income = st.number_input("Annual Income ($)", min_value=0, value=st.session_state.default_income)

    submit_label = "Update Details ✅" if st.session_state.edit_id else "Register User 🚀"
    submit_button = st.form_submit_button(submit_label)

    if submit_button:
        if name.strip() == "":
            st.error("Please enter a name.")
        else:
            conn = get_connection()
            c = conn.cursor()
            
            if st.session_state.edit_id:
                # UPDATE EXISTING RECORD
                c.execute("UPDATE users SET name=?, age=?, income=? WHERE id=?", 
                          (name, age, income, st.session_state.edit_id))
                st.success(f"Updated {name} successfully!")
            else:
                # REGISTER NEW RECORD
                c.execute("INSERT INTO users (name, age, income) VALUES (?,?,?)", (name, age, income))
                st.success(f"Registered {name} successfully!")
            
            conn.commit()
            conn.close()
            
            # Reset defaults for the next time the form renders
            st.session_state.edit_id = None
            st.session_state.default_name = ""
            st.session_state.default_age = 18
            st.session_state.default_income = 0
            
            st.rerun()

# --- 3. DATABASE DISPLAY ---
st.subheader("🔎 Database Records")
conn = get_connection()
df = pd.read_sql_query("SELECT * FROM users", conn)
conn.close()

# Display Table with Action Buttons
h_cols = st.columns([1, 2, 1, 2, 1, 1])
h_cols[0].write("**ID**")
h_cols[1].write("**Name**")
h_cols[2].write("**Age**")
h_cols[3].write("**Income**")
h_cols[4].write("**Edit**")
h_cols[5].write("**Delete**")

for i, row in df.iterrows():
    r_cols = st.columns([1, 2, 1, 2, 1, 1])
    r_cols[0].write(row['id'])
    r_cols[1].write(row['name'])
    r_cols[2].write(row['age'])
    r_cols[3].write(f"${row['income']:,}")
    
    # EDIT: This sets the "defaults" and reruns the page to fill the form above
    if r_cols[4].button("Edit", key=f"edit_{row['id']}"):
        st.session_state.edit_id = row['id']
        st.session_state.default_name = row['name']
        st.session_state.default_age = int(row['age'])
        st.session_state.default_income = int(row['income'])
        st.rerun()

    # DELETE
    if r_cols[5].button("Del", key=f"del_{row['id']}"):
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE id=?", (row['id'],))
        conn.commit()
        conn.close()
        st.rerun()