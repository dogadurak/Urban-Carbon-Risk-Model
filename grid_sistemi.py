"""
04_master_grid_olustur.py
==========================
Tüm vektör ve raster katmanları 50x50m grid üzerine toplanır.

Kullanılan yöntemler:
- gpd.overlay()     → hassas geometrik kesişim (bina, yol, yeşil alan, sanayi)
- gpd.sjoin()       → nokta sayımı (otopark, trafik emisyon noktaları)
- rasterio.sample() → raster örnekleme (nüfus yoğunluğu)

Not: Yollar için uzunluk oranı hesabı yapılır.
Yani yolun sadece hücre içinde kalan kısmının skoru o hücreye atanır.
Bu "overcounting" (fazla sayma) hatasını önler.
"""

import geopandas as gpd
import pandas as pd
import numpy as np
import rasterio
import os

os.chdir(r'c:\Users\PC\Desktop\opengıs_proje_karbon_kentler\Bayrakli_Vektor_Analizi')

print("MASTER GRID OLUŞTURULUYOR...\n")

# ==========================================
# 1. TÜM DOSYALARI OKU
# ==========================================
print("1/6: Dosyalar okunuyor...")
grid           = gpd.read_file('grid_lst_ndvi_skor.geojson').to_crs(epsg=32635)
binalar        = gpd.read_file('bayrakli_binalar_hacim_c_skor.geojson').to_crs(epsg=32635)
yollar         = gpd.read_file('bayrakli_yollar_cskorli.geojson').to_crs(epsg=32635)
yesil_alanlar  = gpd.read_file('bayrakli_karbon_yutaklari_yesil_alanlar.geojson').to_crs(epsg=32635)
sanayi_ticaret = gpd.read_file('bayrakli_sanayi_ticaret.geojson').to_crs(epsg=32635)
otoparklar     = gpd.read_file('bayrakli_otoparklar.geojson').to_crs(epsg=32635)
trafik         = gpd.read_file('bayrakli_trafik_ve_emisyon_noktalari.geojson').to_crs(epsg=32635)

grid['grid_id'] = range(len(grid))
print(f"   Grid hücre sayısı: {len(grid)}")
print("✅ Dosyalar tamam\n")

# ==========================================
# 2. BİNALAR (Overlay — Hassas Kesişim)
# ==========================================
print("2/6: Binalar kesiliyor...")
bina_k   = gpd.overlay(binalar[['bina_c_skor','geometry']], grid[['grid_id','geometry']], how='intersection')
bina_sum = bina_k.groupby('grid_id')['bina_c_skor'].sum().reset_index()
bina_sum.rename(columns={'bina_c_skor': 'bina_emisyon'}, inplace=True)
print(f"   Bina skoru olan hücre: {len(bina_sum)}")
print("✅ Binalar tamam\n")

# ==========================================
# 3. YOLLAR (Overlay + Uzunluk Oranı)
# ==========================================
print("3/6: Yollar kesiliyor...")
yollar['uzunluk_tam'] = yollar.geometry.length
yol_k = gpd.overlay(
    yollar[['highway','yol_c_skor','uzunluk_tam','geometry']],
    grid[['grid_id','geometry']],
    how='intersection'
)
yol_k['uzunluk_parca'] = yol_k.geometry.length
yol_k['yol_emisyon']   = (yol_k['uzunluk_parca'] / yol_k['uzunluk_tam']) * yol_k['yol_c_skor']
yol_sum = yol_k.groupby('grid_id')['yol_emisyon'].sum().reset_index()
print(f"   Yol skoru olan hücre: {len(yol_sum)}")
print("✅ Yollar tamam\n")

# ==========================================
# 4. YEŞİL ALAN + SANAYİ (Alan m²)
# Karışık geometri tipi filtrelenir
# ==========================================
print("4/6: Yeşil alan ve sanayi hesaplanıyor...")
yesil_temiz  = yesil_alanlar[yesil_alanlar.geometry.geom_type.isin(['Polygon','MultiPolygon'])].copy()
sanayi_temiz = sanayi_ticaret[sanayi_ticaret.geometry.geom_type.isin(['Polygon','MultiPolygon'])].copy()

yesil_k = gpd.overlay(yesil_temiz[['geometry']], grid[['grid_id','geometry']], how='intersection')
yesil_k['yesil_m2'] = yesil_k.geometry.area
yesil_sum = yesil_k.groupby('grid_id')['yesil_m2'].sum().reset_index()

sanayi_k = gpd.overlay(sanayi_temiz[['geometry']], grid[['grid_id','geometry']], how='intersection')
sanayi_k['sanayi_m2'] = sanayi_k.geometry.area
sanayi_sum = sanayi_k.groupby('grid_id')['sanayi_m2'].sum().reset_index()
print("✅ Yeşil alan ve sanayi tamam\n")

# ==========================================
# 5. OTOPARK + TRAFİK (Nokta Sayımı)
# ==========================================
print("5/6: Otopark ve trafik sayılıyor...")
otopark_j   = gpd.sjoin(otoparklar[['geometry']], grid[['grid_id','geometry']], how='inner', predicate='intersects')
otopark_sum = otopark_j.groupby('grid_id').size().reset_index(name='otopark_sayisi')

trafik_j   = gpd.sjoin(trafik[['geometry']], grid[['grid_id','geometry']], how='inner', predicate='intersects')
trafik_sum = trafik_j.groupby('grid_id').size().reset_index(name='trafik_sayisi')
print(f"   Otopark olan hücre: {len(otopark_sum)}")
print(f"   Trafik noktası olan hücre: {len(trafik_sum)}")
print("✅ Otopark ve trafik tamam\n")

# ==========================================
# 6. NÜFUS RASTER (Centroid Örnekleme)
# ==========================================
print("6/6: Nüfus verisi rasterdan okunuyor...")
grid_wgs84 = grid.to_crs(epsg=4326)
centroids  = grid_wgs84.geometry.centroid
coords     = [(x, y) for x, y in zip(centroids.x, centroids.y)]

with rasterio.open('turkiye_nufus_1km.tif') as src:
    nufus = [val[0] for val in src.sample(coords)]

nufus_series  = pd.to_numeric(pd.Series(nufus), errors='coerce').fillna(0)
grid['nufus'] = nufus_series.values
grid['nufus'] = grid['nufus'].apply(lambda x: max(x, 0))
print("✅ Nüfus tamam\n")

# ==========================================
# 7. HEPSİNİ BİRLEŞTİR
# ==========================================
print("Tüm katmanlar birleştiriliyor...")
grid = grid.merge(bina_sum,    on='grid_id', how='left')
grid = grid.merge(yol_sum,     on='grid_id', how='left')
grid = grid.merge(yesil_sum,   on='grid_id', how='left')
grid = grid.merge(sanayi_sum,  on='grid_id', how='left')
grid = grid.merge(otopark_sum, on='grid_id', how='left')
grid = grid.merge(trafik_sum,  on='grid_id', how='left')

for col in ['bina_emisyon','yol_emisyon','yesil_m2','sanayi_m2','otopark_sayisi','trafik_sayisi']:
    grid[col] = grid[col].fillna(0)

grid = grid.to_crs(epsg=4326)
grid.to_file('grid_MASTER_FINAL.geojson', driver='GeoJSON')
print("\n✅ 'grid_MASTER_FINAL.geojson' kaydedildi.")
print(f"Toplam hücre: {len(grid)}")
