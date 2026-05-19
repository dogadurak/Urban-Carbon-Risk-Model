
# 🌍 İklim Dirençli Kentler: 3B Kentsel Morfoloji ve Makine Öğrenmesi Destekli Karbon Risk Modeli

**Geliştirici:** İzmir Katip Çelebi Üniversitesi, Geomatik Mühendisliği - Grup 6 (Manifest)
**Bölge:** İzmir / Bayraklı

---

## 📌 Projenin Amacı ve Vizyonu
İklim krizine karşı şehirleri "İklim Dirençli" (Climate Resilient) hale getirmek yerel yönetimlerin en acil gündemidir. Ancak klasik CBS (Coğrafi Bilgi Sistemleri) yaklaşımları genellikle yüzeysel ve statik ısı haritaları üretir. 

Bu proje, **Makro (Grid) ölçekten Mikro (Bina) ölçeğe** inen; uydu verilerini, 3 boyutlu kentsel morfolojiyi ve demografik kırılganlığı **Makine Öğrenmesi (K-Means)** ile birleştiren **Dinamik Bir Mekansal Karar Destek Sistemidir.** Amacımız; yerel yönetimlere "Bayraklı çok sıcak" demek yerine, "Sıcaklığın, yoğun yapılaşmanın ve trafiğin kesiştiği X sokağına acilen Düşük Emisyon Bölgesi (LEZ) yatırımı yapılmalıdır" diyebilecek veriye dayalı bir reçete sunmaktır.

---

## 🚀 Kullanılan Teknolojiler ve Veri Kaynakları

* **Programlama & Veri Bilimi:** Python, GeoPandas, Pandas, Numpy, Scikit-Learn
* **Mekansal Analiz & Görselleştirme:** QGIS (Model Builder, Qgis2threejs), Rasterio
* **API & Açık Veri:** OSMnx (OpenStreetMap API)
* **Uydu Verileri:** USGS (Landsat 8/9 LST ve NDVI İndeksleri)
* **Sosyal Veri:** TÜİK (Mahalle Bazlı Yaşlı ve Kırılgan Nüfus)

---

## ⚙️ Metodoloji: Uçtan Uca (End-to-End) Veri Mimarisi

Proje 4 ana aşamadan oluşmaktadır ve kodları depoda sırasıyla numaralandırılmıştır:

### 1. Açık Veri Toplama (OSMnx) 👉 `0_Veri_Toplama_OSMnx.py`
Tüm Bayraklı ilçesinin bina ayak izleri, kat yükseklikleri, karayolu ağları, parkları ve sanayi alanları doğrudan OpenStreetMap API'si kullanılarak çekilmiş ve EPSG:32635 metrik sistemine projeksiyolanmıştır.

### 2. AHP ve Dazimetrik Maskeleme 👉 `1_Veri_Birlestirme_ve_AHP_Model.py`
Raster verilerin (Sıcaklık) vektör verileri (Otopark, Sanayi) ezmesini engellemek için "Hiyerarşik İndeksleme" kullanılmıştır.
* **Ulaşım İndeksi** (Yol, Trafik, Otopark)
* **Yapısal İndeks** (Bina Hacmi, Nüfus, Sanayi)
* **Mikroklima İndeksi** (LST - NDVI)
**Dazimetrik Filtre:** Binaların olmadığı doğal arazilerde kentsel risk sıfırlanarak modelin gerçeğe yakınsaması sağlanmıştır.

### 3. Mikro Ölçek Geçişi 👉 `2_Bina_Bazli_Mikro_Model.py`
Projenin en yenilikçi adımıdır. Analizler grid düzeyinde kalmamış, `sjoin` (Spatial Join) ile doğrudan 3 boyutlu binaların üzerine indirilmiştir. Her bina; kendi emisyonu, önündeki yolun baskısı ve bulunduğu mikroklima ile **"Karbon Kimlik Kartı"**na sahip olmuştur.

### 4. Yapay Zeka ile Teşhis 👉 `3_Yapay_Zeka_KMeans_Modeli.py`
*AHP ile hesaplanan veriler ne kadar doğru?* Bu soruyu cevaplamak için veriler (Dağlar ve boş araziler maskelenerek) K-Means (Unsupervised Learning) algoritmasına verilmiştir. 
Yapay zeka, Bayraklı'nın kentsel dokusunu insan müdahalesi olmadan 5 ana karaktere bölmüştür. Sonuçlar kentsel eşitsizliği kanıtlamıştır: **Bayraklı'daki Karbon Riskinin çok büyük bir kısmı, ilçenin genelinde değil, Altınyol aksı ve Merkezi İş Alanında (MİA) bulunan dar bir alana sıkışmıştır.**

---

## 📊 Kentsel Planlama İçin Karar Destek Çıktıları
Bu model sonucunda belediyeler ve AFAD için şu eylem planları haritalandırılmıştır:
1.  **Risk Grubu 5 (Ekstrem Risk):** Transit ulaşım ve gökdelenler. (Öneri: Acil emisyon bariyerleri ve yeşil çatı zorunluluğu).
2.  **Risk Grubu 4 (Isı Adaları):** Yoğun, ağaçsız betonarme doku. (Öneri: Mikro ağaçlandırma ve rüzgar koridoru açma çalışmaları).
3.  **Kırılganlık Kesişimi:** En yüksek Karbon Riski ile 65+ yaş nüfusun kesiştiği "Acil Müdahale" sokakları.
