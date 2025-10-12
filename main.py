# main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

# Model ve Class Names
MODEL_PATH = os.path.join(os.path.dirname(__file__), "trained_plant_disease_model.keras")
CLASS_NAMES = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 
    'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 
    'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 
    'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 
    'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
    'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 
    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 
    'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 
    'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 
    'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 
    'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

# Model Yükleme
if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"❌ Model dosyası bulunamadı: {MODEL_PATH}")

try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print(f"✅ Model başarıyla yüklendi!")
    print(f"📊 Toplam {len(CLASS_NAMES)} sınıf tanımlı")
except Exception as e:
    raise RuntimeError(f"❌ Model yüklenirken hata: {e}")

# FastAPI Uygulaması
app = FastAPI(title="Plant Disease Recognition API")

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def model_prediction(image_bytes: bytes):
    """Görüntüden hastalık tahmini yapar"""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image = image.resize((128, 128))
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = np.array([input_arr])
        predictions = model.predict(input_arr, verbose=0)
        return np.argmax(predictions), predictions[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Görüntü işlenemedi: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "Plant Disease Recognition API",
        "version": "1.0",
        "endpoints": {
            "/predict": "POST - Hastalık tahmini yap",
            "/health": "GET - Sistem durumu",
            "/classes": "GET - Tüm sınıfları listele"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": True,
        "total_classes": len(CLASS_NAMES)
    }

@app.get("/classes")
async def get_classes():
    return {
        "total_classes": len(CLASS_NAMES),
        "classes": CLASS_NAMES
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Sadece görüntü dosyaları kabul edilir")
    
    image_bytes = await file.read()
    result_index, probabilities = model_prediction(image_bytes)
    
    predicted_class = CLASS_NAMES[result_index]
    confidence = float(probabilities[result_index]) * 100
    
    top_5_indices = np.argsort(probabilities)[-5:][::-1]
    top_5_predictions = [
        {"class": CLASS_NAMES[idx], "confidence": float(probabilities[idx]) * 100}
        for idx in top_5_indices
    ]
    
    return {
        "success": True,
        "prediction": predicted_class,
        "confidence": round(confidence, 2),
        "prediction_index": int(result_index),
        "top_5_predictions": top_5_predictions,
        "message": f"Model is predicting it's a {predicted_class}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
