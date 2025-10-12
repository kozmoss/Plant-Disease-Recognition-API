# 🌿 Plant Disease Recognition API

Deep Learning tabanlı bitki hastalığı tespit sistemi. 38 farklı bitki hastalığını %95+ doğrulukla tespit eder.

## 🎯 Özellikler

- ✅ 38 farklı bitki hastalığı sınıfı
- ✅ FastAPI ile RESTful API
- ✅ Apple M1/M2 Metal GPU desteği
- ✅ Swagger UI dokümantasyonu
- ✅ Docker desteği
- ✅ AWS deployment ready

## 🌱 Desteklenen Bitkiler

- 🍎 Apple, 🫐 Blueberry, 🍒 Cherry
- 🌽 Corn (Maize), 🍇 Grape, 🍊 Orange
- 🍑 Peach, 🌶️ Pepper, 🥔 Potato
- 🫐 Raspberry, 🫘 Soybean, 🥒 Squash
- 🍓 Strawberry, 🍅 Tomato

## 🚀 Hızlı Başlangıç

### Gereksinimler

- Python 3.10+
- 4GB+ RAM
- Model dosyası (90MB)

### Kurulum

```bash
# 1. Repoyu klonlayın
git clone https://github.com/your-username/plant-disease-api.git
cd plant-disease-api

# 2. Virtual environment oluşturun
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 3. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 4. Model dosyasını indirin
# Model dosyasını releases sayfasından indirip proje klasörüne koyun

# 5. API'yi başlatın
python main.py
```

API şu adreste çalışacak: http://localhost:8000

## 📚 API Dokümantasyonu

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 Endpoints

### GET `/`
API bilgisi ve endpoint listesi

### GET `/health`
API sistem durumu

```json
{
  "status": "healthy",
  "model_loaded": true,
  "tensorflow_version": "2.16.1",
  "total_classes": 38
}
```

### GET `/classes`
Tüm hastalık sınıflarını listele

### POST `/predict`
Bitki yaprak görselinden hastalık tahmini

**Request:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@leaf_image.jpg"
```

**Response:**
```json
{
  "success": true,
  "prediction": "Tomato___Late_blight",
  "confidence": 98.45,
  "prediction_index": 30,
  "top_5_predictions": [
    {
      "class": "Tomato___Late_blight",
      "confidence": 98.45
    },
    ...
  ],
  "message": "Model is predicting it's a Tomato___Late_blight"
}
```

## 🐳 Docker ile Çalıştırma

```bash
# Image oluştur
docker build -t plant-disease-api .

# Container çalıştır
docker run -p 8000:8000 plant-disease-api

# Docker Compose ile
docker-compose up
```

## ☁️ AWS Deployment

### EC2

```bash
# 1. EC2 instance oluşturun (Ubuntu 22.04, t3.medium)
# 2. Security Group: Port 8000'i açın
# 3. Bağlanın
ssh -i key.pem ubuntu@ec2-ip

# 4. Deploy script'i çalıştırın
bash ec2_setup.sh
```

Detaylı AWS deployment dökümanı için [AWS_DEPLOYMENT.md](AWS_DEPLOYMENT.md) dosyasına bakın.

## 🧪 Test

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Tahmin
with open("leaf.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/predict", files=files)
    print(response.json())
```

## 📊 Model Detayları

- **Mimari**: CNN (Convolutional Neural Network)
- **Input Size**: 128x128x3
- **Classes**: 38
- **Doğruluk**: ~95%
- **Model Size**: 90MB
- **Framework**: TensorFlow 2.16.1 + Keras 3.x

## 🛠️ Teknolojiler

- **Backend**: FastAPI 0.104.1
- **ML Framework**: TensorFlow 2.16.1
- **Image Processing**: Pillow 10.1.0
- **Server**: Uvicorn
- **Python**: 3.10+

## 📝 Versiyon Geçmişi

### v1.0.0 (2025-10-12)
- ✅ İlk release
- ✅ 38 hastalık sınıfı desteği
- ✅ FastAPI entegrasyonu
- ✅ Docker desteği

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📄 Lisans

MIT License - detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 👨‍💻 Geliştirici

Samet - [GitHub](https://github.com/your-username)

## 🙏 Teşekkürler

- PlantVillage Dataset
- TensorFlow Team
- FastAPI Community

---

⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!