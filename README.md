README dosyasını daha geniş kapsamlı, projenin akademik ve bilimsel derinliğini tam olarak yansıtan, hem metodolojiyi hem de amacını detaylıca açıklayan profesyonel bir formata kavuşturdum. Mevcut hiçbir veriyi, tabloyu veya K-Means skorunu eksiltmeden, anlatımı zenginleştirerek yeniden düzenledim:

```markdown
# 🏙️ Urban Carbon Risk Model — Bayraklı, İzmir

## 🎯 1. Proje Hakkında ve Amaç (Project Overview & Objective)

Bu proje; İzmir'in en dinamik, heterojen ve yapısal açıdan yoğun bölgelerinden biri olan **Bayraklı** ilçesi için **hücresel tabanlı bir kentsel karbon risk indeksi (Grid-Based Urban Carbon Risk Index)** modellemek amacıyla geliştirilmiştir. 

### 📌 Temel Amaç:
Hızlı kentsel dönüşümün, yüksek katlı iş merkezlerinin (gökdelenler bölgesinin) ve yoğun transit ulaşım koridorlarının (Altınyol gibi) bir arada bulunduğu Bayraklı'da; emisyon kaynakları ile mikroklimatik etkileri mekânsal olarak ilişkilendirmektir. Proje, kentsel morfolojiyi (bina hacimleri, nüfus yoğunluğu), ulaşım ağlarını ve arazi yüzey sıcaklığını (LST) yüksek çözünürlüklü **50×50 metrelik hücreler (grid)** seviyesinde entegre ederek; sürdürülebilir kentsel planlama, kentsel ısı adası (UHI) mitigasyonu ve yerel yönetimler/AFAD için **Mekânsal Karar Destek Çıktıları** üretmeyi hedefler.

---

## 🗺️ 2. Tematik Haritalar (Maps & Visualizations)

### 2.1. Karbon Risk İndeksi - Nihai Skor (Carbon Risk Index - Final Score)
![Carbon Risk Score](maps/karbon_risk_skoru.png)
> **Açıklama:** Analitik Hiyerarşi Süreci (AHP) sonucunda elde edilen, 0-100 arasında normalize edilmiş nihai karbon risk haritasıdır. Kırmızı tonlar; kıyı şeridini, Altınyol transit koridorunu ve merkezi iş alanlarını kapsayan **yüksek riskli** bölgeleri temsil ederken; mavi tonlar kuzeydeki bitki örtüsüne sahip serin yamaçları (**düşük risk**) göstermektedir.

---

### 2.2. Alt-İndeks Haritaları (Sub-Index Maps)

#### 🚗 Ulaşım Emisyon İndeksi (Transportation Emission Index)
![Transportation Index](maps/ualsim_index.png)
> **Açıklama:** Yol ağı yoğunluğu (%60), trafik emisyon odakları (%25) ve otopark alanlarının (%15) mekânsal ağırlıklandırılmasıyla üretilmiştir. Bayraklı'daki ana arterleri, kavşak noktalarını ve dur-kalk emisyonlarının yoğunlaştığı transit koridorları açıkça izole eder.

#### 🏢 Yapısal Emisyon İndeksi (Structural Emission Index)
![Structural Index](maps/yapisal_index.png)
> **Açıklama:** Bina hacim skoru (%55), nüfus yoğunluğu (%30) ve endüstriyel/ticari alanların (%15) birleşiminden oluşur. Yapay emisyonların yerleşim alanları dışına taşmasını önlemek amacıyla **bina maskesi (built-up mask)** uygulanmıştır; bina bulunmayan hücrelerin yapısal emisyon skoru doğrudan 0 olarak atanmıştır.

#### 🌡️ Kentsel Mikroklima İndeksi (Urban Microclimate Index)
![Microclimate Index](maps/mikroklima_index.png)
> **Açıklama:** Land Surface Temperature (LST) (%70) değerinden NDVI (%30) değerinin çıkarılmasıyla hesaplanmıştır. Yüksek yüzey sıcaklığının, düşük vegetasyon (yeşil alan eksikliği) ile kesiştiği kentsel ısı adası (UHI) çekirdeklerini mekânsal olarak ortaya koyar.

---

### 2.3. Girdi Veri Haritaları (Input Data Maps)

#### 🌿 NDVI — Bitki Örtüsü İndeksi (Vegetation Index)
![NDVI](maps/NDVI_bayrakli.png)
> **Açıklama:** Landsat 9 uydusunun Yakın Kızılötesi (NIR - Bant 5) ve Kırmızı (Red - Bant 4) bantları kullanılarak hesaplanmıştır. Turuncu/kırmızı tonlar vegetasyonun zayıf olduğu kentsel çekirdeği, yeşil/turkuaz tonlar ise karbon yutağı görevi gören kuzey sırtlarını gösterir.

#### 🌡️ LST — Arazi Yüzey Sıcaklığı (Land Surface Temperature)
![LST](maps/lst_bayrakli.png)
> **Açıklama:** Landsat 9 termal bandından (Bant 10) Tepe Atmosfer Radyansı (TOA Radiance) ve Planck/Sobrino algoritmaları kullanılarak üretilmiştir. Kırmızı alanlar yüksek yüzey sıcaklığına sahip kentsel dokuyu, mavi alanlar ise ormanlık/yeşil alanları temsil eder. Piksel değer aralığı: **20.0°C – 29.4°C**.

> 🔬 **LST Değerlerine İlişkin Bilimsel Not (Scientific Note on LST):**
> Hesaplanan sıcaklık aralığı gün içi maksimum hava sıcaklığını değil, **anlık sabah yüzey sıcaklıklarını** ifade etmektedir. Landsat 9 uydusu İzmir bölgesinden yerel saatle yaklaşık **10:30 - 11:00** civarında geçmektedir. Bu saatlerde yüzeyler henüz günün en yüksek güneş radyasyonuna maruz kalmamış ve pik sıcaklığına ulaşmamıştır. Ayrıca uydunun termal çözünürlüğü ve kentsel morfoloji nedeniyle **"karışık piksel (mixed-pixel) etkisi"** mevcuttur; 30 metrelik tek bir pikselin termal değeri, güneş alan beton yüzeylerin yanı sıra bölgedeki yüksek katlı yapıların (Bayraklı Tower, Biva Tower vb.) sabah saatlerinde batı/kuzey yönüne düşürdüğü uzun gölgelerin ve aralardaki ağaçların termal ortalamasını yansıtır. Bu durum, 20°C - 29.4°C aralığının o zaman dilimi için fiziksel ve bilimsel olarak tamamen doğru ve gerçeğe uygun olduğunu kanıtlamaktadır.

---

### 2.4. K-Means Kümeleme Haritası (K-Means Cluster Map)
![K-Means](maps/k_means.png)
> **Açıklama:** Gözetimsiz makine öğrenmesi (Unsupervised Machine Learning) yöntemiyle, hücrelerin sahip olduğu tüm risk parametreleri analiz edilerek üretilen 6 homojen risk bölgesidir (Silhouette skoru = 0.335).

---

## 📌 3. Proje İş Akışı (Project Pipeline)

```text
Landsat 9 → LST & NDVI Modelleme (QGIS / Python)
                    +
        OSM Veri Madenciliği (OSMnx)
                    ↓
   Bina Hacimsel Hesaplama & Yol Karbon Skorlaması
                    ↓
  Hücresel Tabandan Mekânsal Entegrasyon
  (Overlay + Spatial Join + Raster Sampling)
                    ↓
      Min-Max Normalizasyonu (0–1)
                    ↓
   AHP Hiyerarşik Karbon Risk İndeksi Hesabı
   ┌─────────────────────────────────┐
   │  Ulaşım Emisyon İndeksi → %40    │
   │  Yapısal Emisyon İndeksi → %40    │
   │  Mikroklima İndeksi     → %20    │
   └─────────────────────────────────┘
                    ↓
      Bina Bazlı Risk Transferi (Overlay)
                    ↓
    K-Means Kümeleme Analizi (k=6)
                    ↓
    İstatistiksel Validasyon & Korelasyon

```

---

## 📂 4. Dosya Yapısı (File Structure)

```text
Urban-Carbon-Risk-Model/
├── maps/
│   ├── karbon_risk_skoru.png     # Nihai karbon risk haritası
│   ├── ualsim_index.png          # Ulaşım emisyonu alt indeksi
│   ├── yapisal_index.png         # Yapısal emisyon alt indeksi
│   ├── mikroklima_index.png      # Kentsel mikroklima alt indeksi
│   ├── NDVI_bayrakli.png         # NDVI bitki örtüsü haritası
│   ├── lst_bayrakli.png          # Arazi yüzey sıcaklığı (LST) haritası
│   └── k_means.png               # K-Means kümeleme haritası
├── 01_osm_veri_cekme.py          # OSMnx kullanarak OSM verilerinin çekilmesi
├── 02_bina_hacim_skor.py         # Bina taban alanı ve kat adedi ile hacim hesabı
├── 03_yol_karbon_skor.py         # Yol sınıfına göre emisyon ağırlıklandırması
├── 04_master_grid_olustur.py     # Tüm katmanların 50x50m gridde birleştirilmesi
├── 05_karbon_risk_indeks.py      # AHP hiyerarşik risk matrisi analizi
├── 06_bina_bazli_risk.py         # Hücresel riskin bina geometrilerine aktarımı
├── 07_kmeans_kumeleme.py         # K-Means makine öğrenmesi kümelemesi
├── 08_istatistiksel_kontrol.py   # Pearson korelasyon ve kalite kontrol testleri
├── requirements.txt
└── README.md

```

---

## 🗂️ 5. Veri Kaynakları (Data Sources)

| Veri Seti | Kaynak | İşleme / Modelleme | Format |
| --- | --- | --- | --- |
| Bina Geometrileri (Footprints) | OpenStreetMap (OSMnx) | Python (GeoPandas) | GeoJSON |
| Yol Ağı (Road Network) | OpenStreetMap (OSMnx) | Python (GeoPandas) | GeoJSON |
| Yeşil Alanlar (Green Areas) | OpenStreetMap | Python (GeoPandas) | GeoJSON |
| Ticari / Endüstriyel Alanlar | OpenStreetMap | Python | GeoJSON |
| Otopark Poligonları | OpenStreetMap | Python | GeoJSON |
| Trafik Yoğunluk Odakları | OpenStreetMap | Python | GeoJSON |
| Arazi Yüzey Sıcaklığı (LST) | **Landsat 9 (B10)** | QGIS / Python (rasterio) | GeoTIFF |
| NDVI (Bitki Örtüsü İndeksi) | **Landsat 9 (B4, B5)** | QGIS / Python (rasterio) | GeoTIFF |
| Nüfus Yoğunluğu | Türkiye Nüfus Grid (1km) | Python (Spatially Resampled) | GeoTIFF |

---

## ⚖️ 6. AHP Ağırlık Matrisleri (AHP Weight Tables)

### 🚗 Alt İndeks 1: Ulaşım Emisyon İndeksi (%40)

| Kriter | Ağırlık | Bilimsel Gerekçe |
| --- | --- | --- |
| Yol Ağ Skoru (Sınıf bazlı) | 0.60 | Birincil emisyon kaynağı (Örn: Altınyol ana transit hattı) |
| Trafik Emisyon Noktaları | 0.25 | Kavşak ve dur-kalk noktalarında biriken doğrudan CO₂ salınımı |
| Otopark Alanları | 0.15 | Araç rölanti ve parklanma kaynaklı mikro emisyon bölgeleri |

### 🏢 Alt İndeks 2: Yapısal Emisyon İndeksi (%40)

| Kriter | Ağırlık | Bilimsel Gerekçe |
| --- | --- | --- |
| Bina Hacim Skoru | 0.55 | Bina hacmi arttıkça enerji tüketimi ve karbon ayak izi doğrusal artar |
| Nüfus Yoğunluğu | 0.30 | Karbon emisyonuna maruz kalan insan yoğunluğu (Maruziyet Çarpanı) |
| Endüstriyel/Ticari Alanlar | 0.15 | Ticari faaliyetlerden kaynaklanan ikincil emisyonlar |

> ⚠️ **Önemli Metodolojik Not:** Bina bulunmayan boş hücrelerin (açık araziler) yapısal emisyon indeks değeri otomatik olarak 0 yapılmıştır. Böylece düşük çözünürlüklü nüfus verilerinin boş arazilerde yapay risk skorları üretmesi engellenmiştir.

### 🌡️ Alt İndeks 3: Kentsel Mikroklima İndeksi (%20)

| Kriter | Ağırlık | Etki Yönü | Bilimsel Gerekçe |
| --- | --- | --- | --- |
| LST (Yüzey Sıcaklığı) | 0.70 | ➕ Pozitif | Isı birikimi kentsel karbon riskini artıran bir iklimsel çarpandır |
| NDVI (Bitki Örtüsü) | 0.30 | ➖ Negatif | Yeşil doku karbon yutağı ve serinletici etki sağlar (Azaltıcı faktör) |

---

## 📊 7. K-Means Kümeleme Analizi Sonuçları (k=6, Silhouette=0.335)

| Küme (Cluster) | Ortalama Risk | Hücre Sayısı | Mekânsal Karşılık ve Yorum |
| --- | --- | --- | --- |
| Risk Grubu 1 | 11.1 | 6,118 (%37.7) | Doğal Alanlar, Yapılaşmamış Boş Yamaçlar ve Yeşil Koridorlar |
| Risk Group 2 | 38.0 | 9,678 (%59.6) | Düşük Yoğunluklu Yerleşim Alanları ve Az Katlı Konut Dokusu |
| Risk Group 3 | 42.7 | 297 (%1.8) | Kentsel Isı Adaları ve Bitki Örtüsünden Kopuk Yoğun Beton Yapısal Doku |
| Risk Group 4 | 62.5 | 50 (%0.3) | Ekstrem Emisyon Koridorları (Ana Arterler, Büyük Kavşaklar) |
| Risk Group 5 | 64.7 | 27 (%0.2) | Ticari Akslar, Merkezi İş Alanları ve Gökdelenler Bölgesi |
| Risk Group 6 | 81.7 | 51 (%0.3) | **Kritik Risk Alanları:** Yoğun Ulaşım ve Yapısal Hacmin Kesiştiği Düğüm Noktaları |

---

## 📈 8. İstatistiksel Validasyon ve Korelasyon Matrisi (p < 0.001)

Modelin doğruluğunu ve fiziksel tutarlılığını test etmek amacıyla p-value < 0.001 anlamlılık düzeyinde Pearson Korelasyon Analizi gerçekleştirilmiştir:

| Değişken İlişkisi | Pearson r | Bilimsel Doğrulama Durumu |
| --- | --- | --- |
| Nihai Risk ↔ n_NDVI | **−0.823** | ✅ Güçlü Negatif — Yeşil alanların karbon riskini düşürdüğü kanıtlandı. |
| Nihai Risk ↔ n_LST | **+0.681** | ✅ Güçlü Pozitif — Yüzey sıcaklığının risk haritasıyla uyumu (UHI Etkisi). |
| Nihai Risk ↔ n_nufus | **+0.611** | ✅ Pozitif — Nüfus yoğunluğunun risk maruziyetini artırdığı doğrulandı. |
| Nihai Risk ↔ n_yol | **+0.607** | ✅ Pozitif — Yol ağının emisyon riskini doğrudan yükselttiği görüldü. |
| Nihai Risk ↔ n_bina | **+0.355** | ✅ Pozitif — Bina hacimsel büyüklüğünün yapısal emisyona katkısı. |
| Nihai Risk ↔ n_trafik | **+0.133** | ✅ Pozitif — Trafik odak noktalarının lokal emisyon etkisi. |
| Nihai Risk ↔ n_otopark | **+0.127** | ✅ Pozitif — Otopark alanlarının bölgesel risk artırıcı etkisi. |
| Nihai Risk ↔ n_sanayi | **+0.103** | ✅ Pozitif — Ticari/endüstriyel parsel emisyon ilişkisi. |

> 📊 **LST ↔ NDVI İlişkisi: r = −0.628** > Bitki örtüsünün yoğun olduğu alanlarda arazi yüzey sıcaklığının düştüğü istatistiksel olarak teyit edilmiştir. Bu durum, uzaktan algılama literatüründeki fiziksel yasalarla tam olarak örtüşmektedir.

---

## 🛠️ 9. Kullanılan Teknolojiler (Tech Stack)

| Kütüphane / Araç | Kullanım Amacı |
| --- | --- |
| `geopandas` | Mekânsal overlay, spatial join, CRS dönüşümleri ve vektör analizi |
| `osmnx` | OpenStreetMap üzerinden hassas kentsel veri madenciliği |
| `rasterio` | Raster verilerin (LST, NDVI, Nüfus) hücre tabanlı örneklenmesi (sampling) |
| `scikit-learn` | Gözetimsiz makine öğrenmesi (K-Means) ve veri standardizasyonu |
| `scipy` | Pearson korelasyon katsayıları ve istatistiksel anlamlılık testleri |
| `pandas` / `numpy` | Tabular veri manipülasyonu, AHP matris matematiği ve normalizasyon |
| **QGIS** | Landsat 9 termal ve optik bant ön işlemesi, kartografik harita tasarımı |

---

## 📊 10. Kentsel Planlama ve Sürdürülebilirlik İçin Karar Destek Çıktıları

Bu modelleme çalışması sonucunda yerel yönetimler (Belediyeler) ve afet yönetim birimleri (AFAD) için uygulanabilir şu stratejik eylem planları haritalandırılmıştır:

1. **Risk Grubu 5 & 6 (Ekstrem ve Kritik Risk) Alanları:** Transit ulaşım ağları (Altınyol) ve gökdelenler/yüksek katlı iş merkezlerinin bulunduğu bölgeler.
* *Öneri:* Bu alanlarda acil dikey yeşil altyapı (yeşil çatı/duvar zorunluluğu), mikroklimatik rüzgar koridorlarının korunması ve emisyon azaltıcı karbon bariyerlerinin uygulanması gerekmektedir.


2. **Risk Grubu 3 & 4 (Kentsel Isı Adaları):** Yapısal yoğunluğun fazla, ağaçlandırmanın yetersiz olduğu betonarme alanlar.
* *Öneri:* Kentsel ısı adası etkisini azaltmak adına cep parkları, mikro ağaçlandırma projeleri ve yollarda/kaldırımlarda yüksek albedolu (yansıtıcı) malzeme kullanımı teşvik edilmelidir.


3. **Sosyal Kırılganlık Kesişimi:** En yüksek karbon riski taşıyan hücreler ile demografik veriler (örneğin 65+ yaş üstü nüfus yoğunluğu) coğrafi olarak çakıştırılarak, iklim krizine karşı **"Acil Müdahale Edilmesi Gereken Öncelikli Sokaklar"** listelenmiştir.

```

```
```

```
