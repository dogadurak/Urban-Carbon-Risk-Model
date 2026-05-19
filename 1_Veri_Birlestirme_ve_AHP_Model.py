import geopandas as gpd
import pandas as pd
import numpy as np
import rasterio

print("MASTER MODEL BAŞLATILIYOR...\n")

# 1. TÜM DOSYALARI OKU
grid           = gpd.read_file('grid_lst_ndvi_skor.geojson').to_crs(epsg=32635)
binalar        = gpd.read_file('bayrakli_binalar_hacim_c_skor.geojson').to_crs(epsg=32635)
yollar         = gpd.read_file('bayrakli_yollar_cskorli.geojson').to_crs(epsg=32635)
yesil_alanlar  = gpd.read_file('bayrakli_karbon_yutaklari_yesil_alanlar.geojson').to_crs(epsg=32635)
sanayi_ticaret = gpd.read_file('bayrakli_sanayi_ticaret.geojson').to_crs(epsg=32635)
otoparklar     = gpd.read_file('bayrakli_otoparklar.geojson').to_crs(epsg=32635)
trafik         = gpd.read_file('bayrakli_trafik_ve_emisyon_noktalari.geojson').to_crs(epsg=32635)

grid['grid_id'] = range(len(grid))

# 2. BİNALAR
bina_k   = gpd.overlay(binalar[['bina_c_skor','geometry']], grid[['grid_id','geometry']], how='intersection')
bina_sum = bina_k.groupby('grid_id')['bina_c_skor'].sum().reset_index()
bina_sum.rename(columns={'bina_c_skor': 'bina_emisyon'}, inplace=True)

# 3. YOLLAR
yollar['uzunluk_tam'] = yollar.geometry.length
yol_k = gpd.overlay(yollar[['highway','yol_c_skor','uzunluk_tam','geometry']], grid[['grid_id','geometry']], how='intersection')
yol_k['uzunluk_parca'] = yol_k.geometry.length
yol_k['yol_emisyon']   = (yol_k['uzunluk_parca'] / yol_k['uzunluk_tam']) * yol_k['yol_c_skor']
yol_sum = yol_k.groupby('grid_id')['yol_emisyon'].sum().reset_index()

# 4. YEŞİL ALAN + SANAYİ
yesil_temiz  = yesil_alanlar[yesil_alanlar.geometry.geom_type.isin(['Polygon','MultiPolygon'])].copy()
sanayi_temiz = sanayi_ticaret[sanayi_ticaret.geometry.geom_type.isin(['Polygon','MultiPolygon'])].copy()

yesil_k = gpd.overlay(yesil_temiz[['geometry']], grid[['grid_id','geometry']], how='intersection')
yesil_k['yesil_m2'] = yesil_k.geometry.area
yesil_sum = yesil_k.groupby('grid_id')['yesil_m2'].sum().reset_index()

sanayi_k = gpd.overlay(sanayi_temiz[['geometry']], grid[['grid_id','geometry']], how='intersection')
sanayi_k['sanayi_m2'] = sanayi_k.geometry.area
sanayi_sum = sanayi_k.groupby('grid_id')['sanayi_m2'].sum().reset_index()

# 5. OTOPARK + TRAFİK
otopark_j   = gpd.sjoin(otoparklar[['geometry']], grid[['grid_id','geometry']], how='inner', predicate='intersects')
otopark_sum = otopark_j.groupby('grid_id').size().reset_index(name='otopark_sayisi')

trafik_j   = gpd.sjoin(trafik[['geometry']], grid[['grid_id','geometry']], how='inner', predicate='intersects')
trafik_sum = trafik_j.groupby('grid_id').size().reset_index(name='trafik_sayisi')

# 6. NÜFUS RASTER
grid_wgs84 = grid.to_crs(epsg=4326)
centroids  = grid_wgs84.geometry.centroid
coords     = [(x, y) for x, y in zip(centroids.x, centroids.y)]

with rasterio.open('turkiye_nufus_1km.tif') as src:
    nufus = [val[0] for val in src.sample(coords)]

grid['nufus'] = pd.to_numeric(pd.Series(nufus), errors='coerce').fillna(0).apply(lambda x: max(x, 0)).values

# 7. HEPSİNİ BİRLEŞTİR
grid = grid.merge(bina_sum, on='grid_id', how='left').merge(yol_sum, on='grid_id', how='left')
grid = grid.merge(yesil_sum, on='grid_id', how='left').merge(sanayi_sum, on='grid_id', how='left')
grid = grid.merge(otopark_sum, on='grid_id', how='left').merge(trafik_sum, on='grid_id', how='left')

grid.fillna(0, inplace=True)

# 8. NORMALİZE ET VE AHP RİSK SKORU HESAPLA
def normalize(series):
    mn, mx = series.min(), series.max()
    return pd.Series([0.0]*len(series), index=series.index) if mx == mn else (series - mn) / (mx - mn)

for col in ['bina_emisyon', 'yol_emisyon', 'sanayi_m2', 'trafik_sayisi', 'otopark_sayisi', 'nufus', 'LST_mean', 'NDVI_mean']:
    grid[f'n_{col.split("_")[0]}'] = normalize(grid[col])

grid['karbon_risk'] = (
      grid['n_yol'] * 0.25 + grid['n_bina'] * 0.20 + grid['n_LST'] * 0.20 
    + grid['n_trafik'] * 0.15 + grid['n_sanayi'] * 0.08 + grid['n_nufus'] * 0.07 
    + grid['n_otopark'] * 0.05 - grid['n_NDVI'] * 0.15
).clip(lower=0)

grid['karbon_risk'] = normalize(grid['karbon_risk']) * 100
grid = grid.to_crs(epsg=4326)
grid.to_file('grid_MASTER_FINAL.geojson', driver='GeoJSON')
print("\n✅ TAMAMLANDI! 'grid_MASTER_FINAL.geojson' hazır.")
