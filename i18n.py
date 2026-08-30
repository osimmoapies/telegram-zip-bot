# -*- coding: utf-8 -*-
"""Translations for FileBox — Russian, English, Tajik. Clear, simple, no errors."""

LANGS = ("ru", "en", "tg")
LANG_NAMES = {"ru": "Русский", "en": "English", "tg": "Тоҷикӣ"}

# --------------------------------------------------------------------------- #
# UI strings
# --------------------------------------------------------------------------- #
UI = {
    "ru": {
        "choose_language": "🌍 <b>Выберите язык</b>\nChoose your language\nЗабонро интихоб кунед",
        "lang_set": "✅ Язык: <b>{name}</b>",
        "menu_title": "🧰 <b>FileBox</b> — что сделаем с файлом?\nВыбери категорию 👇",
        "cat_title": "<b>{cat}</b>\nВыбери инструмент 👇",
        "pick_param": "⚙️ Выбери вариант:",
        "btn_back": "◀️ Назад",
        "btn_home": "🏠 В меню",
        "btn_run": "▶️ Готово",
        "btn_clear": "🗑 Очистить",
        "btn_lang": "🌐 Язык",
        "btn_help": "❓ Помощь",
        "collected": "📎 Собрано: <b>{n}</b>\nПришли ещё или нажми <b>«▶️ Готово»</b>.",
        "prompt_images": "🖼 Пришли <b>фотографии</b> (сколько нужно), потом нажми <b>«▶️ Готово»</b>.",
        "prompt_image": "🖼 Пришли <b>одно изображение</b>.",
        "prompt_pdf": "📄 Пришли <b>PDF-файл</b>.",
        "prompt_pdfs": "📄 Пришли <b>несколько PDF</b>, потом нажми <b>«▶️ Готово»</b>.",
        "prompt_office": "📝 Пришли <b>документ</b> (Word, Excel, PowerPoint, TXT…).",
        "prompt_files": "📎 Пришли <b>файлы</b> (любые), потом нажми <b>«▶️ Готово»</b>.",
        "prompt_zip": "🗜 Пришли <b>ZIP-архив</b>.",
        "prompt_video": "🎬 Пришли <b>видео</b>.",
        "prompt_audio": "🎵 Пришли <b>аудио</b> или голосовое.",
        "prompt_text": "🔳 Пришли <b>текст или ссылку</b> — сделаю QR-код.",
        "stage_prepare": "Готовлю…",
        "stage_process": "Обрабатываю…",
        "stage_send": "Отправляю…",
        "progress_frame": "⚙️ <b>{stage}</b>\n\n{bar}  <b>{pct}%</b>",
        "result_caption": "🎁 Готово!",
        "result_text": "📝 <b>Результат:</b>",
        "ready_again": "✨ Готово! Выбери следующий инструмент — /menu",
        "err_generic": "😕 Не получилось обработать. Проверь файл и попробуй ещё раз.",
        "err_timeout": "⌛ Обработка заняла слишком долго и была остановлена. Попробуй файл поменьше.",
        "busy": "⏳ Подожди — я ещё обрабатываю предыдущий файл…",
        "err_too_big_in": "⚠️ Файл больше <b>20 МБ</b> — Telegram не даёт мне его скачать. Пришли поменьше.",
        "err_too_big_out": "⚠️ Результат больше <b>50 МБ</b> — не могу отправить. Попробуй сжать/меньше файлов.",
        "err_wrong_type": "🤔 Не тот тип файла. {hint}",
        "err_no_files": "🤔 Ты ещё ничего не прислал.",
        "cleared": "🗑 Очищено.",
        "name_hint": "💡 Можешь прислать своё <b>название файла</b> (например, <code>моё.pdf</code>).",
        "name_set": "✅ Имя файла: <b>{name}</b>",
        "pay_prompt": "🔒 Обработка стоит <b>{stars} ⭐</b>. Оплати, чтобы продолжить 👇",
        "pay_title": "FileBox — обработка файла",
        "pay_desc": "Оплата {stars} ⭐ за одну обработку файла.",
        "pay_label": "1 обработка",
        "pay_thanks": "✅ Оплата получена, спасибо! Обрабатываю…",
        "help": (
            "🧰 <b>FileBox</b> — универсальный файловый мастер.\n\n"
            "Как пользоваться:\n"
            "1️⃣ Открой меню — /menu\n"
            "2️⃣ Выбери категорию и инструмент\n"
            "3️⃣ Пришли файл(ы)\n"
            "4️⃣ Получи готовый результат 🎁\n\n"
            "Команды: /menu · /language · /help\n"
            "Лимит: входящий файл до 20 МБ, результат до 50 МБ."
        ),
    },
    "en": {
        "choose_language": "🌍 <b>Choose your language</b>\nВыберите язык\nЗабонро интихоб кунед",
        "lang_set": "✅ Language: <b>{name}</b>",
        "menu_title": "🧰 <b>FileBox</b> — what shall we do with your file?\nPick a category 👇",
        "cat_title": "<b>{cat}</b>\nPick a tool 👇",
        "pick_param": "⚙️ Choose an option:",
        "btn_back": "◀️ Back",
        "btn_home": "🏠 Menu",
        "btn_run": "▶️ Done",
        "btn_clear": "🗑 Clear",
        "btn_lang": "🌐 Language",
        "btn_help": "❓ Help",
        "collected": "📎 Collected: <b>{n}</b>\nSend more or tap <b>“▶️ Done”</b>.",
        "prompt_images": "🖼 Send <b>photos</b> (as many as you like), then tap <b>“▶️ Done”</b>.",
        "prompt_image": "🖼 Send <b>one image</b>.",
        "prompt_pdf": "📄 Send a <b>PDF file</b>.",
        "prompt_pdfs": "📄 Send <b>several PDFs</b>, then tap <b>“▶️ Done”</b>.",
        "prompt_office": "📝 Send a <b>document</b> (Word, Excel, PowerPoint, TXT…).",
        "prompt_files": "📎 Send <b>files</b> (any), then tap <b>“▶️ Done”</b>.",
        "prompt_zip": "🗜 Send a <b>ZIP archive</b>.",
        "prompt_video": "🎬 Send a <b>video</b>.",
        "prompt_audio": "🎵 Send <b>audio</b> or a voice message.",
        "prompt_text": "🔳 Send <b>text or a link</b> — I'll make a QR code.",
        "stage_prepare": "Preparing…",
        "stage_process": "Processing…",
        "stage_send": "Sending…",
        "progress_frame": "⚙️ <b>{stage}</b>\n\n{bar}  <b>{pct}%</b>",
        "result_caption": "🎁 Done!",
        "result_text": "📝 <b>Result:</b>",
        "ready_again": "✨ Done! Pick the next tool — /menu",
        "err_generic": "😕 Couldn't process it. Check the file and try again.",
        "err_timeout": "⌛ Processing took too long and was stopped. Try a smaller file.",
        "busy": "⏳ Please wait — I'm still processing your previous file…",
        "err_too_big_in": "⚠️ The file is over <b>20 MB</b> — Telegram won't let me download it. Send a smaller one.",
        "err_too_big_out": "⚠️ The result is over <b>50 MB</b> — I can't send it. Try compressing / fewer files.",
        "err_wrong_type": "🤔 Wrong file type. {hint}",
        "err_no_files": "🤔 You haven't sent anything yet.",
        "cleared": "🗑 Cleared.",
        "name_hint": "💡 You can send a custom <b>file name</b> (e.g. <code>my.pdf</code>).",
        "name_set": "✅ File name: <b>{name}</b>",
        "pay_prompt": "🔒 Processing costs <b>{stars} ⭐</b>. Pay to continue 👇",
        "pay_title": "FileBox — file processing",
        "pay_desc": "Pay {stars} ⭐ for one file processing.",
        "pay_label": "1 processing",
        "pay_thanks": "✅ Payment received, thanks! Processing…",
        "help": (
            "🧰 <b>FileBox</b> — your universal file master.\n\n"
            "How to use:\n"
            "1️⃣ Open the menu — /menu\n"
            "2️⃣ Pick a category and a tool\n"
            "3️⃣ Send your file(s)\n"
            "4️⃣ Get the result 🎁\n\n"
            "Commands: /menu · /language · /help\n"
            "Limits: incoming file up to 20 MB, result up to 50 MB."
        ),
    },
    "tg": {
        "choose_language": "🌍 <b>Забонро интихоб кунед</b>\nChoose your language\nВыберите язык",
        "lang_set": "✅ Забон: <b>{name}</b>",
        "menu_title": "🧰 <b>FileBox</b> — бо файл чӣ кор кунем?\nКатегорияро интихоб кунед 👇",
        "cat_title": "<b>{cat}</b>\nАбзорро интихоб кунед 👇",
        "pick_param": "⚙️ Вариантро интихоб кунед:",
        "btn_back": "◀️ Бозгашт",
        "btn_home": "🏠 Меню",
        "btn_run": "▶️ Тайёр",
        "btn_clear": "🗑 Тоза кардан",
        "btn_lang": "🌐 Забон",
        "btn_help": "❓ Кӯмак",
        "collected": "📎 Ҷамъшуда: <b>{n}</b>\nБоз фиристед ё <b>«▶️ Тайёр»</b>-ро зер кунед.",
        "prompt_images": "🖼 <b>Расмҳо</b> фиристед (ҳар қадар лозим), баъд <b>«▶️ Тайёр»</b>-ро зер кунед.",
        "prompt_image": "🖼 <b>Як расм</b> фиристед.",
        "prompt_pdf": "📄 Файли <b>PDF</b> фиристед.",
        "prompt_pdfs": "📄 <b>Якчанд PDF</b> фиристед, баъд <b>«▶️ Тайёр»</b>-ро зер кунед.",
        "prompt_office": "📝 <b>Ҳуҷҷат</b> фиристед (Word, Excel, PowerPoint, TXT…).",
        "prompt_files": "📎 <b>Файлҳо</b> (ҳар гуна) фиристед, баъд <b>«▶️ Тайёр»</b>-ро зер кунед.",
        "prompt_zip": "🗜 <b>Архиви ZIP</b> фиристед.",
        "prompt_video": "🎬 <b>Видео</b> фиристед.",
        "prompt_audio": "🎵 <b>Аудио</b> ё паёми овозӣ фиристед.",
        "prompt_text": "🔳 <b>Матн ё пайванд</b> фиристед — QR-код месозам.",
        "stage_prepare": "Омода мекунам…",
        "stage_process": "Коркард мекунам…",
        "stage_send": "Мефиристам…",
        "progress_frame": "⚙️ <b>{stage}</b>\n\n{bar}  <b>{pct}%</b>",
        "result_caption": "🎁 Тайёр!",
        "result_text": "📝 <b>Натиҷа:</b>",
        "ready_again": "✨ Тайёр! Абзори навбатиро интихоб кунед — /menu",
        "err_generic": "😕 Коркард нашуд. Файлро санҷед ва боз кӯшиш кунед.",
        "err_timeout": "⌛ Коркард хеле тӯл кашид ва қатъ шуд. Файли хурдтарро кӯшиш кунед.",
        "busy": "⏳ Лутфан интизор шавед — ман ҳанӯз файли қаблиро коркард мекунам…",
        "err_too_big_in": "⚠️ Файл аз <b>20 МБ</b> зиёд аст — Telegram ба ман иҷозаи боргирӣ намедиҳад. Хурдтарашро фиристед.",
        "err_too_big_out": "⚠️ Натиҷа аз <b>50 МБ</b> зиёд аст — фиристода наметавонам. Фишурда кунед ё камтар файл.",
        "err_wrong_type": "🤔 Навъи файл нодуруст аст. {hint}",
        "err_no_files": "🤔 Шумо ҳанӯз чизе нафиристодед.",
        "cleared": "🗑 Тоза шуд.",
        "name_hint": "💡 Метавонед <b>номи файл</b>-ро фиристед (мисол: <code>ман.pdf</code>).",
        "name_set": "✅ Номи файл: <b>{name}</b>",
        "pay_prompt": "🔒 Коркард <b>{stars} ⭐</b> меарзад. Барои идома пардохт кунед 👇",
        "pay_title": "FileBox — коркарди файл",
        "pay_desc": "Пардохти {stars} ⭐ барои як коркард.",
        "pay_label": "1 коркард",
        "pay_thanks": "✅ Пардохт қабул шуд, ташаккур! Коркард мекунам…",
        "help": (
            "🧰 <b>FileBox</b> — устоди универсалии файлҳо.\n\n"
            "Тарзи истифода:\n"
            "1️⃣ Менюро кушоед — /menu\n"
            "2️⃣ Категория ва абзорро интихоб кунед\n"
            "3️⃣ Файл(ҳо)ро фиристед\n"
            "4️⃣ Натиҷаро гиред 🎁\n\n"
            "Фармонҳо: /menu · /language · /help\n"
            "Маҳдудият: файли воридотӣ то 20 МБ, натиҷа то 50 МБ."
        ),
    },
}

# --------------------------------------------------------------------------- #
# Category labels
# --------------------------------------------------------------------------- #
CATS = {
    "pdf": {"ru": "📄 PDF", "en": "📄 PDF", "tg": "📄 PDF"},
    "office": {"ru": "📝 Документы", "en": "📝 Documents", "tg": "📝 Ҳуҷҷатҳо"},
    "image": {"ru": "🖼 Картинки", "en": "🖼 Images", "tg": "🖼 Расмҳо"},
    "archive": {"ru": "🗜 Архивы", "en": "🗜 Archives", "tg": "🗜 Архивҳо"},
    "utils": {"ru": "🔧 Утилиты", "en": "🔧 Utilities", "tg": "🔧 Абзорҳо"},
    "media": {"ru": "🎬 Медиа", "en": "🎬 Media", "tg": "🎬 Медиа"},
}

# --------------------------------------------------------------------------- #
# Operation labels
# --------------------------------------------------------------------------- #
OPS = {
    "photos_to_pdf": {"ru": "🖼→📄 Фото в PDF", "en": "🖼→📄 Photos to PDF", "tg": "🖼→📄 Акс ба PDF"},
    "pdf_to_images": {"ru": "📄→🖼 PDF в фото", "en": "📄→🖼 PDF to images", "tg": "📄→🖼 PDF ба акс"},
    "merge_pdf": {"ru": "🔗 Объединить PDF", "en": "🔗 Merge PDF", "tg": "🔗 Муттаҳиди PDF"},
    "split_pdf": {"ru": "✂️ Разделить PDF", "en": "✂️ Split PDF", "tg": "✂️ Ҷудо кардани PDF"},
    "compress_pdf": {"ru": "🗜 Сжать PDF", "en": "🗜 Compress PDF", "tg": "🗜 Фишурдани PDF"},
    "rotate_pdf": {"ru": "🔄 Повернуть PDF", "en": "🔄 Rotate PDF", "tg": "🔄 Гардондани PDF"},
    "pdf_to_text": {"ru": "🔤 PDF в текст", "en": "🔤 PDF to text", "tg": "🔤 PDF ба матн"},
    "office_to_pdf": {"ru": "📘 Office в PDF", "en": "📘 Office to PDF", "tg": "📘 Office ба PDF"},
    "pdf_to_word": {"ru": "📄→📘 PDF в Word", "en": "📄→📘 PDF to Word", "tg": "📄→📘 PDF ба Word"},
    "image_convert": {"ru": "🔄 Конвертировать", "en": "🔄 Convert format", "tg": "🔄 Табдил додан"},
    "compress_image": {"ru": "🗜 Сжать фото", "en": "🗜 Compress image", "tg": "🗜 Фишурдани акс"},
    "resize_image": {"ru": "📐 Изменить размер", "en": "📐 Resize", "tg": "📐 Тағйири андоза"},
    "images_to_gif": {"ru": "🎞 Фото в GIF", "en": "🎞 Photos to GIF", "tg": "🎞 Акс ба GIF"},
    "strip_exif": {"ru": "🧹 Убрать метаданные", "en": "🧹 Strip metadata", "tg": "🧹 Пок кардани EXIF"},
    "remove_bg": {"ru": "🪄 Убрать фон", "en": "🪄 Remove background", "tg": "🪄 Хориҷи замина"},
    "files_to_zip": {"ru": "📦 Файлы в ZIP", "en": "📦 Files to ZIP", "tg": "📦 Файлҳо ба ZIP"},
    "unzip": {"ru": "📂 Распаковать ZIP", "en": "📂 Unzip", "tg": "📂 Кушодани ZIP"},
    "text_to_qr": {"ru": "🔳 Текст в QR", "en": "🔳 Text to QR", "tg": "🔳 Матн ба QR"},
    "qr_to_text": {"ru": "📷 QR в текст", "en": "📷 QR to text", "tg": "📷 QR ба матн"},
    "ocr_image": {"ru": "👁 Текст с фото", "en": "👁 Image to text", "tg": "👁 Матн аз акс"},
    "video_to_gif": {"ru": "🎥 Видео в GIF", "en": "🎥 Video to GIF", "tg": "🎥 Видео ба GIF"},
    "video_to_audio": {"ru": "🔇 Видео в MP3", "en": "🔇 Video to MP3", "tg": "🔇 Видео ба MP3"},
    "compress_video": {"ru": "🗜 Сжать видео", "en": "🗜 Compress video", "tg": "🗜 Фишурдани видео"},
    "audio_convert": {"ru": "🎵 Конверт. аудио", "en": "🎵 Convert audio", "tg": "🎵 Табдили аудио"},
}


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def t(lang, key, **kwargs):
    table = UI.get(lang, UI["en"])
    text = table.get(key) or UI["en"].get(key, key)
    return text.format(**kwargs) if kwargs else text


def cat_label(lang, cat):
    return CATS.get(cat, {}).get(lang) or CATS.get(cat, {}).get("en", cat)


def op_label(lang, op_id):
    return OPS.get(op_id, {}).get(lang) or OPS.get(op_id, {}).get("en", op_id)


def prompt_for(lang, input_kind):
    return t(lang, f"prompt_{input_kind}")


def detect_lang(code):
    if not code:
        return "en"
    code = code.lower()
    if code.startswith("ru"):
        return "ru"
    if code.startswith("tg") or code.startswith("tj"):
        return "tg"
    return "en"
