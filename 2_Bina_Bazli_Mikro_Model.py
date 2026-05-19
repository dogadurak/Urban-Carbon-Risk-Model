import geopandas as gpd
import pandas as pd

print("BİNA BAZLI KARBON RİSK BAŞLATILIYOR...\n")

binalar = gpd.read_file('bayrakli_binalar_hacim_c_skor.geojson').to_crs(epsg=32635)
grid    = gpd.read_file('grid_MASTER_FINAL.geojson').to_crs(epsg=32635)

mn, mx = binalar['bina_c_skor'].min(), binalar['bina_c_skor'].max()
binalar['bina_normalize'] = ((binalar['bina_c_skor'] - mn) / (mx - mn)) * 100

# Grid'den sadece ihtiyaç duyulan sütunları alıyoruz
# Not: Yukarıdaki AHP modelinde sütun isimleri dinamik üretildiği için 
# bu birleştirmede indeksleri kullanıyoruz.
grid_cols = grid[['n_yol', 'n_bina', 'n_LST', 'karbon_risk', 'geometry']]

print("Binalar grid ile eslestiriliyor...")
binalar_gridli = gpd.sjoin(binalar, grid_cols, how='left', predicate='intersects')
binalar_gridli = binalar_gridli[~binalar_gridli.index.duplicated(keep='first')]
binalar_gridli.fillna(0, inplace=True)

print("Bina bazli risk skoru hesaplaniyor...")
binalar_gridli['bina_risk'] = (
      binalar_gridli['bina_normalize'] * 0.40
    + binalar_gridli['n_yol'] * 0.40
    + binalar_gridli['n_LST'] * 0.20
)

mn2, mx2 = binalar_gridli['bina_risk'].min(), binalar_gridli['bina_risk'].max()
binalar_gridli['bina_risk'] = ((binalar_gridli['bina_risk'] - mn2) / (mx2 - mn2)) * 100

binalar_gridli.to_file('binalar_NIHAI_RISK.geojson', driver='GeoJSON')
print("\n✅ 'binalar_NIHAI_RISK.geojson' hazır!")
