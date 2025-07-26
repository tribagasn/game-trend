# import time
# from pytrends.request import TrendReq
# import pandas as pd

# # Inisialisasi pytrends
# pytrends = TrendReq(hl='id-ID', tz=360, requests_args={'headers': {'User-Agent': 'Mozilla/5.0'}})

# # Keyword asli dan alternatif
# keywords_mapping = {
#     'Mobile Legends': ['Mobile Legends'],
#     'PUBG Mobile': ['PUBG Mobile', 'PUBG'],
#     'Resident Evil Village': ['Resident Evil Village', 'Resident Evil']
# }

# # Data akhir
# all_data = pd.DataFrame()

# # Looping setiap keyword
# for original_keyword, alternatives in keywords_mapping.items():
#     success = False
#     for kw in alternatives:
#         for timeframe in ['today 3-m', 'today 12-m']:  # Coba 3 bulan lalu 12 bulan
#             try:
#                 pytrends.build_payload([kw], timeframe=timeframe, geo='ID')
#                 df = pytrends.interest_over_time()
#                 if not df.empty:
#                     all_data[original_keyword] = df[kw]
#                     print(f"✅ Berhasil ambil data: '{kw}' sebagai pengganti '{original_keyword}' (timeframe: {timeframe})")
#                     success = True
#                     break
#             except Exception as e:
#                 print(f"⚠️ Gagal ambil data: '{kw}' (timeframe: {timeframe}) - {e}")
#         if success:
#             break
#         time.sleep(10)  # Jeda untuk menghindari blokir

#     if not success:
#         print(f"❌ Semua percobaan gagal untuk: '{original_keyword}'")

# # Simpan jika ada data
# if not all_data.empty:
#     all_data.to_csv("trend_game_data.csv")
#     print("📁 Sukses simpan: trend_game_data.csv")
# else:
#     print("🚫 Semua data kosong, tidak ada file disimpan.")

