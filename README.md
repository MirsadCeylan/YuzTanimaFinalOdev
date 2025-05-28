
# YOLOv8 ile Gerçek Zamanlı Yüz Tanıma

Bu proje, **YOLOv8** modelini kullanarak bir webcam'den gerçek zamanlı yüz tanıma yapmayı amaçlar. Modelin tahminleri her birkaç karede bir gerçekleştirilir ve sonuçlar görselleştirilerek kullanıcıya gösterilir.

## 🧠 Kullanılan Kütüphaneler

- `ultralytics`: YOLOv8 modelini çalıştırmak için
- `cv2 (OpenCV)`: Görüntü işleme ve kamera erişimi için
- `torch (PyTorch)`: Derin öğrenme ve cihaz yönetimi (CPU/GPU) için
- `os`: Dosya kontrolü
- `time`: FPS (frame per second) hesaplaması için

## 🔧 Kurulum

Gerekli kütüphaneleri yüklemek için:

```bash
pip install ultralytics opencv-python torch
```

## 📁 Model Dosyası

Proje klasöründe eğitilmiş bir YOLOv8 model dosyasının (`best (1).pt`) bulunması gerekir. Dosya yoksa çalıştırma sırasında hata alırsınız.

## 🚀 Kodun Açıklaması

### 1. Model ve Cihaz Kurulumu

```python
assert os.path.exists("best (1).pt"), "Model dosyası bulunamadı!"
model = YOLO("best (1).pt")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
```

- Model dosyasının varlığı kontrol edilir.
- Model uygun cihaza (GPU varsa `cuda`, yoksa `cpu`) aktarılır.

### 2. Kamera Ayarları

```python
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
```

- Varsayılan kamera açılır.
- Görüntü çözünürlüğü 480x360 olarak ayarlanır.

### 3. FPS ve Tahmin Sıklığı

```python
predict_every_n_frames = 2
```

- Her 2 karede bir tahmin yapılır. Bu, performansı artırmak içindir.

### 4. Ana Döngü

```python
while cap.isOpened():
    ...
    results = model.predict(...)
    ...
    annotated_frame = last_result.plot() if last_result else frame
```

- Kamera görüntüsü alınır.
- Belirlenen aralıklarda YOLO tahmini yapılır.
- Tahmin sonucu işlenerek görsel üzerine çizilir.
- FPS bilgisi ekrana yazdırılır.

### 5. Çıkış

```python
if cv2.waitKey(1) & 0xFF == ord('q'):
    break
```

- Kullanıcı `q` tuşuna bastığında program sonlandırılır.

## 🖥️ Ekran Görüntüsü

Model tarafından işaretlenmiş yüzlerin görüntüsü ve FPS değeri ekranda canlı olarak gösterilir:

```
-----------------------------
|  FPS: 27                  |
|  [Yüz Kutucukları]       |
|                           |
-----------------------------
```

## ❌ Hata Ayıklama

- `Model dosyası bulunamadı!` → `best (1).pt` dosyasını proje klasörüne eklediğinizden emin olun.
- Webcam çalışmıyorsa: `cap.read()` her zaman `True` döndürmeyebilir. Bağlantıyı kontrol edin.
## ✔ ÖĞRENCİ KONTROL LİSTESİ (Hazırlık + Teknik)
- 1 Proje konusu belirlendi ve yapay zekâ yöntemine karar verildi. Haar, YOLO, Mediapipe vb. yöntemlerden biri seçildi ve README'de belirtildi. |✔|

- 2 Kodlama aşaması tamamlandı ve sistem nesne/özellik tespiti yapabiliyor. Proje kameradan veya görselden veri alabiliyor; en az bir nesneyi başarıyla tespit ediyor. |✔|

- 3 Kullanılan yöntem kod içerisinde açıkça yorumlandı. Kod içindeki açıklamalar, hangi algoritmanın nerede kullanıldığını anlatıyor. |✔|

- 4 Tespit edilen nesne/özellik ekranda işaretleniyor. (bounding box, etiket, vb.) Algoritma çıktısı görsel olarak anlamlı hale getirildi. |✔|

- 5 Çalışma çıktıları kayıt altına alındı. Ekran görüntüleri (.png, .jpg) ve/veya kısa bir tanıtım videosu hazırlandı. |✔|

- 6 GitHub reposu oluşturuldu. Proje klasörü yapılandırıldı. (kod, README, çıktıdosyaları, poster) |✔|

- 7 README.md dosyası eksiksiz hazırlandı. Proje tanıtımı, kurulum talimatları, örnek çıktı ve katkı bilgileri yer alıyor. |✔|

- 8 QR kod üretildi QR, GitHub deposuna veya çıktı görsellerini içeren demo sayfasına yönlendirilmek üzere oluşturuldu. |✔|

- 9 QR kod poster üzerine eklendi A4 veya A3 boyutundaki posterde, QR kod ve üniversite logosu görünür şekilde yer aldı. |✔|

- 10 PDF proje posteri hazırlandı. Poster, proje özeti, ekran görüntüleri, kullanılan algoritmalar ve öğrenci bilgileriyle tamamlandı. |✔|

- 11 GitHub’a poster ve çıktılar yüklendi poster.pdf ve outputs/ klasörü GitHub reposuna eklendi |✔|

- 12 Grup halinde çalışıldıysa katkılar açıkça belirtildi. Her üyenin adı ve görev paylaşımı README’de yer alıyor; her üye GitHub üzerinden en az bir katkı sağladı. |✔|

---
## 📜 Lisans

Bu proje kişisel kullanım içindir. Model ve veri seti lisanslarını kontrol etmeyi unutmayın.
