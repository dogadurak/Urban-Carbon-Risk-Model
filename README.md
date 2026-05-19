# 🏙️ Urban Carbon Risk Model — Bayraklı, İzmir

A **grid-based urban carbon risk index** developed for the Bayraklı district of İzmir, Turkey.
Building volume, road networks, traffic emissions, green areas, land surface temperature (LST),
and vegetation index (NDVI) are integrated to assign a carbon risk score to each 50×50m grid cell and individual building.
A K-Means clustering model is applied to classify risk zones.

---

## 📌 Project Pipeline

```
OSM Data Collection
       ↓
Building Volume & Road Carbon Scoring
       ↓
Grid-Based Spatial Integration (Overlay + Spatial Join)
       ↓
Min-Max Normalization (0–1)
       ↓
AHP-Based Hierarchical Carbon Risk Index (3 sub-indices)
       ↓
Building-Level Risk Transfer
       ↓
K-Means Clustering (k=6, silhouette=0.335)
       ↓
Statistical Validation (Pearson correlation, outlier analysis)
```

---

## 📂 File Structure

```
Urban-Carbon-Risk-Model/
├── 01_osm_veri_cekme.py          # OSM data collection via OSMnx
├── 02_bina_hacim_skor.py         # Building volume & carbon score calculation
├── 03_yol_karbon_skor.py         # Road network carbon scoring
├── 04_master_grid_olustur.py     # Spatial integration of all layers
├── 05_karbon_risk_indeks.py      # AHP hierarchical risk index
├── 06_bina_bazli_risk.py         # Building-level risk transfer
├── 07_kmeans_kumeleme.py         # K-Means clustering
├── 08_istatistiksel_kontrol.py   # Statistical quality control
└── README.md
```

---

## 🗂️ Data Sources

| Data | Source | Format |
|---|---|---|
| Building footprints | OpenStreetMap (OSMnx) | GeoJSON |
| Road network | OpenStreetMap (OSMnx) | GeoJSON |
| Green areas | OpenStreetMap (OSMnx) | GeoJSON |
| Land Surface Temperature | Landsat 8 | GeoTIFF |
| NDVI (Vegetation Index) | Landsat 8 | GeoTIFF |
| Population density | Türkiye Nüfus Grid (1km) | GeoTIFF |
| Industrial/commercial areas | OpenStreetMap | GeoJSON |
| Parking lots | OpenStreetMap | GeoJSON |
| Traffic emission points | OpenStreetMap | GeoJSON |

---

## ⚖️ AHP Weight Table

### Sub-Index 1: Transportation Emission Index (40% of final score)
| Criterion | Weight | Justification |
|---|---|---|
| Road network score | 0.60 | Primary emission source in Bayraklı (Altınyol transit corridor) |
| Traffic emission points | 0.25 | Direct CO₂ from vehicle idling |
| Parking lots | 0.15 | Vehicle idling emission zones |

### Sub-Index 2: Structural Emission Index (40% of final score)
| Criterion | Weight | Justification |
|---|---|---|
| Building volume score | 0.55 | Energy consumption proportional to volume |
| Population density | 0.30 | Exposure multiplier |
| Industrial/commercial area | 0.15 | Residual industrial activity |
> ⚠️ Building mask applied: cells with no buildings receive structural index = 0
> to prevent low-resolution population grids from generating artificial scores.

### Sub-Index 3: Urban Microclimate Index (20% of final score)
| Criterion | Weight | Direction |
|---|---|---|
| LST (Land Surface Temperature) | 0.70 | + Risk amplifier |
| NDVI (Vegetation Index) | 0.30 | − Carbon sink |

---

## 📊 K-Means Clustering Results

| Cluster | Risk Score (avg) | Cell Count | Interpretation |
|---|---|---|---|
| Risk Group 1 | 11.1 | 6,118 (37.7%) | Very Low Risk |
| Risk Group 2 | 38.0 | 9,678 (59.6%) | Low-Medium Risk |
| Risk Group 3 | 42.7 | 297 (1.8%) | Medium Risk |
| Risk Group 4 | 62.5 | 50 (0.3%) | Medium-High Risk |
| Risk Group 5 | 64.7 | 27 (0.2%) | High Risk |
| Risk Group 6 | 81.7 | 51 (0.3%) | Critical Risk |

---

## 📈 Statistical Validation

All emission criteria show expected correlation direction with final carbon risk score:

| Criterion | Pearson r | Direction |
|---|---|---|
| n_NDVI | −0.823 | ✅ Negative (carbon sink) |
| n_LST | +0.681 | ✅ Positive (heat island) |
| n_nufus | +0.611 | ✅ Positive (exposure) |
| n_yol | +0.607 | ✅ Positive (road emissions) |
| n_bina | +0.355 | ✅ Positive (building emissions) |
| n_trafik | +0.133 | ✅ Positive (traffic) |
| n_otopark | +0.127 | ✅ Positive (parking) |
| n_sanayi | +0.103 | ✅ Positive (industry) |

LST ↔ NDVI: r = −0.628 ✅ (higher temperature = lower vegetation, physically correct)

---

## 🛠️ Tech Stack

- **Python 3.x**
- `geopandas` — spatial data processing
- `osmnx` — OpenStreetMap data collection
- `rasterio` — raster data sampling
- `scikit-learn` — K-Means clustering
- `scipy` — statistical analysis
- `pandas`, `numpy` — data processing
- **QGIS** — visualization & symbology

## 📊 Kentsel Planlama İçin Karar Destek Çıktıları
Bu model sonucunda belediyeler ve AFAD için şu eylem planları haritalandırılmıştır:
1.  **Risk Grubu 5 (Ekstrem Risk):** Transit ulaşım ve gökdelenler. (Öneri: Acil emisyon bariyerleri ve yeşil çatı zorunluluğu).
2.  **Risk Grubu 4 (Isı Adaları):** Yoğun, ağaçsız betonarme doku. (Öneri: Mikro ağaçlandırma ve rüzgar koridoru açma çalışmaları).
3.  **Kırılganlık Kesişimi:** En yüksek Karbon Riski ile 65+ yaş nüfusun kesiştiği "Acil Müdahale" sokakları.
