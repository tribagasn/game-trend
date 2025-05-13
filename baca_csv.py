import pandas as pd
import matplotlib.pyplot as plt

# Membaca file CSV tren game
df = pd.read_csv('trend_game_data.csv')

# Menampilkan 5 baris pertama data
print(df.head())

# Plot data tren
plt.figure(figsize=(10, 6))

# Plot setiap game dengan tanggal sebagai sumbu x
plt.plot(df['date'], df['Mobile Legends'], label='Mobile Legends', marker='o')
plt.plot(df['date'], df['PUBG Mobile'], label='PUBG Mobile', marker='o')
plt.plot(df['date'], df['Resident Evil Village'], label='Resident Evil Village', marker='o')

# Memberikan label pada sumbu X dan Y
plt.xlabel('Tanggal')
plt.ylabel('Tingkat Kepopuleran')

# Memberikan judul grafik
plt.title('Tren Game (3 Bulan Terakhir)')

# Menampilkan legend untuk membedakan setiap garis
plt.legend()

# Rotasi sumbu X (tanggal) agar lebih mudah dibaca
plt.xticks(rotation=45)

# Tampilkan grafik
plt.tight_layout()
plt.show()
