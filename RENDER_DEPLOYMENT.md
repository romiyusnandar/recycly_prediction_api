# 🚀 Panduan Deploy Recycly API ke Render.com

## ✅ Keuntungan Render.com untuk ML Apps:
- ✅ Free tier cukup RAM untuk TensorFlow
- ✅ Auto-deploy dari GitHub
- ✅ Support Docker (reliable)
- ✅ Free SSL certificate
- ✅ Logs & monitoring built-in

---

## 📋 Langkah-langkah Deployment

### 1️⃣ Push Project ke GitHub

```bash
# Pastikan project sudah di-push ke GitHub
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### 2️⃣ Sign Up / Login ke Render

1. Buka https://render.com
2. Sign up dengan GitHub account (recommended)
3. Authorize Render untuk akses GitHub repo Anda

### 3️⃣ Create New Web Service

1. Di Render Dashboard, klik **New +** → **Web Service**
2. Pilih **Connect a repository**
3. Cari dan pilih repository **recycly** Anda
4. Klik **Connect**

### 4️⃣ Configure Web Service

Isi form dengan konfigurasi berikut:

**Basic Settings:**
- **Name**: `recycly-api` (atau nama lain yang Anda mau)
- **Region**: `Singapore` (paling dekat dengan Indonesia)
- **Branch**: `main` (atau branch yang Anda gunakan)
- **Runtime**: `Docker` (akan otomatis detect Dockerfile)

**Build & Deploy:**
- **Dockerfile Path**: `./Dockerfile` (biarkan default jika Dockerfile di root)
- **Docker Command**: (kosongkan, sudah ada CMD di Dockerfile)

**Instance Type:**
- Pilih **Free** (cukup untuk testing)
- Note: Free tier akan sleep setelah 15 menit tidak ada request

**Environment Variables (Optional):**
Klik **Add Environment Variable** jika perlu:
- Key: `TF_CPP_MIN_LOG_LEVEL`, Value: `2`
- Key: `ENVIRONMENT`, Value: `production`

### 5️⃣ Deploy!

1. Scroll ke bawah
2. Klik **Create Web Service**
3. Render akan mulai:
   - Clone repository
   - Build Docker image (ini akan memakan waktu 5-10 menit untuk TensorFlow)
   - Deploy container

### 6️⃣ Monitor Deployment

Anda akan melihat logs real-time:
```
==> Cloning from https://github.com/YOUR_USERNAME/recycly...
==> Building Docker image...
==> Pulling base image python:3.10-slim...
==> Installing dependencies...
==> Starting service...
==> Your service is live 🎉
```

### 7️⃣ Test API

Setelah deployment selesai (status: **Live**), Anda akan mendapat URL:
```
https://recycly-api.onrender.com
```

**Test endpoints:**

```bash
# Test root endpoint
curl https://recycly-api.onrender.com/

# Test predict endpoint
curl -X POST "https://recycly-api.onrender.com/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_image.jpg"
```

**Atau gunakan browser:**
- Akses: `https://recycly-api.onrender.com/docs`
- Ini akan membuka Swagger UI untuk test API interaktif

---

## 🔧 Konfigurasi Tambahan (Optional)

### Auto-Deploy on Push

Render sudah otomatis setup auto-deploy:
- Setiap `git push` ke branch `main` akan trigger deployment baru
- Tidak perlu konfigurasi tambahan

### Custom Domain

Jika punya domain sendiri:
1. Di Render Dashboard → Service → Settings
2. Scroll ke **Custom Domain**
3. Tambah domain Anda
4. Ikuti instruksi DNS configuration

### Health Check

Render otomatis melakukan health check ke root path `/`
Karena Anda sudah punya endpoint di `/`, ini akan berfungsi otomatis.

### Scaling (Paid Plan)

Free tier cukup untuk testing, tapi jika perlu:
- Upgrade ke Starter ($7/month) untuk:
  - Always-on (tidak sleep)
  - Lebih RAM & CPU
  - Multiple instances

---

## 🐛 Troubleshooting

### Build Failed: Out of Memory

**Solusi 1**: Optimize Dockerfile (sudah optimal)

**Solusi 2**: Upgrade ke Starter plan (lebih RAM saat build)

### Service Timeout / Crashes

**Cek logs**:
1. Di Render Dashboard → Service
2. Tab **Logs**
3. Lihat error message

**Common issues**:
- Model file tidak ditemukan → Pastikan `app/model/recycly_model.keras` ada di repo
- Import error → Cek `requirements.txt` lengkap

### Service Sleep (Free Tier)

Free tier akan sleep setelah 15 menit inactive:
- First request setelah sleep akan lambat (30-60 detik)
- Subsequent requests normal

**Solusi**: Upgrade ke Starter ($7/month) untuk always-on

### API Lambat

**Cold start**: Model loading memakan waktu
- Pertimbangkan lazy loading model
- Atau upgrade ke instance lebih besar

---

## 📊 Monitoring & Logs

### View Logs

**Real-time:**
1. Dashboard → Service → Logs tab
2. Atau gunakan Render CLI

**Download logs:**
- Klik **Download** di pojok kanan atas logs

### Metrics

Dashboard → Service → Metrics:
- CPU usage
- Memory usage
- Request count
- Response time

---

## 💡 Tips & Best Practices

### 1. Environment Variables
Simpan config sensitif di Environment Variables, bukan di code:
```python
import os
THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.70"))
```

### 2. Optimize Model Size
Jika model >100MB:
- Gunakan model quantization
- Atau host model di external storage (S3, Google Cloud Storage)

### 3. Add Health Check Endpoint
Sudah ada di `/` - Good!

### 4. Rate Limiting
Untuk production, tambahkan rate limiting:
```bash
pip install slowapi
```

### 5. CORS (jika ada frontend)
Tambahkan CORS middleware di `main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Atau specify domain frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🔗 Useful Links

- **Render Dashboard**: https://dashboard.render.com
- **Render Docs**: https://render.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Support**: https://render.com/docs/support

---

## 🎯 Summary

**URL API Anda (setelah deploy):**
```
https://recycly-api.onrender.com
```

**Endpoints:**
- `GET /` → Status check
- `POST /predict` → Upload gambar untuk prediksi
- `GET /docs` → Swagger UI (interactive API docs)

**Deploy time:** ~5-10 menit (build Docker + TensorFlow install)

**Status:** Check di https://dashboard.render.com

---

**Selamat deployment! 🚀**

Jika ada pertanyaan atau error, cek logs di Render Dashboard atau tanya saya!
