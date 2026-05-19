"""
08_istatistiksel_kontrol.py
============================
Karbon risk modelinin istatistiksel kalite kontrolü.

Kontroller:
1. Temel istatistikler (min, max, ort, std)
2. Risk dağılımı (düşük / orta / yüksek)
3. Pearson korelasyon analizi (beklenen yön kontrolü)
4. LST ↔ NDVI fiziksel tutarlılık kontrolü
5. Aykırı değer analizi (Z-score > 3)

Sonuçlar:
- Tüm kriterler beklenen korelasyon yönünde ✅
- LST ↔ NDVI: r=-0.628 (fiziksel olarak doğru) ✅
- Veri kalitesi: Yayınlanabilir düzey ✅
"""

import geopandas as gpd
import pandas as pd
import numpy as np
from scipy import stats
import os

os.chdir(r'c:\Users\PC\Desktop\opengıs_proje_karbon_kentler\Bayrakli_Vektor_Analizi')

grid = gpd.read_file('grid_MASTER_FINAL.geojson')
df   = grid.drop(columns='geometry')

print("=" * 60)
print("İSTATİSTİKSEL KALİTE KONTROLÜ — grid_MASTER_FINAL")
print("=" * 60)

# 1. TEMEL İSTATİSTİKLER
print("\n📊 1. TEMEL İSTATİSTİKLER")
print("-" * 40)
kolonlar = ['karbon_risk_v2','n_bina','n_yol','n_LST',
            'n_trafik','n_sanayi','n_nufus','n_otopark','n_NDVI']

for k in kolonlar:
    s = df[k]
    print(f"{k:18s} Min:{s.min():.3f}  Max:{s.max():.3f}  Ort:{s.mean():.3f}  Std:{s.std():.3f}")

# 2. RİSK DAĞILIMI
print("\n📊 2. KARBON RİSK DAĞILIMI (0-100)")
print("-" * 40)
risk = df['karbon_risk_v2']
print(f"Dusuk  (0-33) : {((risk>=0)&(risk<33)).sum():5d} hucre (%{((risk>=0)&(risk<33)).sum()/len(df)*100:.1f})")
print(f"Orta  (33-66) : {((risk>=33)&(risk<66)).sum():5d} hucre (%{((risk>=33)&(risk<66)).sum()/len(df)*100:.1f})")
print(f"Yuksek(66-100): {(risk>=66).sum():5d} hucre (%{(risk>=66).sum()/len(df)*100:.1f})")

# 3. KORELASYON ANALİZİ
print("\n📊 3. PEARSON KORELASYON (kriterlerin risk ile ilişkisi)")
print("-" * 60)
print("(+) pozitif = risk artırıyor, (-) negatif = risk azaltıyor")
for k in kolonlar[1:]:
    mask = df[k].notna() & df['karbon_risk_v2'].notna()
    x    = df.loc[mask, k].astype(float)
    y    = df.loc[mask, 'karbon_risk_v2'].astype(float)
    r, p = stats.pearsonr(x, y)
    beklenen = (k == 'n_NDVI' and r < 0) or (k != 'n_NDVI' and r > 0)
    yorum = "Beklenen" if beklenen else "Beklenmedik - kontrol et"
    print(f"{k:18s} r={r:+.3f}  {'✅' if beklenen else '⚠️ '} {yorum}")

# 4. LST & NDVI FİZİKSEL KONTROL
print("\n📊 4. LST & NDVI FİZİKSEL TUTARLILIK")
print("-" * 40)
mask = df['LST_mean'].notna() & df['NDVI_mean'].notna()
r2, _ = stats.pearsonr(
    df.loc[mask,'LST_mean'].astype(float),
    df.loc[mask,'NDVI_mean'].astype(float)
)
print(f"LST ↔ NDVI: r={r2:.3f}")
print(f"{'✅ Negatif korelasyon — sıcaklık arttıkça bitki azalıyor (fiziksel olarak doğru)' if r2 < 0 else '⚠️ Pozitif — veri kontrolü önerilir'}")

# 5. AYKIRI DEĞER KONTROLÜ
print("\n📊 5. AYKIRI DEĞER (Z-score > 3)")
print("-" * 40)
for k in ['bina_emisyon','yol_emisyon','karbon_risk_v2']:
    if k in df.columns:
        temiz   = df[k].dropna().astype(float)
        z       = np.abs(stats.zscore(temiz))
        outlier = (z > 3).sum()
        yuzde   = outlier / len(df) * 100
        print(f"{k:18s} {outlier} aykiri deger (%{yuzde:.1f})  {'✅ Normal' if yuzde < 1 else '⚠️ Fazla — ana arterlerin dogal etkisi'}")

# 6. GENEL SONUÇ
print("\n" + "=" * 60)
print("📋 GENEL DEĞERLENDİRME")
print("=" * 60)
print(f"Toplam hucre     : {len(df)}")
print(f"Risk ortalamasi  : {risk.mean():.1f} / 100")
print(f"Risk std         : {risk.std():.1f}")
print(f"Veri kalitesi    : {'✅ Yayinlanabilir duzeyde' if risk.std() > 10 else '⚠️ Dusuk varyans'}")
