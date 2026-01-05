import os

# Suppress TensorFlow info messages (only show warnings and errors)
if 'TF_CPP_MIN_LOG_LEVEL' not in os.environ:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from fastapi import FastAPI, UploadFile, File
import tensorflow as tf
import numpy as np
from PIL import Image
import logging
import io
from datetime import datetime

# =========================
# CONFIG
# =========================
MODEL_PATH = "app/model/recycly_model.keras"
IMG_SIZE = (224, 224)
CONFIDENCE_THRESHOLD = 0.70

CLASS_NAMES = [
    "BotolRecycle",
    "DamagedBottle",
    "FullBottle",
    "NonBotol"
]

# =========================
# LOGGING SETUP
# =========================
logging.basicConfig(
    filename="app/logs/predictions.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

# =========================
# LOAD MODEL (ONCE)
# =========================
model = tf.keras.models.load_model(MODEL_PATH)

# =========================
# FASTAPI APP
# =========================
app = FastAPI(title="Recycly Image Classification API")

# =========================
# UTILS
# =========================
def preprocess_image(file_bytes):
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    image = image.resize(IMG_SIZE)
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# =========================
# ROUTES
# =========================
@app.get("/")
def root():
    return {
        "status": "API is running",
        "Author": "Romi Yusnandar"
        }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = preprocess_image(image_bytes)

    preds = model.predict(image)
    confidence = float(np.max(preds))
    class_index = int(np.argmax(preds))

    if confidence < CONFIDENCE_THRESHOLD:
        predicted_class = "Uncertain"
    else:
        predicted_class = CLASS_NAMES[class_index]

    # Logging
    logging.info(
        f"filename={file.filename} | "
        f"class={predicted_class} | "
        f"confidence={confidence:.4f}"
    )

    return {
        "predicted_class": predicted_class,
        "confidence": round(confidence, 4),
        "threshold": CONFIDENCE_THRESHOLD
    }
