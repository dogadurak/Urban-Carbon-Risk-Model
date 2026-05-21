# 🏙️ Urban Carbon Risk Model — Bayraklı, İzmir

A **grid-based urban carbon risk index** developed for the Bayraklı district of İzmir, Turkey.
Building volume, road networks, traffic emissions, green areas, land surface temperature (LST),
and vegetation index (NDVI) are integrated into a hierarchical AHP model to assign a carbon risk score
to each 50×50m grid cell and individual building. K-Means clustering is applied to identify spatial risk zones.

---

## 🗺️ Maps

### 1. Carbon Risk Index (Final Score)
![Carbon Risk Score](maps/karbon_risk_skoru.png)
> Final grid-based carbon risk index (0–100). Red = high risk (coastal strip, Altınyol corridor), Blue = low risk (northern vegetated slopes).

---

### 2. Sub-Index Maps

#### 🚗 Transportation Emission Index
![Transportation Index](maps/ualsim_index.png)
> Combines road network score (60%), traffic emission points (25%), and parking lots (15%). Highlights major arterial corridors and dense traffic zones.

#### 🏢 Structural Emission Index
![Structural Index](maps/yapisal_index.png)
> Combines building volume score (55%), population density (30%), and industrial/commercial area (15%). Building mask applied — cells with no buildings receive score = 0.

#### 🌡️ Urban Microclimate Index
![Microclimate Index](maps/mikroklima_index.png)
> LST (70%) minus NDVI (30%). Highlights urban heat island zones where high temperature meets low vegetation.

---

### 3. Input Data Maps

#### 🌿 NDVI — Vegetation Index
![NDVI](maps/NDVI_bayrakli.png)
> Derived from Landsat 8 (Band 4 & Band 8) in QGIS. Orange/red = low vegetation (urban core), Green/teal = high vegetation (northern slopes).

#### 🌡️ LST — Land Surface Temperature
![LST](maps/lst_bayrakli.png)
> Derived from Landsat 8 thermal band in QGIS. Red = high temperature (urban heat island), Blue = cool (forested slopes). Range: 20.0°C – 29.4°C.

---

### 4. K-Means Cluster Map
![K-Means](maps/k_means.png)
> 6 spatially coherent risk zones identified by unsupervised machine learning (silhouette score = 0.335).

---

## 📌 Project Pipeline

```
Landsat 8 → LST & NDVI Processing (QGIS)
                    +
        OSM Data Collection (OSMnx)
                    ↓
   Building Volume & Road Carbon Scoring
                    ↓
  Grid-Based Spatial Integration
  (Overlay + Spatial Join + Raster Sampling)
                    ↓
      Min-Max Normalization (0–1)
                    ↓
   AHP Hierarchical Carbon Risk Index
   ┌─────────────────────────────────┐
   │  Transportation Index  → 40%   │
   │  Structural Index      → 40%   │
   │  Microclimate Index    → 20%   │
   └─────────────────────────────────┘
                    ↓
      Building-Level Risk Transfer
                    ↓
    K-Means Clustering (k=6)
                    ↓
    Statistical Validation
```

---

## 📂 File Structure

```
Urban-Carbon-Risk-Model/
├── maps/
│   ├── karbon_risk_skoru.png     # Final carbon risk index
│   ├── ualsim_index.png          # Transportation emission sub-index
│   ├── yapisal_index.png         # Structural emission sub-index
│   ├── mikroklima_index.png      # Urban microclimate sub-index
│   ├── NDVI_bayrakli.png         # NDVI vegetation map
│   ├── lst_bayrakli.png          # Land surface temperature map
│   └── k_means.png               # K-Means cluster map
├── 01_osm_veri_cekme.py          # OSM data collection via OSMnx
├── 02_bina_hacim_skor.py         # Building volume & carbon score
├── 03_yol_karbon_skor.py         # Road network carbon scoring
├── 04_master_grid_olustur.py     # Spatial integration of all layers
├── 05_karbon_risk_indeks.py      # AHP hierarchical risk index
├── 06_bina_bazli_risk.py         # Building-level risk transfer
├── 07_kmeans_kumeleme.py         # K-Means clustering
├── 08_istatistiksel_kontrol.py   # Statistical quality control
├── requirements.txt
└── README.md
```

---

## 🗂️ Data Sources

| Data | Source | Processing | Format |
|---|---|---|---|
| Building footprints | OpenStreetMap (OSMnx) | Python | GeoJSON |
| Road network | OpenStreetMap (OSMnx) | Python | GeoJSON |
| Green areas | OpenStreetMap (OSMnx) | Python | GeoJSON |
| Industrial/commercial areas | OpenStreetMap | Python | GeoJSON |
| Parking lots | OpenStreetMap | Python | GeoJSON |
| Traffic emission points | OpenStreetMap | Python | GeoJSON |
| Land Surface Temperature | Landsat 8 | **QGIS** | GeoTIFF |
| NDVI (Vegetation Index) | Landsat 8 | **QGIS** | GeoTIFF |
| Population density | Türkiye Nüfus Grid (1km) | Python (rasterio) | GeoTIFF |

> **Note:** LST and NDVI rasters were processed in QGIS using Landsat 8 imagery before being integrated into the Python pipeline via `rasterio`.

---

## ⚖️ AHP Weight Table

### 🚗 Sub-Index 1: Transportation Emission Index (40%)
| Criterion | Weight | Justification |
|---|---|---|
| Road network score | 0.60 | Primary emission source — Altınyol transit corridor |
| Traffic emission points | 0.25 | Direct CO₂ from vehicle idling |
| Parking lots | 0.15 | Vehicle idling emission zones |

### 🏢 Sub-Index 2: Structural Emission Index (40%)
| Criterion | Weight | Justification |
|---|---|---|
| Building volume score | 0.55 | Energy consumption proportional to volume |
| Population density | 0.30 | Exposure multiplier |
| Industrial/commercial area | 0.15 | Residual industrial activity |

> ⚠️ **Built-up mask applied:** Cells with no buildings receive structural index = 0 to prevent low-resolution population grids from generating artificial scores in open land.

### 🌡️ Sub-Index 3: Urban Microclimate Index (20%)
| Criterion | Weight | Direction |
|---|---|---|
| LST (Land Surface Temperature) | 0.70 | ➕ Risk amplifier |
| NDVI (Vegetation Index) | 0.30 | ➖ Carbon sink |

> LST is treated as a **risk outcome indicator**, not an emission source. Isolating it in its own sub-index prevents it from statistically dominating human-caused emission variables.

---

## 📊 K-Means Clustering Results (k=6, silhouette=0.335)

| Cluster | Risk Avg | Cell Count | Interpretation |
|---|---|---|---|
| Risk Group 1 | 11.1 | 6,118 (37.7%) | Natural / Undeveloped Areas |
| Risk Group 2 | 38.0 | 9,678 (59.6%) | Low-Risk Residential |
| Risk Group 3 | 42.7 | 297 (1.8%) | Urban Heat Islands & Dense Fabric |
| Risk Group 4 | 62.5 | 50 (0.3%) | Extreme Emission Corridors |
| Risk Group 5 | 64.7 | 27 (0.2%) | Commercial Axes & Tower Zones |
| Risk Group 6 | 81.7 | 51 (0.3%) | Critical Risk |

---

## 📈 Statistical Validation (p < 0.001)

| Criterion | Pearson r | Result |
|---|---|---|
| n_NDVI | −0.823 | ✅ Negative — carbon sink confirmed |
| n_LST | +0.681 | ✅ Positive — heat island effect |
| n_nufus | +0.611 | ✅ Positive — population exposure |
| n_yol | +0.607 | ✅ Positive — road emissions |
| n_bina | +0.355 | ✅ Positive — building emissions |
| n_trafik | +0.133 | ✅ Positive — traffic points |
| n_otopark | +0.127 | ✅ Positive — parking emissions |
| n_sanayi | +0.103 | ✅ Positive — industrial activity |

**LST ↔ NDVI: r = −0.628** ✅ Physically correct — higher temperature correlates with lower vegetation

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| `geopandas` | Spatial overlay, join, CRS transformations |
| `osmnx` | OpenStreetMap data collection |
| `rasterio` | Raster sampling (LST, NDVI, population) |
| `scikit-learn` | K-Means clustering, StandardScaler |
| `scipy` | Pearson correlation, Z-score outlier detection |
| `pandas` / `numpy` | Data wrangling & normalization |
| **QGIS** | LST & NDVI processing, cartographic output |



## 📊 Kentsel Planlama İçin Karar Destek Çıktıları
Bu model sonucunda belediyeler ve AFAD için şu eylem planları haritalandırılmıştır:
1.  **Risk Grubu 5 (Ekstrem Risk):** Transit ulaşım ve gökdelenler. (Öneri: Acil emisyon bariyerleri ve yeşil çatı zorunluluğu).
2.  **Risk Grubu 4 (Isı Adaları):** Yoğun, ağaçsız betonarme doku. (Öneri: Mikro ağaçlandırma ve rüzgar koridoru açma çalışmaları).
3.  **Kırılganlık Kesişimi:** En yüksek Karbon Riski ile 65+ yaş nüfusun kesiştiği "Acil Müdahale" sokakları.

# 🏙️ Urban Carbon Risk Model — Bayraklı, İzmir

A **grid-based urban carbon risk index** developed for the Bayraklı district of İzmir, Turkey.
Building volume, road networks, traffic emissions, green areas, land surface temperature (LST),
and vegetation index (NDVI) are integrated into a hierarchical AHP model to assign a carbon risk score
to each 50×50m grid cell and individual building. K-Means clustering is applied to identify spatial risk zones.

---

## 🗺️ Maps

### 1. Carbon Risk Index (Final Score)
![Carbon Risk Score](maps/karbon_risk_skoru.png)
> Final grid-based carbon risk index (0–100). Red = high risk (coastal strip, Altınyol corridor), Blue = low risk (northern vegetated slopes).

---

### 2. Sub-Index Maps

#### 🚗 Transportation Emission Index
![Transportation Index](maps/ualsim_index.png)
> Combines road network score (60%), traffic emission points (25%), and parking lots (15%). Highlights major arterial corridors and dense traffic zones.

#### 🏢 Structural Emission Index
![Structural Index](maps/yapisal_index.png)
> Combines building volume score (55%), population density (30%), and industrial/commercial area (15%). Building mask applied — cells with no buildings receive score = 0.

#### 🌡️ Urban Microclimate Index
![Microclimate Index](maps/mikroklima_index.png)
> LST (70%) minus NDVI (30%). Highlights urban heat island zones where high temperature meets low vegetation.

---

### 3. Input Data Maps

#### 🌿 NDVI — Vegetation Index
![NDVI](maps/NDVI_bayrakli.png)
> Derived from Landsat 9 (Band 4 & Band 5) via thresholding methods. Orange/red = low vegetation (urban core), Green/teal = high vegetation (northern slopes).

#### 🌡️ LST — Land Surface Temperature
![LST](maps/lst_bayrakli.png)
> Derived from Landsat 9 (Band 10) utilizing TOA Radiance and the Jimenez-Munoz & Sobrino equation. Red = high temperature (urban heat island), Blue = cool (forested slopes). Range: **19.1°C – 29.4°C**.
>
> 🔬 **Scientific Note on LST Values:** > The calculated temperature range reflects **instantaneous morning surface temperatures**, not daily maximum air temperatures. Landsat 9 passes over the İzmir region at approximately **10:30 AM local time**, capturing the thermal signature of surfaces before they absorb peak midday solar radiation. Furthermore, the 30-meter spatial resolution introduces a **"mixed-pixel effect"**; a single grid cell's thermal value represents a weighted average of sunlit concrete, cooling vegetation, and long morning shadows cast by high-rise structures (e.g., Bayraklı Tower, Biva Tower). This makes the 19°C - 29°C range highly accurate for this specific temporal window.

---

### 4. K-Means Cluster Map
![K-Means](maps/k_means.png)
> 6 spatially coherent risk zones identified by unsupervised machine learning (silhouette score = 0.335).

---

## 📌 Project Pipeline

```text
Landsat 9 → LST & NDVI Processing (QGIS / Python)
                    +
        OSM Data Collection (OSMnx)
                    ↓
   Building Volume & Road Carbon Scoring
                    ↓
  Grid-Based Spatial Integration
  (Overlay + Spatial Join + Raster Sampling)
                    ↓
      Min-Max Normalization (0–1)
                    ↓
   AHP Hierarchical Carbon Risk Index
   ┌─────────────────────────────────┐
   │  Transportation Index  → 40%    │
   │  Structural Index      → 40%    │
   │  Microclimate Index    → 20%    │
   └─────────────────────────────────┘
                    ↓
      Building-Level Risk Transfer
                    ↓
    K-Means Clustering (k=6)
                    ↓
    Statistical Validation
