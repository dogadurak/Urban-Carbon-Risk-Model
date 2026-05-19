import osmnx as ox
import geopandas as gpd

print("BAYRAKLI KENTSEL VERİLERİ ÇEKİLİYOR (OSMnx)...\n")

# Analiz edilecek bölge
ilce = "Bayraklı, İzmir, Turkey"

# ==========================================
# 1. BİNA VERİLERİNİN ÇEKİLMESİ
# ==========================================
print("1/4: Bina ayak izleri indiriliyor...")
tags_bina = {'building': True}
binalar = ox.features_from_place(ilce, tags=tags_bina)
# Sadece poligon olan gerçek binaları filtrele
binalar = binalar[binalar.geometry.geom_type.isin(['Polygon', 'MultiPolygon'])]

# ==========================================
# 2. ULAŞIM (YOL) AĞLARININ ÇEKİLMESİ
# ==========================================
print("2/4: Ulaşım ve yol ağları indiriliyor...")
tags_yol = {'highway': True}
yollar = ox.features_from_place(ilce, tags=tags_yol)
# Sadece çizgi (LineString) olan yolları filtrele
yollar = yollar[yollar.geometry.geom_type.isin(['LineString', 'MultiLineString'])]

# ==========================================
# 3. KARBON YUTAKLARI (YEŞİL ALANLAR)
# ==========================================
print("3/4: Yeşil alanlar ve parklar indiriliyor...")
tags_yesil = {'leisure': 'park', 'landuse': ['forest', 'grass', 'meadow']}
yesil_alanlar = ox.features_from_place(ilce, tags=tags_yesil)

# ==========================================
# 4. KOORDİNAT DÖNÜŞÜMÜ VE KAYDETME
# Metrik sisteme (EPSG:32635) geçiş yapıyoruz ki alan hesabı yapabilelim
# ==========================================
print("4/4: Koordinat sistemleri EPSG:32635 (Metrik) olarak ayarlanıyor ve kaydediliyor...")

binalar_32635 = binalar.to_crs(epsg=32635)
yollar_32635 = yollar.to_crs(epsg=32635)
yesil_alanlar_32635 = yesil_alanlar.to_crs(epsg=32635)

# Gereksiz sütunlardan arındırıp sadece geometriyi ve ana türü kaydedelim
binalar_32635[['geometry']].to_file('bayrakli_binalar_ham.geojson', driver='GeoJSON')
yollar_32635[['geometry', 'highway']].to_file('bayrakli_yollar_ham.geojson', driver='GeoJSON')
yesil_alanlar_32635[['geometry']].to_file('bayrakli_yesil_alanlar_ham.geojson', driver='GeoJSON')

print("\n✅ İŞLEM TAMAM! Tüm altlık veriler başarıyla indirildi.")
