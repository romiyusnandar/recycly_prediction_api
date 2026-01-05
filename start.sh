#!/bin/sh
# Start script untuk Render.com
# Render menyediakan PORT env variable (default 10000)

uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}
