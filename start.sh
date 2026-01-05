#!/bin/sh
# Start script untuk Render.com
# Menggunakan PORT environment variable dari Render

PORT=${PORT:-8000}
uvicorn app.main:app --host 0.0.0.0 --port $PORT
