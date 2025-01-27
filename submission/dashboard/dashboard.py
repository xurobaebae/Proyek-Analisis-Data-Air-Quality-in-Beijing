import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
import os

# Load your pre-processed data
base_path = os.path.dirname(__file__)
path_shunyi = os.path.join(base_path, 'data_shunyi.csv')
path_dongsi = os.path.join(base_path, 'data_dongsi.csv')
path_guanyuan = os.path.join(base_path, 'data_guanyuan.csv')

# Load your pre-processed data using jalur absolut
data_shunyi = pd.read_csv(path_shunyi)
data_dongsi = pd.read_csv(path_dongsi)
data_guanyuan = pd.read_csv(path_guanyuan)

# Convert 'Tanggal' to datetime in individual datasets
data_shunyi['Tanggal'] = pd.to_datetime(data_shunyi[['year', 'month', 'day', 'hour']])
data_dongsi['Tanggal'] = pd.to_datetime(data_dongsi[['year', 'month', 'day', 'hour']])
data_guanyuan['Tanggal'] = pd.to_datetime(data_guanyuan[['year', 'month', 'day', 'hour']])

# Add geolocation data for each station
locations = {
    "Shunyi": [40.1277, 116.6546],
    "Dongsi": [39.9292, 116.4173],
    "Guanyuan": [39.9334, 116.3408]
}

# Combine the data into one main DataFrame and convert 'Tanggal' to datetime
main_data = pd.concat([data_shunyi, data_dongsi, data_guanyuan], keys=['Shunyi', 'Dongsi', 'Guanyuan']).reset_index(level=0).rename(columns={'level_0': 'Location'})
main_data['Tanggal'] = pd.to_datetime(main_data['Tanggal'])  # Ensure 'Tanggal' is datetime

# Set title
st.title("🌍 Dashboard Analisis Kualitas Udara di Beijing")

# Subtitle
st.subheader("📊 Menggali Data Kualitas Udara dari Tiga Lokasi: Shunyi, Dongsi, dan Guanyuan")

# Introduction
st.write("""
Selamat datang di dashboard analisis kualitas udara! 
Dalam analisis ini, kami akan menjelajahi hubungan antara curah hujan, kecepatan angin, dan kadar polutan di tiga distrik di Beijing. 
Silakan jelajahi data dan visualisasi yang kami sajikan di bawah ini.
""")

# Sidebar with user profile
with st.sidebar:
    st.image("https://avatars.githubusercontent.com/u/118404166?v=4", width=150)
    st.write("## Profil")
    st.write("Nama: **Raka Satria Efendi**")
    st.write("Email: [rakaefendi1683@gmail.com](mailto:rakaefendi1683@gmail.com)")
    st.write("ID Dicoding: **rakaefendi**")
    st.write("Github: [xurobaebae](https://github.com/xurobaebae)")
    st.write("Instagram: [raka.fx](https://instagram.com/raka.fx)")

# Fitur interaktif: Filtering berdasarkan tanggal
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Tanggal Mulai", value=data_shunyi['Tanggal'].min())
end_date = st.sidebar.date_input("Tanggal Akhir", value=data_shunyi['Tanggal'].max())
selected_station = st.sidebar.selectbox("Pilih Stasiun", options=['Shunyi', 'Dongsi', 'Guanyuan'])

# Filter data based on selections
filtered_data = main_data[(main_data['Tanggal'] >= pd.to_datetime(start_date)) & 
                          (main_data['Tanggal'] <= pd.to_datetime(end_date)) & 
                          (main_data['Location'] == selected_station)]

# Display data
st.header("Data Per Lokasi")
st.write(f"Data {selected_station}")
st.write(filtered_data.head())

# Visualize geolocation map of 3 Locations
st.header("Lokasi Shunyi, Guanyuan, dan Dongsi di Maps")
geo_map = folium.Map(location=[39.93, 116.4], zoom_start=10)

for station, coords in locations.items():
    folium.Marker(location=coords, popup=f"Stasiun: {station}").add_to(geo_map)

st_folium(geo_map, key="geo_map")

# Question 1: Hubungan antara Curah Hujan dan Jumlah Polutan
st.header("1. Hubungan antara Curah Hujan dan Jumlah Polutan")
pollutants = ['PM10', 'SO2', 'NO2']
colors = ['red', 'blue', 'green']

fig, axs = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

for i, pollutant in enumerate(pollutants):
    sns.regplot(data=filtered_data, x='RAIN', y=pollutant, scatter_kws={'alpha': 0.5}, line_kws={"color": colors[i]}, ax=axs[i])
    axs[i].set_title(f'Curah Hujan vs {pollutant}')
    axs[i].set_xlabel('Curah Hujan (mm)')
    axs[i].set_ylabel(f'{pollutant} (µg/m³)')

st.pyplot(fig)

# Question 2: Korelasi antara Kecepatan Angin dan Polutan
st.header("2. Korelasi antara Kecepatan Angin dan Polutan")

fig2, axs2 = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

for i, pollutant in enumerate(pollutants):
    sns.regplot(data=filtered_data, x='WSPM', y=pollutant, scatter_kws={'alpha': 0.5}, line_kws={"color": colors[i]}, ax=axs2[i])
    axs2[i].set_title(f'Kecepatan Angin vs {pollutant}')
    axs2[i].set_xlabel('Kecepatan Angin (m/s)')
    axs2[i].set_ylabel(f'{pollutant} (µg/m³)')

st.pyplot(fig2)

# Question 3: Tren Curah Hujan Bulanan
st.header("3. Tren Curah Hujan Bulanan")

monthly_rain_filtered = filtered_data.groupby(filtered_data['Tanggal'].dt.to_period('M')).agg({'RAIN': 'sum'}).reset_index()

plt.figure(figsize=(12, 6))
plt.plot(monthly_rain_filtered['Tanggal'].dt.to_timestamp(), monthly_rain_filtered['RAIN'], marker='o', color='red', label=selected_station)
plt.title('Tren Curah Hujan Bulanan')
plt.xlabel('Tanggal')
plt.ylabel('Curah Hujan (mm)')
plt.legend()
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(plt)

# Display conclusion in a separate column
st.header("Kesimpulan Analisis")
st.write("""
Dalam analisis ini, kita telah melakukan data gathering mulai dari data curah hujan, kecepatan angin, dan kadar polutan di Distrik Shunyi, Guanyuan, dan Dongsi. Kemudian, kita melakukan analisis terhadap data tersebut untuk menjawab tiga pertanyaan yang diajukan.

- **Curah Hujan dan Polutan**: Hubungan signifikan di Shunyi dan Dongsi, namun tidak di Guanyuan.
- **Kecepatan Angin dan Polutan**: Korelasi signifikan di Shunyi dan Dongsi, namun tidak di Guanyuan.
- **Tren Curah Hujan Bulanan**: Tren meningkat di Shunyi dan Dongsi, tidak signifikan di Guanyuan.

Secara keseluruhan, Shunyi memiliki kualitas udara paling buruk dibandingkan dengan Dongsi dan Guanyuan.
""")

# Footer with copyright
st.markdown("---")
st.markdown("© 2025 Raka Satria Efendi")
