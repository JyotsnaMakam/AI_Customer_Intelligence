import streamlit as st
import pandas as pd
import sqlite3
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import plotly.express as px

st.title("👥 Module 2: AI Customer Personas")

@st.cache_data
def get_clustered_data():
# 1. Load the same data as before
 df = pd.read_csv("data/customer_data.csv", sep=None, engine='python')
 df_numeric = df.select_dtypes(include=['number']).dropna()
 if 'ID' in df_numeric.columns:
  df_numeric = df_numeric.drop(columns=['ID'])

# 2. PCA Compression (the part you just mastered!)
 scaler = StandardScaler()
 scaled_data = scaler.fit_transform(df_numeric)
 pca = PCA(n_components=3)
 pca_data = pca.fit_transform(scaled_data)

# 3. K-Means Clustering (Finding the "Groups")
# We will ask the AI to find 4 distinct groups of customers
 kmeans = KMeans(n_clusters=4, random_state=42)
 clusters = kmeans.fit_predict(pca_data)

# Create a DataFrame for plotting
 plot_df = pd.DataFrame(pca_data, columns=['PC1', 'PC2', 'PC3'])
 plot_df['Cluster'] = clusters.astype(str) # Labels for the groups
 return plot_df

try:
 chart_data = get_clustered_data()

 st.write("### 🌐 3D Persona Visualization")
 st.write("Each dot is a customer. The colors represent different AI-identified segments.")

# Create a beautiful 3D scatter plot
 fig = px.scatter_3d(
  chart_data, x='PC1', y='PC2', z='PC3',
  color='Cluster',
  title="Customer Clusters in Reduced Space",
  opacity=0.7,
  color_discrete_sequence=px.colors.qualitative.Vivid
)

 st.plotly_chart(fig, use_container_width=True)

 st.info("💡 **Discovery:** Notice how the dots of the same color stay together? Those are customers with similar lifestyles and spending habits!")
except Exception as e:
 st.error(f"An error occurred: {e}")