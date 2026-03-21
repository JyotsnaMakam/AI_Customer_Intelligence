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
# 1. Load and Clean
 df = pd.read_csv("data/customer_data.csv", sep=None, engine='python')
 df_numeric = df.select_dtypes(include=['number']).dropna()

# Keep Income for profiling before dropping columns for PCA
 raw_for_profile = df_numeric.copy()

 if 'ID' in df_numeric.columns:
  df_numeric = df_numeric.drop(columns=['ID'])

# 2. PCA & Clustering
 scaler = StandardScaler()
 scaled_data = scaler.fit_transform(df_numeric)
 pca = PCA(n_components=3)
 pca_data = pca.fit_transform(scaled_data)

 kmeans = KMeans(n_clusters=4, random_state=42)
 clusters = kmeans.fit_predict(pca_data)

# 3. Naming the Clusters (Profiling)
 raw_for_profile['Cluster'] = clusters
 cluster_means = raw_for_profile.groupby('Cluster')['Income'].mean()

# Map cluster numbers to descriptive names based on average income
# (This is a simplified way to name them automatically)
 sorted_clusters = cluster_means.sort_values(ascending=False).index
 names = {
  sorted_clusters[0]: "💎 Platinum Elites",
  sorted_clusters[1]: "👔 Professional Class",
  sorted_clusters[2]: "🛒 Value Seekers",
  sorted_clusters[3]: "🎓 Budget Students/Young"
 }

 plot_df = pd.DataFrame(pca_data, columns=['PC1', 'PC2', 'PC3'])
 plot_df['Cluster_Name'] = [names[c] for c in clusters]
 return plot_df, names

try:
 plot_df, cluster_names = get_clustered_data()

 st.write("### 🌐 3D Persona Visualization")

 fig = px.scatter_3d(
 plot_df, x='PC1', y='PC2', z='PC3',
  color='Cluster_Name',
  title="AI-Generated Customer Segments",
  color_discrete_sequence=px.colors.qualitative.Safe
)
 st.plotly_chart(fig, use_container_width=True)

# --- THE LEGEND / EXPLANATION ---
 st.write("### 📝 What do these colors mean?")
 col1, col2 = st.columns(2)

with col1:
 st.markdown(f"**{cluster_names[0]}**")
 st.caption("High income, high spending on luxury goods like Wine and Meat.")
 st.markdown(f"**{cluster_names[1]}**")
 st.caption("Steady income, moderate spending across all categories.")

with col2:
 st.markdown(f"**{cluster_names[2]}**")
 st.caption("Price sensitive, looking for deals and discounts.")
 st.markdown(f"**{cluster_names[3]}**")
 st.caption("Lower income, likely younger or smaller households.")

except Exception as e:
 st.error(f"Error: {e}")