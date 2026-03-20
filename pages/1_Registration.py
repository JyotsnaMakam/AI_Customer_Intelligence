import streamlit as st
import sqlite3
import pandas as pd

st.title("📝 Customer Registration (SQL Database)")

# --- DATABASE SETUP ---
def init_db():
 conn = sqlite3.connect('data/customer_intelligence.db')
 c = conn.cursor()
# Create table if it doesn't exist
 c.execute('''CREATE TABLE IF NOT EXISTS users
  (id INTEGER PRIMARY KEY AUTOINCREMENT,
   name TEXT, age INTEGER, income REAL, education TEXT)''')
 conn.commit()
 conn.close()

init_db()

# --- REGISTRATION FORM ---
with st.form("sql_registration", clear_on_submit=True):
 name = st.text_input("Full Name")
 age = st.number_input("Age", min_value=18, max_value=100)
 income = st.number_input("Annual Income ($)", min_value=0)
 education = st.selectbox("Education Level", ["Graduation", "PhD", "Master", "Basic"])
 submit = st.form_submit_button("Register to Database")

if submit:
 if name and income:
# Connect and Insert using SQL commands
  conn = sqlite3.connect('data/customer_intelligence.db')
  c = conn.cursor()
  c.execute("INSERT INTO users (name, age, income, education) VALUES (?, ?, ?, ?)",
   (name, age, income, education))
  conn.commit()
  conn.close()

  st.success(f"Successfully saved {name} to the SQL database!")
  st.balloons()
 else:
  st.error("Please fill in all details.")

# --- VIEW LIVE DATABASE ---
if st.checkbox("Show Registered Users (Live SQL Query)"):
 conn = sqlite3.connect('data/customer_intelligence.db')
# Using Pandas to read an SQL query - very common in Data Science!
 df = pd.read_sql_query("SELECT * FROM users", conn)
 st.dataframe(df)
 conn.close()