"""
05_karbon_risk_indeks.py
=========================
AHP tabanlı hiyerarşik karbon risk indeksi hesaplanır.

Sorun: LST verisi tüm Bayraklı'da yüksek olduğu için
tek formüllü modelde LST diğer kriterleri baskılıyordu.

Çözüm: Hiyerarşik alt-indeks yöntemi
"Karbon kaynaklarını tematik olarak ayırarak,
 iklimsel verilerin (LST) insan kaynaklı emisyon
 verilerini istatistiksel olarak baskılaması engellenmiştir."

3 Alt İndeks:
  1. Ulaşım Emisyon İndeksi  → %40
  2. Yapısal Emisyon İndeksi → %40
  3. Kentsel Mikroklima       → %20

AHP Ağırlıkları (Bayraklı kentsel kimliği + literatür):
  n_yol     0.25 — Altınyol transit etkisi
  n_bina    0.20 — Yüksek katlı yapılaşma
  n_LST     0.20 — Isı adası riski
  n_trafik  0.15 — Emisyon yoğunluğu
  n_sanayi  0.08 — Dönüşüm bölgesi sanayisi
  n_nufus   0.07 — Maruziyet çarpanı
  n_otopark 0.05 — Rölanti emisyonu
  n_NDVI   -0.15 — Karbon yutağı (negatif)
"""

import geopandas as gpd
import pandas as pd
import numpy as np
import os

os.chdir(r'c:\Users\PC\Desktop\opengıs_proje_karbon_kentler\Bayrakli_Vektor_Analizi')

grid = gpd.read_file('grid_MASTER_FINAL.geojson').to_crs(epsg=32635)

# ==========================================
# 1. NORMALİZASYON (Min-Max, 0-1 arası)
# ==========================================
def normalize(series):
    mn, mx = series.min(), series.max()
    if mx == mn:
        return pd.Series([0.0] * len(series), index=series.index)
    return (series - mn) / (mx - mn)

grid['n_bina']    = normalize(grid['bina_emisyon'])
grid['n_yol']     = normalize(grid['yol_emisyon'])
grid['n_sanayi']  = normalize(grid['sanayi_m2'])
grid['n_trafik']  = normalize(grid['trafik_sayisi'])
grid['n_otopark'] = normalize(grid['otopark_sayisi'])
grid['n_nufus']   = normalize(grid['nufus'])
grid['n_LST']     = normalize(grid['LST_mean'])
grid['n_NDVI']    = normalize(grid['NDVI_mean'])

# ==========================================
# 2. ALT İNDEKS 1: ULAŞIM EMİSYON İNDEKSİ
# ==========================================
grid['ulasim_ham']    = grid['n_yol']*0.60 + grid['n_trafik']*0.25 + grid['n_otopark']*0.15
grid['ulasim_indeks'] = normalize(grid['ulasim_ham']) * 100

# ==========================================
# 3. ALT İNDEKS 2: YAPISAL EMİSYON İNDEKSİ
# Bina maskesi: bina olmayan hücrelerde yapısal indeks = 0
# Düşük çözünürlüklü nüfus gridinin boş alanlarda
# yapay yoğunluk üretmesini engeller (built-up mask)
# ==========================================
grid['yapi_ham']          = grid['n_bina']*0.55 + grid['n_nufus']*0.30 + grid['n_sanayi']*0.15
grid['yapi_ham_norm']     = normalize(grid['yapi_ham']) * 100
grid['yapi_indeks']       = np.where(grid['n_bina'] == 0, 0, grid['yapi_ham_norm'])

# ==========================================
# 4. ALT İNDEKS 3: KENTSEL MİKROKLİMA İNDEKSİ
# LST riski artırır, NDVI azaltır
# ==========================================
grid['mikroklima_ham']    = (grid['n_LST']*0.70 - grid['n_NDVI']*0.30).clip(lower=0)
grid['mikroklima_indeks'] = normalize(grid['mikroklima_ham']) * 100

# ==========================================
# 5. FİNAL KARBON RİSK SKORU (0-100)
# ==========================================
grid['karbon_risk_v2'] = (
      grid['ulasim_indeks']     * 0.40
    + grid['yapi_indeks']       * 0.40
    + grid['mikroklima_indeks'] * 0.20
)
grid['karbon_risk_v2'] = normalize(grid['karbon_risk_v2']) * 100

print("📊 KARBON RİSK SKORU SONUÇLARI")
print("-" * 40)
risk = grid['karbon_risk_v2']
print(f"Min: {risk.min():.1f}  Max: {risk.max():.1f}  Ort: {risk.mean():.1f}  Std: {risk.std():.1f}")
print(f"Dusuk  (0-33) : {((risk>=0)&(risk<33)).sum():5d} hucre (%{((risk>=0)&(risk<33)).sum()/len(grid)*100:.1f})")
print(f"Orta  (33-66) : {((risk>=33)&(risk<66)).sum():5d} hucre (%{((risk>=33)&(risk<66)).sum()/len(grid)*100:.1f})")
print(f"Yuksek(66-100): {(risk>=66).sum():5d} hucre (%{(risk>=66).sum()/len(grid)*100:.1f})")

grid = grid.to_crs(epsg=4326)
grid.to_file('grid_MASTER_FINAL.geojson', driver='GeoJSON')
print("\n✅ 'grid_MASTER_FINAL.geojson' guncellendi.")
