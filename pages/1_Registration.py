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

# Function to reset the text boxes
def reset_form():
    st.session_state.editing_user_id = None
    st.session_state.edit_name = ""
    st.session_state.edit_age = 18
    st.session_state.edit_income = 0

# --- STEP 1: SESSION STATE INITIALIZATION ---
if 'editing_user_id' not in st.session_state:
    reset_form()

# --- STEP 2: THE FORM UI ---
with st.container(border=True):
    # Dynamic header based on mode
    mode = "Edit Mode 📝" if st.session_state.editing_user_id else "New Registration 🆕"
    st.subheader(mode)
    
    new_name = st.text_input("Name", value=st.session_state.edit_name)
    new_age = st.number_input("Age", min_value=0, value=st.session_state.edit_age)
    new_income = st.number_input("Annual Income ($)", min_value=0, value=st.session_state.edit_income)

    col_btn1, col_btn2 = st.columns([1, 4])
    
    if st.session_state.editing_user_id:
        if col_btn1.button("Update ✅", type="primary"):
            update_user(st.session_state.editing_user_id, new_name, new_age, new_income)
            st.success(f"Successfully updated {new_name}!")
            reset_form() # This clears the text boxes
            st.rerun()
        if col_btn2.button("Cancel / Clear"):
            reset_form()
            st.rerun()
    else:
        if col_btn1.button("Register"):
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO users (name, age, income) VALUES (?,?,?)", (new_name, new_age, new_income))
            conn.commit()
            conn.close()
            st.success("User Registered!")
            reset_form()
            st.rerun()

# --- STEP 3: SEARCH & FILTER ---
st.divider()
st.subheader("🔍 Search Database")
search_query = st.text_input("Search by Name", placeholder="Type a name to filter...")

# --- STEP 4: DATABASE RECORDS TABLE ---
conn = get_connection()
query = "SELECT * FROM users"
df = pd.read_sql_query(query, conn)
conn.close()

# Apply the filter if search box is not empty
if search_query:
    df = df[df['name'].str.contains(search_query, case=False, na=False)]

if df.empty:
    st.warning("No users found.")
else:
    # Header for the table
    h_cols = st.columns([1, 2, 1, 2, 2])
    h_cols[0].bold("ID")
    h_cols[1].bold("Name")
    h_cols[2].bold("Age")
    h_cols[3].bold("Income")
    h_cols[4].bold("Action")

    for index, row in df.iterrows():
        cols = st.columns([1, 2, 1, 2, 2])
        cols[0].write(row['id'])
        cols[1].write(row['name'])
        cols[2].write(row['age'])
        cols[3].write(f"${row['income']:,}")
        
        if cols[4].button("Edit 📝", key=f"edit_{row['id']}"):
            st.session_state.editing_user_id = row['id']
            st.session_state.edit_name = row['name']
            st.session_state.edit_age = int(row['age'])
            st.session_state.edit_income = int(row['income'])
            st.rerun()