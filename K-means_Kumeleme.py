import geopandas as gpd
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

print("GERÇEKÇİ K-MEANS MODELİ BAŞLATILIYOR (SADECE KENTSEL ALAN)...\n")

# 1. Veriyi Oku (Orijinal dosyanı okuyoruz)
grid = gpd.read_file('grid_MASTER_FINAL.geojson')

# ==========================================
# 2. ŞEHRİ DAĞLARDAN AYIRMA (Urban Masking)
# İçinde BİNA veya YOL olan hücreleri "Kentsel Alan" kabul et
# ==========================================
kent_maskesi = (grid['n_bina'] > 0) | (grid['n_yol'] > 0)

kent_grid = grid[kent_maskesi].copy() # Makinenin inceleyeceği asıl şehir
doga_grid = grid[~kent_maskesi].copy() # İçi boş olan dağlar/tepeler

print(f"Toplam Hücre: {len(grid)}")
print(f"🏢 Kentsel (Analiz Edilecek) Hücre: {len(kent_grid)}")
print(f"🌲 Doğal/Boş Hücre (Devre Dışı Bırakılan): {len(doga_grid)}\n")

# ==========================================
# 3. SADECE KENTSEL ALANI KÜMELE
# ==========================================
ozellikler = ['n_bina', 'n_yol', 'n_LST', 'n_NDVI', 'n_trafik', 'n_sanayi', 'n_nufus', 'n_otopark']
df_kent = kent_grid[ozellikler].fillna(0)

# Standardizasyon
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_kent)

# Kentsel alan için ideal olan 5 farklı kentsel karakter belirleyelim
k = 5
km = KMeans(n_clusters=k, random_state=42, n_init=10)
kent_grid['kume'] = km.fit_predict(df_scaled)

# ==========================================
# 4. KENTSEL ETİKETLERİ RİSKE GÖRE SIRALA VE İSİMLENDİR
# ==========================================
profil = kent_grid.groupby('kume')['karbon_risk_v2'].mean()
risk_sirali = profil.sort_values()

# Şehrin gerçeklerine uygun yeni etiketler
isimler = [
    'Düşük Riskli Konutlar (Yeşili Bol)', 
    'Orta Riskli Standart Mahalleler', 
    'Kentsel Isı Adaları ve Yoğun Dokular', 
    'Ticari Akslar ve Kuleler Bölgesi', 
    'Ekstrem Emisyon Damarı (Ana Arterler)'
]
etiketler = {kume_id: isimler[i] for i, (kume_id, _) in enumerate(risk_sirali.items())}
kent_grid['kume_etiket'] = kent_grid['kume'].map(etiketler)

# ==========================================
# 5. DOĞAL ALANLARI SİSTEME GERİ EKLE
# ==========================================
doga_grid['kume'] = -1
doga_grid['kume_etiket'] = 'Doğal / Yapılaşmamış Alan'

# İşlenmiş şehir verisiyle, ayrılan doğal alanları tekrar birleştir
grid_final = pd.concat([kent_grid, doga_grid], ignore_index=True)
grid_final = gpd.GeoDataFrame(grid_final, geometry='geometry', crs=grid.crs)

# ==========================================
# 6. KAYDET
# ==========================================
dosya_adi = 'grid_KMEANS_GERCEKCI.geojson'
grid_final.to_file(dosya_adi, driver='GeoJSON')
print(f"\n✅ Tamamlandı! Gerçekçi model '{dosya_adi}' olarak kaydedildi.")
