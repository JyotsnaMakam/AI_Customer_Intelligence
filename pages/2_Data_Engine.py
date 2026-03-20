import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

st.title("⚙️ Module 1: The Data Engine (PCA)")

@st.cache_data
@st.cache_data
def load_and_clean():
# We try reading with tab first, then comma if that fails
 try:
  df = pd.read_csv("data/customer_data.csv", sep="\t")
# If it only found 1 column, it probably failed to find the tabs
  if df.shape[1] <= 1:
   df = pd.read_csv("data/customer_data.csv", sep=",")
 except:
   st.error("Could not read the file. Check if it's in the data folder!")
   return pd.DataFrame()

# Clean the data: keep only numbers and remove empty rows
 df_numeric = df.select_dtypes(include=['number']).dropna()

# Remove 'ID' if it exists because it's not a 'math' feature
 cols_to_drop = ['ID', 'id', 'Id']
 for col in cols_to_drop:
  if col in df_numeric.columns:
    df_numeric = df_numeric.drop(columns=[col])

 return df_numeric

try:
 data = load_and_clean()
 st.write(f"### ✅ Successfully loaded {data.shape[0]} rows and {data.shape[1]} features.")

# 1. Standardization (Scaling)
 scaler = StandardScaler()
 scaled_data = scaler.fit_transform(data)

# 2. PCA Implementation
 pca = PCA(n_components=3)
 pca_results = pca.fit_transform(scaled_data)

 pca_df = pd.DataFrame(pca_results, columns=['PC1', 'PC2', 'PC3'])

 st.write("### 🚀 Principal Components (Compressed Data)")
 st.dataframe(pca_df.head())

# 3. Visualization: The Scree Plot
 st.write("### 📉 Explained Variance Ratio")
 fig, ax = plt.subplots()
 ax.bar(['PC1', 'PC2', 'PC3'], pca.explained_variance_ratio_ * 100)
 ax.set_ylabel('Percentage of Information Retained (%)')
 st.pyplot(fig)

except Exception as e:
 st.error(f"Error: {e}")
 st.info("Make sure the file is named 'customer_data.csv' in the data folder.")