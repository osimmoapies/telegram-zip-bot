# 📸➡️🗜 Zip Photo Bot

Telegram-бот, который принимает **сколько угодно фотографий** и по кнопке **«✅ Готово»** отдаёт один **.zip** архив.
Работает 24/7 в облаке (даже когда компьютер выключен). Три языка: 🇷🇺 Русский · 🇬🇧 English · 🇹🇯 Тоҷикӣ.

> A Telegram bot: send as many photos as you want, tap **Done**, get a **.zip** back. Runs 24/7 in the cloud. Multilingual (RU/EN/TG).

---

## 🇷🇺 Русский

### Что делает
1. Пользователь открывает бота и выбирает язык.
2. Кидает любое количество фото 📸 (бот показывает счётчик «Собрано: N»).
3. Нажимает **«✅ Готово»** — бот присылает `.zip` со всеми фото.
4. Кнопка **«🗑 Очистить»** сбрасывает набор, **«🌐 Язык»** меняет язык.

### Шаг 1. Создать бота и получить токен
1. Открой в Telegram [@BotFather](https://t.me/BotFather).
2. Отправь `/newbot`, придумай имя и username (заканчивается на `bot`).
3. BotFather пришлёт **токен** вида `123456:ABC...` — сохрани его.

### Шаг 2. Задеплоить (бесплатно, работает 24/7)

**Вариант A — Koyeb (рекомендую: бесплатно, без карты, не «засыпает»)**
1. Залей этот код на GitHub (см. ниже «Публикация на GitHub»).
2. Зайди на [koyeb.com](https://www.koyeb.com) → **Create Service** → **GitHub** → выбери репозиторий.
3. Тип билда: **Dockerfile**. Порт: **8000**.
4. В разделе **Environment variables** добавь `BOT_TOKEN` = твой токен.
5. **Deploy**. Через минуту бот в сети. ✅

**Вариант B — Render (бесплатно, но «засыпает» и просыпается ~30 сек при новом сообщении)**
1. Залей код на GitHub.
2. [render.com](https://render.com) → **New** → **Blueprint** → выбери репозиторий (там уже есть `render.yaml`).
3. Добавь переменную `BOT_TOKEN`. Render сам включит режим webhook.

**Вариант C — Railway** (`railway.app`): New Project → Deploy from GitHub → добавь `BOT_TOKEN`. Просто, но платно после пробного кредита.

### Запуск локально (для теста)
```bash
pip install -r requirements.txt
export BOT_TOKEN=твой_токен      # Windows: set BOT_TOKEN=...
python bot.py
```

### Публикация на GitHub
```bash
cd telegram-zip-bot
git init && git add . && git commit -m "Zip photo bot"
gh repo create telegram-zip-bot --public --source=. --push
```

---

## 🇬🇧 English

**What it does:** users send any number of photos, tap **Done**, and get a single `.zip`.

**1) Get a token** from [@BotFather](https://t.me/BotFather) (`/newbot`).
**2) Deploy free & always-on:**
- **Koyeb** (recommended, free, no card): Create Service → GitHub → Dockerfile → port `8000` → add env `BOT_TOKEN` → Deploy.
- **Render** (free, sleeps): New → Blueprint (uses `render.yaml`) → add `BOT_TOKEN`.
- **Railway**: Deploy from GitHub → add `BOT_TOKEN`.
**3) Run locally:** `pip install -r requirements.txt` then `BOT_TOKEN=... python bot.py`.

---

## 🇹🇯 Тоҷикӣ

**Чӣ кор мекунад:** корбар ҳар қадар расм мефиристад, тугмаи **«Тайёр»**-ро зер мекунад ва як файли `.zip` мегирад.

**1) Токен гиред** аз [@BotFather](https://t.me/BotFather) (`/newbot`).
**2) Ройгон ва доимӣ ҷойгир кунед:**
- **Koyeb** (тавсия, ройгон, бе корт): Create Service → GitHub → Dockerfile → порт `8000` → тағйирёбандаи `BOT_TOKEN`-ро илова кунед → Deploy.
- **Render** (ройгон, вале «хоб меравад»): New → Blueprint (`render.yaml`) → `BOT_TOKEN`.
**3) Дар компютер:** `pip install -r requirements.txt`, баъд `BOT_TOKEN=... python bot.py`.

---

## ⚙️ Переменные окружения / Environment variables

| Переменная      | Обязательна | Описание |
|-----------------|:-----------:|----------|
| `BOT_TOKEN`     | ✅ да       | Токен от @BotFather |
| `PORT`          | авто        | Порт health/webhook сервера (задаёт хостинг) |
| `WEBHOOK_URL`   | нет         | Включает режим webhook вручную (на Render определяется автоматически) |

## ℹ️ Заметки
- Лимит Telegram на отправку файла — **50 МБ**. Если фото много и они тяжёлые, бот попросит отправить меньше за раз.
- Фото хранятся во временной папке только до отправки архива, затем удаляются.
- Сессии хранятся в памяти: после перезапуска хостинга незавершённые наборы очищаются (это нормально).
