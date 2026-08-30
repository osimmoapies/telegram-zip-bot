# 🧰 FileBox — универсальный файловый Telegram-бот

Пришли файл — получи результат. **23 инструмента**, красивое меню, 3 языка (🇷🇺 🇬🇧 🇹🇯), работает 24/7 бесплатно на GitHub Actions.

> Send a file — get the result. 23 tools, pretty menu, RU/EN/TG, runs 24/7 free on GitHub Actions.

## ✨ Что умеет

- **📄 PDF:** фото→PDF, PDF→фото, объединить, разделить, сжать, повернуть, PDF→текст
- **📝 Документы:** Word/Excel/PowerPoint→PDF, PDF→Word
- **🖼 Картинки:** конвертация (JPG/PNG/WEBP/HEIC…), сжать, изменить размер, фото→GIF, убрать метаданные
- **🗜 Архивы:** файлы→ZIP, распаковать ZIP
- **🔧 Утилиты:** текст→QR, QR→текст, OCR (текст с фото, рус+eng)
- **🎬 Медиа:** видео→GIF, видео→MP3, сжать видео, конвертация аудио

Лимиты Telegram: входящий файл до **20 МБ**, результат до **50 МБ**.

## 🚀 Хостинг: GitHub Actions (бесплатно, 24/7)

Бот живёт прямо в этом репозитории: воркфлоу `.github/workflows/bot.yml` запускает бота в режиме polling, работает ~5ч45м и плавно передаёт смену следующему запуску (без потери сообщений).

**Активация:**
1. Создай бота у [@BotFather](https://t.me/BotFather) → получи токен.
2. Добавь секрет: **Settings → Secrets and variables → Actions → New repository secret**, имя `BOT_TOKEN`, значение — токен.
3. Репозиторий должен быть **публичным** (бесплатные безлимитные минуты Actions).
4. **Actions → filebox → Run workflow** — бот запускается.

> ⚠️ Каждые ~6 часов раннер пересоздаётся и заново ставит движки (LibreOffice и др.) — пересменка занимает ~1-2 мин, 4 раза в сутки. Сообщения в этот момент не теряются: Telegram их запоминает.

## 🖥 Локальный запуск / другой хостинг

```bash
# нужны системные движки: libreoffice poppler-utils ghostscript ffmpeg
#                         tesseract-ocr tesseract-ocr-rus zbar-tools libheif1
pip install -r requirements.txt
export BOT_TOKEN=твой_токен
python bot.py
```
Или через Docker (все движки уже внутри):
```bash
docker build -t filebox . && docker run -e BOT_TOKEN=токен filebox
```

## 🏷 Брендинг
- Имя: **FileBox 🧰**
- Аватар: `assets/avatar.png` (поставить в BotFather: `/setuserpic`)
- Команды: /menu · /language · /help

## 🗂 Структура
- `bot.py` — меню, навигация, сбор файлов, прогресс, отправка
- `converters.py` — все конвертеры + реестр операций
- `i18n.py` — переводы RU/EN/TG
- `.github/workflows/bot.yml` — хостинг 24/7
