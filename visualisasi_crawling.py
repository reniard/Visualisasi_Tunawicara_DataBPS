import streamlit as st
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt

# Koneksi MongoDB - langsung dari URI
uri = "mongodb+srv://dewi85280:biartuhansaja@selvoi.w5zmt4f.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)
db = client['visualisasi']
collection = db['disabilitas_tunarungu']

# Ambil data
data = list(collection.find())
df = pd.DataFrame(data)

# Filter kolom yang dibutuhkan
df_filtered = df[['Regency/Municipality', 'Tuna Wicara']]
df_filtered = df_filtered.dropna(subset=['Tuna Wicara'])
df_filtered['Tuna Wicara'] = pd.to_numeric(df_filtered['Tuna Wicara'], errors='coerce').fillna(0).astype(int)

# Tampilan di Streamlit
st.title("Visualisasi Data Penyandang Tuna Wicara per Kabupaten/Kota")

st.subheader("Data Tabel")
st.dataframe(df_filtered)

st.subheader("Bar Chart Tuna Wicara")
st.bar_chart(df_filtered.set_index('Regency/Municipality')['Tuna Wicara'])

st.subheader("Pie Chart Proporsi Tuna Wicara")
fig1, ax1 = plt.subplots()
ax1.pie(df_filtered['Tuna Wicara'], labels=df_filtered['Regency/Municipality'], autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

st.subheader("Line Chart Tuna Wicara")
st.line_chart(df_filtered.set_index('Regency/Municipality')['Tuna Wicara'])
