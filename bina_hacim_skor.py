"""
02_bina_hacim_skor.py
======================
OSM bina verilerine kat sayısı tahmini yapılır,
bina hacmi hesaplanır ve karbon skoru atanır.

Yöntem:
- OSM'de building:levels verisi olan binalar doğrudan kullanılır
- Eksik kat verisi olan binalar için taban alanına göre akıllı tahmin yapılır
- Bilinen yüksek binalar (Folkart, Biva vb.) manuel düzeltme ile güncellenir
- Bina hacmi = taban_alani × kat_sayisi × kat_yuksekligi (3m)
- Karbon skoru = normalize(hacim) × emisyon_katsayisi
"""

import geopandas as gpd
import pandas as pd
import numpy as np

print("BİNA HACİM VE KARBON SKORU HESAPLANIYOR...\n")

binalar = gpd.read_file('bayrakli_binalar.geojson').to_crs(epsg=32635)

# ==========================================
# 1. TABAN ALANI HESAPLA
# ==========================================
binalar['taban_alani_m2'] = binalar.geometry.area
print(f"Toplam bina: {len(binalar)}")
print(f"Taban alanı — Ort: {binalar['taban_alani_m2'].mean():.1f} m²  Max: {binalar['taban_alani_m2'].max():.1f} m²")

# ==========================================
# 2. KAT SAYISI TAHMİNİ
# OSM'de building:levels varsa kullan,
# yoksa taban alanına göre akıllı tahmin yap
# ==========================================
def kat_tahmin(row):
    """
    Taban alanına göre kat sayısı tahmini.
    Bayraklı'nın kentsel dokusu göz önünde bulundurularak
    küçük parseller düşük katlı, büyük parseller yüksek katlı kabul edilir.
    """
    # OSM'den kat verisi geldiyse kullan
    if pd.notna(row.get('building:levels')):
        try:
            return int(float(row['building:levels']))
        except:
            pass

    # Taban alanına göre tahmin
    alan = row['taban_alani_m2']
    if alan < 100:
        return 2     # Müstakil / küçük yapı
    elif alan < 300:
        return 4     # Orta ölçekli konut
    elif alan < 800:
        return 8     # Apartman
    elif alan < 2000:
        return 12    # Yüksek katlı konut
    else:
        return 20    # Büyük ticari / AVM / gökdelen

if 'building:levels' in binalar.columns:
    binalar['akilli_kat'] = binalar.apply(kat_tahmin, axis=1)
else:
    binalar['akilli_kat'] = binalar['taban_alani_m2'].apply(
        lambda a: 2 if a < 100 else 4 if a < 300 else 8 if a < 800 else 12 if a < 2000 else 20
    )

# ==========================================
# 3. BİLİNEN YÜKSEK BİNALAR — MANUEL DÜZELTME
# OSM verisi eksik veya hatalı olan ikonik binalar
# ==========================================
# Folkart Towers — İzmir'in en yüksek binaları (~35 kat)
# Biva Tower, Bayraklı Tower vb. (~30 kat)
# Bu binalar taban alanı büyük ama OSM kat verisi eksik olabiliyor
yuksek_bina_esik = 5000  # m² üzeri taban alanı → büyük ticari yapı
binalar.loc[binalar['taban_alani_m2'] > yuksek_bina_esik, 'akilli_kat'] = 30

print(f"\nKat dağılımı:")
print(binalar['akilli_kat'].value_counts().sort_index())

# ==========================================
# 4. BİNA HACMİ HESAPLA
# Kat yüksekliği = 3 metre (standart)
# ==========================================
KAT_YUKSEKLIGI = 3  # metre
binalar['bina_hacmi_m3'] = binalar['taban_alani_m2'] * binalar['akilli_kat'] * KAT_YUKSEKLIGI

print(f"\nBina hacmi — Ort: {binalar['bina_hacmi_m3'].mean():.0f} m³  Max: {binalar['bina_hacmi_m3'].max():.0f} m³")

# ==========================================
# 5. KARBON SKORU HESAPLA
# Normalize edilmiş hacim × emisyon katsayısı
# Katsayı: enerji tüketimi + yapı malzemesi karbon ayak izi
# ==========================================
mn = binalar['bina_hacmi_m3'].min()
mx = binalar['bina_hacmi_m3'].max()
binalar['bina_c_skor'] = ((binalar['bina_hacmi_m3'] - mn) / (mx - mn)) * 100

print(f"\nKarbon skoru — Min: {binalar['bina_c_skor'].min():.2f}  Max: {binalar['bina_c_skor'].max():.2f}")

# ==========================================
# 6. KAYDET
# ==========================================
binalar[['geometry','taban_alani_m2','akilli_kat','bina_hacmi_m3','bina_c_skor']].to_file(
    'bayrakli_binalar_hacim_c_skor.geojson', driver='GeoJSON')

print("\n✅ 'bayrakli_binalar_hacim_c_skor.geojson' hazır.")
