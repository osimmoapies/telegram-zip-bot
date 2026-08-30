# -*- coding: utf-8 -*-
"""Translations for the Zip Photo Bot: Russian, English, Tajik."""

LANG_NAMES = {"ru": "Русский", "en": "English", "tg": "Тоҷикӣ"}

TEXTS = {
    "ru": {
        "choose_language": "🌍 <b>Выберите язык</b>\nChoose your language\nЗабонро интихоб кунед",
        "lang_set": "✅ Язык установлен: <b>{name}</b>",
        "instructions": (
            "👋 <b>Привет!</b>\n\n"
            "Отправь мне сколько угодно фотографий 📸, а когда закончишь — "
            "нажми <b>«✅ Готово»</b>.\n\n"
            "Я соберу всё в один <b>.zip</b> архив и пришлю тебе 🎁"
        ),
        "collected": (
            "📸 Собрано фото: <b>{n}</b>\n\n"
            "Продолжай отправлять или нажми <b>«✅ Готово»</b>."
        ),
        "btn_done": "✅ Готово",
        "btn_clear": "🗑 Очистить",
        "btn_lang": "🌐 Язык",
        "no_photos": "🤔 Ты ещё не отправил ни одной фотографии.\nПросто пришли мне фото 📸",
        "cleared": "🗑 Готово, всё очищено. Можешь начинать заново 📸",
        "packing": "📦 Упаковываю фотографии в архив…",
        "packing_frame": "🗜 <b>{stage}</b>\n\n{bar}  <b>{pct}%</b>",
        "stage_collect": "Собираю фотографии…",
        "stage_zip": "Сжимаю в архив…",
        "stage_send": "Отправляю тебе…",
        "done_caption": "🎁 Готово! Твой архив с <b>{n}</b> фото 📸",
        "ready_again": "✨ Можешь отправлять следующую пачку фото!",
        "too_large": (
            "⚠️ Архив получился больше 50 МБ — Telegram не даёт отправить такой файл.\n"
            "Пришли, пожалуйста, меньше фотографий за один раз."
        ),
        "not_a_photo": "🖼 Это не похоже на изображение. Пришли фото 📸",
        "send_photos_hint": "📸 Пришли мне фотографии, а потом нажми <b>«✅ Готово»</b>.",
        "help": (
            "ℹ️ <b>Как пользоваться</b>\n\n"
            "1️⃣ Отправь мне одну или несколько фотографий 📸\n"
            "2️⃣ Нажми <b>«✅ Готово»</b>\n"
            "3️⃣ Получи <b>.zip</b> архив со всеми фото 🎁\n\n"
            "Команды:\n"
            "/start — начать заново\n"
            "/language — сменить язык\n"
            "/help — эта справка"
        ),
    },
    "en": {
        "choose_language": "🌍 <b>Choose your language</b>\nВыберите язык\nЗабонро интихоб кунед",
        "lang_set": "✅ Language set: <b>{name}</b>",
        "instructions": (
            "👋 <b>Hi there!</b>\n\n"
            "Send me as many photos 📸 as you like. When you're done — "
            "tap <b>“✅ Done”</b>.\n\n"
            "I'll pack everything into a single <b>.zip</b> archive and send it back 🎁"
        ),
        "collected": (
            "📸 Photos collected: <b>{n}</b>\n\n"
            "Keep sending, or tap <b>“✅ Done”</b>."
        ),
        "btn_done": "✅ Done",
        "btn_clear": "🗑 Clear",
        "btn_lang": "🌐 Language",
        "no_photos": "🤔 You haven't sent any photos yet.\nJust send me a photo 📸",
        "cleared": "🗑 Done, everything is cleared. You can start again 📸",
        "packing": "📦 Packing your photos into an archive…",
        "packing_frame": "🗜 <b>{stage}</b>\n\n{bar}  <b>{pct}%</b>",
        "stage_collect": "Collecting photos…",
        "stage_zip": "Compressing into archive…",
        "stage_send": "Sending it to you…",
        "done_caption": "🎁 Done! Your archive with <b>{n}</b> photos 📸",
        "ready_again": "✨ You can send the next batch of photos!",
        "too_large": (
            "⚠️ The archive is larger than 50 MB — Telegram won't let me send such a file.\n"
            "Please send fewer photos at once."
        ),
        "not_a_photo": "🖼 That doesn't look like an image. Please send a photo 📸",
        "send_photos_hint": "📸 Send me photos, then tap <b>“✅ Done”</b>.",
        "help": (
            "ℹ️ <b>How to use</b>\n\n"
            "1️⃣ Send me one or more photos 📸\n"
            "2️⃣ Tap <b>“✅ Done”</b>\n"
            "3️⃣ Get a <b>.zip</b> archive with all your photos 🎁\n\n"
            "Commands:\n"
            "/start — start over\n"
            "/language — change language\n"
            "/help — this help"
        ),
    },
    "tg": {
        "choose_language": "🌍 <b>Забонро интихоб кунед</b>\nChoose your language\nВыберите язык",
        "lang_set": "✅ Забон интихоб шуд: <b>{name}</b>",
        "instructions": (
            "👋 <b>Салом!</b>\n\n"
            "Ҳар қадаре, ки хоҳед расм 📸 фиристед, вақте ки тамом шуд — "
            "тугмаи <b>«✅ Тайёр»</b>-ро зер кунед.\n\n"
            "Ман ҳамаашро дар як файли <b>.zip</b> ҷамъ карда, ба шумо мефиристам 🎁"
        ),
        "collected": (
            "📸 Расмҳои ҷамъшуда: <b>{n}</b>\n\n"
            "Давом диҳед ё тугмаи <b>«✅ Тайёр»</b>-ро зер кунед."
        ),
        "btn_done": "✅ Тайёр",
        "btn_clear": "🗑 Тоза кардан",
        "btn_lang": "🌐 Забон",
        "no_photos": "🤔 Шумо ҳанӯз ягон расм нафиристодед.\nФақат ба ман расм фиристед 📸",
        "cleared": "🗑 Тайёр, ҳамааш тоза шуд. Метавонед аз нав оғоз кунед 📸",
        "packing": "📦 Расмҳо бастабандӣ шуда истодаанд…",
        "packing_frame": "🗜 <b>{stage}</b>\n\n{bar}  <b>{pct}%</b>",
        "stage_collect": "Расмҳо ҷамъ шуда истодаанд…",
        "stage_zip": "Ба архив фишурда истодаам…",
        "stage_send": "Ба шумо фиристода истодаам…",
        "done_caption": "🎁 Тайёр! Архиви шумо бо <b>{n}</b> расм 📸",
        "ready_again": "✨ Метавонед дастаи навбатии расмҳоро фиристед!",
        "too_large": (
            "⚠️ Ҳаҷми архив аз 50 МБ зиёд шуд — Telegram чунин файлро намефиристад.\n"
            "Лутфан, дар як маротиба камтар расм фиристед."
        ),
        "not_a_photo": "🖼 Ин ба расм монанд нест. Лутфан расм фиристед 📸",
        "send_photos_hint": "📸 Ба ман расм фиристед, баъд тугмаи <b>«✅ Тайёр»</b>-ро зер кунед.",
        "help": (
            "ℹ️ <b>Тарзи истифода</b>\n\n"
            "1️⃣ Ба ман як ё якчанд расм фиристед 📸\n"
            "2️⃣ Тугмаи <b>«✅ Тайёр»</b>-ро зер кунед\n"
            "3️⃣ Архиви <b>.zip</b>-ро бо ҳамаи расмҳоятон гиред 🎁\n\n"
            "Фармонҳо:\n"
            "/start — аз нав оғоз кардан\n"
            "/language — иваз кардани забон\n"
            "/help — ин кӯмак"
        ),
    },
}

# Every localized button label -> action name (language-independent routing).
BUTTON_ACTIONS = {}
for _lang, _d in TEXTS.items():
    BUTTON_ACTIONS[_d["btn_done"]] = "done"
    BUTTON_ACTIONS[_d["btn_clear"]] = "clear"
    BUTTON_ACTIONS[_d["btn_lang"]] = "lang"


def t(lang, key, **kwargs):
    """Return a translated string, falling back to English, then to the key."""
    table = TEXTS.get(lang, TEXTS["en"])
    text = table.get(key) or TEXTS["en"].get(key, key)
    return text.format(**kwargs) if kwargs else text


def detect_lang(code):
    """Map a Telegram language_code to one of our supported languages."""
    if not code:
        return "en"
    code = code.lower()
    if code.startswith("ru"):
        return "ru"
    if code.startswith("tg") or code.startswith("tj"):
        return "tg"
    return "en"
