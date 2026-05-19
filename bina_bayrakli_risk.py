"""
06_bina_bazli_risk.py
======================
Grid bazlı karbon risk skorları bina geometrilerine transfer edilir.
Binaya tıklandığında o binanın karbon risk skoru görülebilir.

Formül:
  bina_risk = bina_normalize × 0.40
            + ulasim_indeks  × 0.40
            + mikroklima     × 0.20

Mantık:
  Binanın kendi hacim/emisyon skoru (%40) +
  Bulunduğu hücrenin ulaşım yükü (%40) +
  Bulunduğu hücrenin ısı adası etkisi (%20)
"""

import geopandas as gpd
import pandas as pd
import numpy as np
import os

os.chdir(r'c:\Users\PC\Desktop\opengıs_proje_karbon_kentler\Bayrakli_Vektor_Analizi')

print("BİNA BAZLI KARBON RİSK HESAPLANIYOR...\n")

binalar = gpd.read_file('bayrakli_binalar_hacim_c_skor.geojson').to_crs(epsg=32635)
grid    = gpd.read_file('grid_MASTER_FINAL.geojson').to_crs(epsg=32635)

# Bina karbon skorunu 0-100 arası normalize et
mn, mx = binalar['bina_c_skor'].min(), binalar['bina_c_skor'].max()
binalar['bina_normalize'] = ((binalar['bina_c_skor'] - mn) / (mx - mn)) * 100

# Grid'den gerekli sütunları al
grid_cols = grid[['ulasim_indeks','yapi_indeks','mikroklima_indeks','karbon_risk_v2','geometry']]

# Spatial join: her binayı düştüğü grid hücresiyle eşleştir
print("Binalar grid ile eslestiriliyor...")
binalar_gridli = gpd.sjoin(binalar, grid_cols, how='left', predicate='intersects')
binalar_gridli = binalar_gridli[~binalar_gridli.index.duplicated(keep='first')]

for col in ['ulasim_indeks','yapi_indeks','mikroklima_indeks','karbon_risk_v2']:
    binalar_gridli[col] = binalar_gridli[col].fillna(0)

# Bina bazlı nihai risk skoru
binalar_gridli['bina_risk'] = (
      binalar_gridli['bina_normalize']    * 0.40
    + binalar_gridli['ulasim_indeks']     * 0.40
    + binalar_gridli['mikroklima_indeks'] * 0.20
)

# 0-100 arası normalize et
mn2, mx2 = binalar_gridli['bina_risk'].min(), binalar_gridli['bina_risk'].max()
binalar_gridli['bina_risk'] = ((binalar_gridli['bina_risk'] - mn2) / (mx2 - mn2)) * 100

print("📊 BİNA RİSK SONUÇLARI")
print("-" * 40)
print(f"Toplam bina    : {len(binalar_gridli)}")
print(f"Risk ort       : {binalar_gridli['bina_risk'].mean():.1f}")
print(f"Risk max       : {binalar_gridli['bina_risk'].max():.1f}")
print(f"Dusuk  (0-33)  : {((binalar_gridli['bina_risk']>=0)&(binalar_gridli['bina_risk']<33)).sum()} bina")
print(f"Orta  (33-66)  : {((binalar_gridli['bina_risk']>=33)&(binalar_gridli['bina_risk']<66)).sum()} bina")
print(f"Yuksek(66-100) : {(binalar_gridli['bina_risk']>=66).sum()} bina")

binalar_gridli.to_file('binalar_NIHAI_RISK.geojson', driver='GeoJSON')
print("\n✅ 'binalar_NIHAI_RISK.geojson' hazir!")
print("QGIS'te 'bina_risk' sutununu graduated ile renklendir.")
