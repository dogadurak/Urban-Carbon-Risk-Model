"""
03_yol_karbon_skor.py
======================
Yol ağına highway tipine göre emisyon katsayısı atanır.
Yol uzunluğu × katsayı = yol karbon skoru

Katsayı mantığı (literatür bazlı):
- primary/trunk  : 2.0  → Ana arterler, yoğun trafik
- secondary      : 1.2  → Toplayıcı yollar
- residential    : 0.5  → Mahalle içi yollar
- diğer          : 0.1  → Servis yolları, yaya yolları
"""

import geopandas as gpd
import pandas as pd

print("YOL KARBON SKORU HESAPLANIYOR...\n")

yollar = gpd.read_file('bayrakli_yollar.geojson').to_crs(epsg=32635)

print(f"Toplam yol segmenti: {len(yollar)}")
print(f"Highway tipleri:\n{yollar['highway'].value_counts().head(10)}")

# ==========================================
# 1. EMİSYON KATSAYISI ATA
# ==========================================
def katsayi_ata(highway):
    h = str(highway).lower()
    if h in ['primary', 'trunk', 'primary_link', 'trunk_link']:
        return 2.0
    elif h in ['secondary', 'tertiary', 'secondary_link', 'tertiary_link']:
        return 1.2
    elif h in ['residential', 'unclassified', 'living_street']:
        return 0.5
    else:
        return 0.1

yollar['emisyon_katsayi'] = yollar['highway'].apply(katsayi_ata)

# ==========================================
# 2. YOL UZUNLUĞU VE KARBON SKORU
# ==========================================
yollar['uzunluk_m']  = yollar.geometry.length
yollar['yol_c_skor'] = yollar['uzunluk_m'] * yollar['emisyon_katsayi']

print(f"\nYol uzunluğu — Ort: {yollar['uzunluk_m'].mean():.1f} m  Max: {yollar['uzunluk_m'].max():.1f} m")
print(f"Yol C skoru  — Ort: {yollar['yol_c_skor'].mean():.2f}  Max: {yollar['yol_c_skor'].max():.2f}")

# ==========================================
# 3. KAYDET
# ==========================================
yollar[['geometry','highway','uzunluk_m','emisyon_katsayi','yol_c_skor']].to_file(
    'bayrakli_yollar_cskorli.geojson', driver='GeoJSON')

print("\n✅ 'bayrakli_yollar_cskorli.geojson' hazır.")
