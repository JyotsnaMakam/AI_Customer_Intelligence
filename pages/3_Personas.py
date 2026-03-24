import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import plotly.express as px

st.title("👥 Module 2: AI Customer Personas")

@st.cache_data
def get_clustered_data():
    # Load and auto-detect separator
    df = pd.read_csv("data/customer_data.csv", sep=None, engine='python')
    df_numeric = df.select_dtypes(include=['number']).dropna()
    
    # Save copy for naming groups later
    raw_data = df_numeric.copy()
    
    if 'ID' in df_numeric.columns:
        df_numeric = df_numeric.drop(columns=['ID'])

    # Standardize and Compress (PCA)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df_numeric)
    pca = PCA(n_components=3)
    pca_results = pca.fit_transform(scaled)
    
    # Grouping (K-Means)
    kmeans = KMeans(n_clusters=4, random_state=42)
    clusters = kmeans.fit_predict(pca_results)
    
    # Naming Logic based on Income
    raw_data['Cluster'] = clusters
    avg_income = raw_data.groupby('Cluster')['Income'].mean().sort_values(ascending=False).index
    
    # Map the group numbers to meaningful names
    names = {
        avg_income[0]: "💎 Platinum Elites",
        avg_income[1]: "👔 Professionals",
        avg_income[2]: "🛒 Value Seekers",
        avg_income[3]: "🎓 Budget Students"
    }
    
    # Create the final table for the 3D Plot
    pdf = pd.DataFrame(pca_results, columns=['PC1', 'PC2', 'PC3'])
    pdf['Persona'] = [names[c] for c in clusters]
    return pdf

try:
    final_df = get_clustered_data()

    # Create the 3D Chart
    fig = px.scatter_3d(
        final_df, x='PC1', y='PC2', z='PC3',
        color='Persona',
        title="AI Customer Segments",
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.success("Successfully generated 3D Persona Clusters!")

except Exception as e:
    st.error(f"Something went wrong: {e}")