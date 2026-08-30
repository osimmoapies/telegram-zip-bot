FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

# Conversion engines
RUN apt-get update && apt-get install -y --no-install-recommends \
      libreoffice poppler-utils ghostscript ffmpeg \
      tesseract-ocr tesseract-ocr-rus tesseract-ocr-eng \
      zbar-tools libzbar0 libheif1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["python", "bot.py"]
