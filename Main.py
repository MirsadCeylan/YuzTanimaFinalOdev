# Gerekli kütüphaneleri projeye dahil ediyoruz
from ultralytics import YOLO   # YOLOv8 modelini çalıştırmak için
import cv2                     # Görüntü işleme için OpenCV
import time                   # FPS hesaplaması için zaman modülü
import torch                  # PyTorch: modelin çalışacağı cihazı ayarlamak için
import os                     # Dosya kontrolleri yapmak için

# Eğitilmiş model dosyasının varlığını kontrol ediyoruz
assert os.path.exists("best (1).pt"), "Model dosyası bulunamadı!"

# YOLOv8 modelini yüklüyoruz (önceden eğitilmiş .pt dosyası)
model = YOLO("best (1).pt")

# CUDA (GPU) varsa onu kullan, yoksa CPU kullan
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)  # Modeli ilgili cihaza taşıyoruz
print(f"Model is using device: {device}")

# Kamerayı başlatıyoruz (0 = varsayılan kamera)
cap = cv2.VideoCapture(0)

# Kameranın çözünürlüğünü ayarlıyoruz (480x360)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

# FPS hesaplaması için zaman ölçüm değişkenleri
prev_time = time.time()
predict_every_n_frames = 2  # Her 2 karede bir tahmin yapılacak
frame_count = 0
fps_list = []
last_result = None  # Son tahmin sonucu burada tutulur

# Sonsuz döngü ile sürekli kamera görüntüsü işlenir
try:
    while cap.isOpened():
        ret, frame = cap.read()  # Yeni kareyi al
        if not ret:
            break  # Eğer kare alınamazsa çık

        # FPS hesaplaması
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time
        fps_list.append(fps)
        if len(fps_list) > 30:
            fps_list.pop(0)  # FPS listesini 30 ile sınırla
        avg_fps = sum(fps_list) / len(fps_list)

        # Sadece her predict_every_n_frames adımda bir tahmin yap
        if frame_count % predict_every_n_frames == 0:
            with torch.no_grad():  # Geriye dönük hesaplama yapılmasın (hız için)
                results = model.predict(
                    source=frame,     # Kamera görüntüsü
                    imgsz=640,        # Görsel boyutu
                    conf=0.7,         # Güven eşiği (%70 ve üzeri)
                    stream=True       # Stream ile verimli kullanım
                )
                last_result = next(results)  # İlk sonucu al (tek görüntü olduğu için)

        frame_count += 1  # Her karede sayacı artır
        # Eğer bir tahmin sonucu varsa, görüntüyü işaretle
        annotated_frame = last_result.plot() if last_result else frame

        # Görüntüye FPS bilgisini yaz
        cv2.putText(
            annotated_frame,
            f"FPS: {int(avg_fps)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # İşlenmiş görüntüyü pencereye göster
        cv2.imshow("Yolov8 Ile Yüz Tanıma", annotated_frame)

        # 'q' tuşuna basılırsa döngüden çık
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Kamera ve pencereyi serbest bırak (her durumda çalışır)
finally:
    cap.release()
    cv2.destroyAllWindows()
