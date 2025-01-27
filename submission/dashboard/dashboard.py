import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

# Load your pre-processed data
data_shunyi = pd.read_csv('./data_shunyi.csv')
data_dongsi = pd.read_csv('./data_dongsi.csv')
data_guanyuan = pd.read_csv('./data_guanyuan.csv')

# Add geolocation data for each station
locations = {
    "Shunyi": [40.1277, 116.6546],
    "Dongsi": [39.9292, 116.4173],
    "Guanyuan": [39.9334, 116.3408]
}

# Combine the data into one main DataFrame
main_data = pd.concat([data_shunyi, data_dongsi, data_guanyuan], keys=['Shunyi', 'Dongsi', 'Guanyuan']).reset_index(level=0).rename(columns={'level_0': 'Location'})

# Convert 'Tanggal' to datetime
data_shunyi['Tanggal'] = pd.to_datetime(data_shunyi[['year', 'month', 'day', 'hour']])
data_dongsi['Tanggal'] = pd.to_datetime(data_dongsi[['year', 'month', 'day', 'hour']])
data_guanyuan['Tanggal'] = pd.to_datetime(data_guanyuan[['year', 'month', 'day', 'hour']])

# Set title
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

# Display data
st.header("Data Per Lokasi")
st.write("Data Shunyi")
st.write(data_shunyi.head())
st.write("Data Dongsi")
st.write(data_dongsi.head())
st.write("Data Guanyuan")
st.write(data_guanyuan.head())
st.write("Data Keseluruhan")
st.write(main_data.head())

# Visualize geolocation map of 3 Locations
st.header("Lokasi Shunyi, Guanyuan, dan Dongsi di Maps")
customer_data = pd.DataFrame({
    "Latitude": [40.1277, 39.9292, 39.9334],
    "Longitude": [116.6546, 116.4173, 116.3408],
    "Station": ["Shunyi", "Dongsi", "Guanyuan"],
    "Count": [500, 1200, 800]  # Example customer counts
})

# Create map for customer geolocation
geo_map = folium.Map(location=[39.93, 116.4], zoom_start=10)

for _, row in customer_data.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=row['Count'] / 100,  # Scale marker size
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.6,
        popup=f"Station: {row['Station']}\n:Count {row['Count']}"
    ).add_to(geo_map)

st_folium(geo_map, key="geo_map")


# Question 1: Hubungan antara Curah Hujan dan Jumlah Polutan
st.header("1. Hubungan antara Curah Hujan dan Jumlah Polutan")
pollutants = ['PM10', 'SO2', 'NO2']
colors = ['red', 'blue', 'green']

fig, axs = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

for i, pollutant in enumerate(pollutants):
    for data, color, label in zip([data_shunyi, data_dongsi, data_guanyuan], colors, ['Shunyi', 'Dongsi', 'Guanyuan']):
        sns.regplot(data=data, x='RAIN', y=pollutant, scatter_kws={'alpha': 0.5}, line_kws={"color": color}, ax=axs[i], label=label)
    axs[i].set_title(f'Curah Hujan vs {pollutant}')
    axs[i].set_xlabel('Curah Hujan (mm)')
    axs[i].set_ylabel(f'{pollutant} (µg/m³)')
    axs[i].legend()

st.pyplot(fig)

# Question 2: Korelasi antara Kecepatan Angin dan Polutan
st.header("2. Korelasi antara Kecepatan Angin dan Polutan")

fig2, axs2 = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

for i, pollutant in enumerate(pollutants):
    for data, color, label in zip([data_shunyi, data_dongsi, data_guanyuan], colors, ['Shunyi', 'Dongsi', 'Guanyuan']):
        sns.regplot(data=data, x='WSPM', y=pollutant, scatter_kws={'alpha': 0.5}, line_kws={"color": color}, ax=axs2[i], label=label)
    axs2[i].set_title(f'Kecepatan Angin vs {pollutant}')
    axs2[i].set_xlabel('Kecepatan Angin (m/s)')
    axs2[i].set_ylabel(f'{pollutant} (µg/m³)')
    axs2[i].legend()

st.pyplot(fig2)

# Question 3: Tren Curah Hujan Bulanan
st.header("3. Tren Curah Hujan Bulanan")

monthly_rain_shunyi = data_shunyi.groupby(data_shunyi['Tanggal'].dt.to_period('M')).agg({'RAIN': 'sum'}).reset_index()
monthly_rain_dongsi = data_dongsi.groupby(data_dongsi['Tanggal'].dt.to_period('M')).agg({'RAIN': 'sum'}).reset_index()
monthly_rain_guanyuan = data_guanyuan.groupby(data_guanyuan['Tanggal'].dt.to_period('M')).agg({'RAIN': 'sum'}).reset_index()

plt.figure(figsize=(12, 6))
plt.plot(monthly_rain_shunyi['Tanggal'].dt.to_timestamp(), monthly_rain_shunyi['RAIN'], marker='o', color='red', label='Shunyi')
plt.plot(monthly_rain_dongsi['Tanggal'].dt.to_timestamp(), monthly_rain_dongsi['RAIN'], marker='o', color='blue', label='Dongsi')
plt.plot(monthly_rain_guanyuan['Tanggal'].dt.to_timestamp(), monthly_rain_guanyuan['RAIN'], marker='o', color='green', label='Guanyuan')
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
