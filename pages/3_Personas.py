import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import plotly.express as px

st.title("👥 Module 2: AI Customer Personas")

@st.cache_data
def get_clustered_data():
 df = pd.read_csv("data/customer_data.csv", sep=None, engine='python')
 df_numeric = df.select_dtypes(include=['number']).dropna()

raw_profile = df_numeric.copy()
if 'ID' in df_numeric.columns:
 df_numeric = df_numeric.drop(columns=['ID'])

scaler = StandardScaler()
scaled = scaler.fit_transform(df_numeric)
pca = PCA(n_components=3)
pca_d = pca.fit_transform(scaled)

km = KMeans(n_clusters=4, random_state=42)
clusters = km.fit_predict(pca_d)

# Logic to name clusters based on income
raw_profile['Cluster'] = clusters
order = raw_profile.groupby('Cluster')['Income'].mean().sort_values(ascending=False).index

lbls = {order[0]: "💎 Platinum", order[1]: "👔 Professional", order[2]: "🛒 Value", order[3]: "🎓 Budget"}

pdf = pd.DataFrame(pca_d, columns=['PC1', 'PC2', 'PC3'])
pdf['Persona'] = [lbls[c] for c in clusters]
return pdf

try:
 pdf = get_clustered_data()
 fig = px.scatter_3d(pdf, x='PC1', y='PC2', z='PC3', color='Persona', title="Customer Segments")
 st.plotly_chart(fig, use_container_width=True)
except Exception as e:
 st.error(f"Error: {e}")