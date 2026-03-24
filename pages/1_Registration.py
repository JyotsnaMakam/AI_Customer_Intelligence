import streamlit as st
import sqlite3
import pandas as pd

st.title("📝 User Registration & Management")

# --- DATABASE FUNCTIONS ---
def get_connection():
    return sqlite3.connect('data/customer_intelligence.db')

def update_user(user_id, name, age, income):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE users SET name=?, age=?, income=? WHERE id=?", (name, age, income, user_id))
    conn.commit()
    conn.close()

# --- STEP 1: SESSION STATE INITIALIZATION ---
# This keeps track of which user we are currently editing
if 'editing_user_id' not in st.session_state:
    st.session_state.editing_user_id = None
if 'edit_name' not in st.session_state:
    st.session_state.edit_name = ""
if 'edit_age' not in st.session_state:
    st.session_state.edit_age = 18
if 'edit_income' not in st.session_state:
    st.session_state.edit_income = 0

# --- STEP 2: THE FORM UI ---
with st.container(border=True):
    st.subheader("Edit/Register User")
    
    # Text boxes are linked to session state values
    new_name = st.text_input("Name", value=st.session_state.edit_name)
    new_age = st.number_input("Age", min_value=0, value=st.session_state.edit_age)
    new_income = st.number_input("Annual Income ($)", min_value=0, value=st.session_state.edit_income)

    if st.session_state.editing_user_id:
        if st.button("Update Details ✅", type="primary"):
            update_user(st.session_state.editing_user_id, new_name, new_age, new_income)
            st.success(f"Updated {new_name} successfully!")
            # Reset the form after update
            st.session_state.editing_user_id = None
            st.rerun()
    else:
        if st.button("Register New User"):
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO users (name, age, income) VALUES (?,?,?)", (new_name, new_age, new_income))
            conn.commit()
            conn.close()
            st.success("User Registered!")
            st.rerun()

# --- STEP 3: DATABASE RECORDS TABLE ---
st.divider()
st.subheader("🔗 Database Records")

conn = get_connection()
df = pd.read_sql_query("SELECT * FROM users", conn)
conn.close()

# We display a custom table with 'Edit' buttons
for index, row in df.iterrows():
    cols = st.columns([1, 2, 1, 2, 2])
    cols[0].write(f"#{row['id']}")
    cols[1].write(row['name'])
    cols[2].write(row['age'])
    cols[3].write(f"${row['income']:,}")
    
    # The 'Edit' button triggers the auto-fill logic
    if cols[4].button("Edit 📝", key=f"edit_{row['id']}"):
        st.session_state.editing_user_id = row['id']
        st.session_state.edit_name = row['name']
        st.session_state.edit_age = int(row['age'])
        st.session_state.edit_income = int(row['income'])
        st.rerun()