# 🚀 Panduan Deploy Recycly API ke PythonAnywhere

## ⚠️ PENTING: Batasan PythonAnywhere Free Tier
- **TensorFlow terlalu berat** untuk free tier PythonAnywhere (terbatas CPU & RAM)
- **Ukuran file** dibatasi 512MB (model Keras Anda mungkin besar)
- **Recommendation**: Gunakan **Render.com**, **Railway.app**, atau **Hugging Face Spaces** untuk aplikasi ML

## Jika tetap ingin mencoba PythonAnywhere:

### 1️⃣ Registrasi & Login
1. Buka https://www.pythonanywhere.com
2. Buat akun gratis (Beginner account)
3. Login ke dashboard

### 2️⃣ Upload Project

**Opsi A: Via Git (Recommended)**
```bash
# Di PythonAnywhere Console
cd ~
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git recycly
cd recycly
```

**Opsi B: Upload Manual**
1. Buka tab **Files**
2. Upload semua file project ke `/home/YOUR_USERNAME/recycly/`
3. Upload folder `app/` dengan semua isinya

### 3️⃣ Setup Virtual Environment
```bash
# Di Bash console PythonAnywhere
cd ~/recycly
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies (ini akan LAMA untuk TensorFlow)
pip install --upgrade pip
pip install -r app/requirements.txt
```

⚠️ **Catatan**: Install TensorFlow bisa gagal di free tier karena memory limit!

### 4️⃣ Konfigurasi Web App

1. Klik tab **Web**
2. Klik **Add a new web app**
3. Pilih **Manual configuration** (bukan Flask/Django)
4. Pilih **Python 3.10**

### 5️⃣ Edit WSGI Configuration

1. Di halaman Web, scroll ke **Code section**
2. Klik link WSGI configuration file (biasanya `/var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py`)
3. **HAPUS semua isi file** dan ganti dengan:

```python
import sys
import os

# Tambahkan project ke path
project_home = '/home/YOUR_USERNAME/recycly'  # ⚠️ GANTI YOUR_USERNAME
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activate virtual environment
activate_this = '/home/YOUR_USERNAME/recycly/venv/bin/activate_this.py'  # ⚠️ GANTI
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Set environment variables
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Import FastAPI app
from app.main import app as application
```

4. **Save file** (Ctrl+S atau tombol Save)

### 6️⃣ Virtualenv Configuration

1. Masih di tab **Web**, scroll ke section **Virtualenv**
2. Masukkan path: `/home/YOUR_USERNAME/recycly/venv`
3. Klik ✅

### 7️⃣ Static Files (Opsional)
Tidak perlu untuk API, skip.

### 8️⃣ Reload & Test

1. Scroll ke atas, klik tombol hijau **Reload YOUR_USERNAME.pythonanywhere.com**
2. Tunggu beberapa detik
3. Klik link **YOUR_USERNAME.pythonanywhere.com** untuk test

4. Test endpoint:
   - GET: `https://YOUR_USERNAME.pythonanywhere.com/`
   - POST: `https://YOUR_USERNAME.pythonanywhere.com/predict`

### 9️⃣ Test API

```bash
# Test root endpoint
curl https://YOUR_USERNAME.pythonanywhere.com/

# Test predict endpoint (dengan file gambar)
curl -X POST "https://YOUR_USERNAME.pythonanywhere.com/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_image.jpg"
```

---

## 🐛 Troubleshooting

### Error: "Application object must be callable"
- Pastikan `from app.main import app as application` benar
- Cek path project sudah benar

### Error: Memory Error / TensorFlow install gagal
- **TensorFlow terlalu berat untuk free tier!**
- Solusi: Gunakan platform lain (Render, Railway, Hugging Face)

### Error: ModuleNotFoundError
- Pastikan virtual environment sudah diaktifkan
- Re-install dependencies: `pip install -r app/requirements.txt`

### Error: Model file not found
- Pastikan `app/model/recycly_model.keras` sudah diupload
- Cek path di `main.py` sudah benar

### Logs tidak muncul
- PythonAnywhere tidak support write ke file di web app
- Ubah logging ke console atau disable

---

## ✅ Alternatif Platform (LEBIH COCOK untuk ML Apps)

### **Render.com** (Recommended)
- Free tier support Docker
- Cukup RAM untuk TensorFlow
- Auto-deploy dari GitHub

### **Railway.app**
- $5 credit gratis
- Support Docker
- Mudah setup

### **Hugging Face Spaces**
- Gratis untuk ML models
- Support Gradio/Streamlit
- Community focused

### **Google Cloud Run**
- Free tier generous
- Serverless, bayar per request
- Support container

---

## 📝 Catatan Penting

1. **Model size**: Cek ukuran `recycly_model.keras` - jika >100MB, compress atau gunakan model quantization
2. **Cold start**: Free tier bisa sleep, API akan lambat saat pertama kali diakses
3. **Request timeout**: PythonAnywhere ada limit 5 menit per request
4. **Disk space**: Free tier hanya 512MB total

---

## 🔗 Useful Links

- PythonAnywhere Help: https://help.pythonanywhere.com/
- PythonAnywhere Forums: https://www.pythonanywhere.com/forums/
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/

---

**Good luck dengan deployment! 🚀**

Jika ada error, cek:
1. Error log di PythonAnywhere Web tab (bagian Log files)
2. Server log: `/var/log/YOUR_USERNAME.pythonanywhere.com.server.log`
3. Error log: `/var/log/YOUR_USERNAME.pythonanywhere.com.error.log`
