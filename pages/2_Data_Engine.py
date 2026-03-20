import streamlit as st
import pandas as pd
import sqlite3
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

st.title("⚙️ The Data Engine: PCA & SVD")

# 1. Load the Kaggle Data
@st.cache_data # This keeps the app fast
def load_kaggle_data():
# Make sure your file name matches exactly!
df = pd.read_csv("data/customer_data.csv", sep="\t")
return df

try:
df_kaggle = load_kaggle_data()
st.write("### 📊 Raw Kaggle Data (Preview)")
st.dataframe(df_kaggle.head())

# 2. Pre-processing: We only take numerical columns for PCA
# We drop columns with missing values for now to keep the math clean
data_numeric = df_kaggle.select_dtypes(include=['float64', 'int64']).dropna()

st.write(f"Processing **{data_numeric.shape[1]}** numerical columns into 3 Components...")

# 3. Standardization (Scaling)
# PCA is sensitive to scales (Income vs Age). We must scale them first!
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data_numeric)

# 4. PCA Implementation
pca = PCA(n_components=3)
pca_data = pca.fit_transform(scaled_data)

# Create a DataFrame for the results
pca_df = pd.DataFrame(data=pca_data, columns=['PC1', 'PC2', 'PC3'])

st.write("### ✨ PCA Transformation Result")
st.write("These 3 columns now represent the 'essence' of the original 20+ columns.")
st.dataframe(pca_df.head())

# 5. The Scree Plot (The Proof)
st.write("### 📉 Explained Variance (The Math)")
fig, ax = plt.subplots()
ax.bar(['PC1', 'PC2', 'PC3'], pca.explained_variance_ratio_)
ax.set_ylabel('Variance Ratio')
st.pyplot(fig)
st.info("The first bar (PC1) usually captures the most important patterns in the data!")

except FileNotFoundError:
st.error("Missing 'customer_data.csv' in the data folder. Please upload it to continue.")