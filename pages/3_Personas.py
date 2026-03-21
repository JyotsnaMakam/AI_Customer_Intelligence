import streamlit as st
import pandas as pd
import sqlite3
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import plotly.express as px
import numpy as np

st.title("👥 Module 2: AI Customer Personas")

@st.cache_data
def get_base_data():
# 1. Load Kaggle Data
 df = pd.read_csv("data/customer_data.csv", sep=None, engine='python')
 df_numeric = df.select_dtypes(include=['number']).dropna()
 if 'ID' in df_numeric.columns:
  df_numeric = df_numeric.drop(columns=['ID'])
 return df_numeric

try:
# --- STEP 1: Process Kaggle Data ---
 df_base = get_base_data()
 scaler = StandardScaler()
 scaled_base = scaler.fit_transform(df_base)

 pca = PCA(n_components=3)
 pca_base = pca.fit_transform(scaled_base)

 kmeans = KMeans(n_clusters=4, random_state=42)
 clusters = kmeans.fit_predict(pca_base)

 plot_df = pd.DataFrame(pca_base, columns=['PC1', 'PC2', 'PC3'])
 plot_df['Cluster'] = clusters.astype(str)
 plot_df['Type'] = 'Kaggle Customer'

# --- STEP 2: Pull Live SQL Data ---
 conn = sqlite3.connect('data/customer_intelligence.db')
 sql_df = pd.read_sql_query("SELECT name, age, income FROM users", conn)
 conn.close()

 if not sql_df.empty:
  st.success(f"Found {len(sql_df)} Registered Users in SQL!")

# We need to make the SQL data 'look like' the Kaggle data to the AI
# We fill missing columns with averages so the math doesn't break
  for col in df_base.columns:
   if col not in sql_df.columns:
    sql_df[col] = df_base[col].mean()

# Scale and Transform the SQL user using the SAME math as the Kaggle data
  live_scaled = scaler.transform(sql_df[df_base.columns])
  live_pca = pca.transform(live_scaled)
  live_cluster = kmeans.predict(live_pca)

# Add the Live User to our plotting dataframe
  live_df = pd.DataFrame(live_pca, columns=['PC1', 'PC2', 'PC3'])
  live_df['Cluster'] = 'YOU (Live User)'
  live_df['Type'] = 'Live User'

# Combine them
  plot_df = pd.concat([plot_df, live_df])

# --- STEP 3: The 3D Plot ---
fig = px.scatter_3d(
 plot_df, x='PC1', y='PC2', z='PC3',
 color='Cluster',
 symbol='Type', # This gives our live user a different shape!
 symbol_map={'Kaggle Customer': 'circle', 'Live User': 'diamond'},
 size_max=10,
 opacity=0.7,
 title="Live Persona Mapping",
 color_discrete_map={'YOU (Live User)': 'red'} # Force live user to be RED
 )

 st.plotly_chart(fig, use_container_width=True)

except Exception as e:
 st.error(f"Error connecting data: {e}")
 st.info("Have you registered a user on the first page yet?")