# -*- coding: utf-8 -*-
"""Translations for FileBox — Russian, English, Tajik. Clear, simple, no errors."""

LANGS = ("ru", "en", "tg", "uz")
LANG_NAMES = {"ru": "Русский", "en": "English", "tg": "Тоҷикӣ", "uz": "O'zbekcha"}

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
        "prompt_image": "🖼 Пришли <b>одну фотографию</b>.",
        "prompt_pdf": "📄 Пришли <b>PDF-файл</b>.",
        "prompt_pdfs": "📄 Пришли <b>несколько PDF</b>, потом нажми <b>«▶️ Готово»</b>.",
        "prompt_office": "📝 Пришли <b>документ</b> (Word, Excel, PowerPoint, TXT…).",
        "prompt_files": "📎 Пришли <b>файлы</b> (любые), потом нажми <b>«▶️ Готово»</b>.",
        "prompt_zip": "🗜 Пришли <b>ZIP-архив</b>.",
        "prompt_video": "🎬 Пришли <b>видео</b>.",
        "prompt_audio": "🎵 Пришли <b>аудио</b> или голосовое.",
        "prompt_text": "🔳 Пришли <b>текст или ссылку</b> — сделаю QR-код.",
        "prompt_any": "📎 Пришли <b>любой файл</b>.",
        "stage_prepare": "Готовлю…",
        "stage_process": "Обрабатываю…",
        "stage_send": "Отправляю…",
        "progress_frame": "⚙️ <b>{stage}</b>\n\n{bar}  <b>{pct}%</b>",
        "result_caption": "🎁 Готово!",
        "result_text": "📝 <b>Результат:</b>",
        "ready_again": "✨ Готово! Выбери следующий инструмент — /menu",
        "err_generic": "😕 Не получилось обработать. Проверь файл и попробуй ещё раз.",
        "err_timeout": "⌛ Обработка заняла слишком долго и была остановлена. Попробуй файл поменьше.",
        "err_rate": "🚦 Слишком много обработок за час. Подожди немного и попробуй снова.",
        "pay_refunded": "↩️ Задача была отменена, поэтому я вернул тебе звёзды. Начни заново — /menu",
        "busy": "⏳ Подожди — я ещё обрабатываю предыдущий файл…",
        "err_too_big_in": "⚠️ Файл больше <b>20 МБ</b> — Telegram не даёт мне его скачать. Пришли поменьше.",
        "err_too_big_out": "⚠️ Результат больше <b>50 МБ</b> — не могу отправить. Попробуй сжать/меньше файлов.",
        "err_wrong_type": "🤔 Не тот тип файла. Нужно прислать: {hint}",
        "err_no_files": "🤔 Ты ещё ничего не прислал.",
        "cleared": "🗑 Очищено.",
        "name_hint": "💡 Можешь прислать своё <b>название файла</b> (например, <code>моё.pdf</code>).",
        "name_set": "✅ Имя файла: <b>{name}</b>",
        "pay_prompt": "🔒 Обработка стоит <b>{stars} ⭐</b>. Оплати, чтобы продолжить 👇",
        "pay_title": "FileBox — обработка файла",
        "pay_desc": "Оплата {stars} ⭐ за одну обработку файла.",
        "pay_label": "1 обработка",
        "pay_thanks": "✅ Оплата получена, спасибо! Обрабатываю…",
        "pack_offer": "💡 Часто пользуешься? Пакет выгоднее:",
        "pack_button": "🎟 {n} обработок за {price} ⭐",
        "pack_title": "FileBox — пакет обработок",
        "pack_desc": "{n} обработок за {price} ⭐.",
        "pack_label": "{n} обработок",
        "pack_added": "🎟 +{n} обработок зачислено! На балансе: <b>{credits}</b>. Просто пришли файл 🎁",
        "credit_used": "🎟 Списана 1 обработка из пакета. Остаток: <b>{credits}</b>.",
        "err_fraud": "🚫 Слишком много возвратов — оплата временно недоступна.",
        "free_used": "🆓 Бесплатная обработка ({left} осталось на этой неделе).",
        "share_button": "📤 Поделиться",
        "share_text": "Конвертирую любые файлы бесплатно в Telegram 👉",
        "ref_reward": "🎁 Твой друг воспользовался ботом — тебе +{n} бесплатных обработок!",
        "help": (
            "🧰 <b>FileBox</b> — универсальный файловый мастер.\n\n"
            "Как пользоваться:\n"
            "1️⃣ Открой меню — /menu\n"
            "2️⃣ Выбери категорию и инструмент\n"
            "3️⃣ Пришли файл(ы)\n"
            "4️⃣ Получи готовый результат 🎁\n\n"
            "Команды: /menu · /language · /help\n"
            "Лимит: входящий файл до 20 МБ, результат до 50 МБ.\n"
            "💫 Бесплатно для избранных; остальным — {stars} ⭐ за обработку.\n"
            "✏️ Пришли текст-сообщение, чтобы задать имя файла (например, моё.pdf)."
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
        "prompt_any": "📎 Send <b>any file</b>.",
        "stage_prepare": "Preparing…",
        "stage_process": "Processing…",
        "stage_send": "Sending…",
        "progress_frame": "⚙️ <b>{stage}</b>\n\n{bar}  <b>{pct}%</b>",
        "result_caption": "🎁 Done!",
        "result_text": "📝 <b>Result:</b>",
        "ready_again": "✨ Done! Pick the next tool — /menu",
        "err_generic": "😕 Couldn't process it. Check the file and try again.",
        "err_timeout": "⌛ Processing took too long and was stopped. Try a smaller file.",
        "err_rate": "🚦 Too many conversions this hour. Please wait a bit and try again.",
        "pay_refunded": "↩️ The job was cancelled, so I refunded your Stars. Start again — /menu",
        "busy": "⏳ Please wait — I'm still processing your previous file…",
        "err_too_big_in": "⚠️ The file is over <b>20 MB</b> — Telegram won't let me download it. Send a smaller one.",
        "err_too_big_out": "⚠️ The result is over <b>50 MB</b> — I can't send it. Try compressing / fewer files.",
        "err_wrong_type": "🤔 Wrong file type. Please send: {hint}",
        "err_no_files": "🤔 You haven't sent anything yet.",
        "cleared": "🗑 Cleared.",
        "name_hint": "💡 You can send a custom <b>file name</b> (e.g. <code>my.pdf</code>).",
        "name_set": "✅ File name: <b>{name}</b>",
        "pay_prompt": "🔒 Processing costs <b>{stars} ⭐</b>. Pay to continue 👇",
        "pay_title": "FileBox — file processing",
        "pay_desc": "Pay {stars} ⭐ for one file processing.",
        "pay_label": "1 processing",
        "pay_thanks": "✅ Payment received, thanks! Processing…",
        "pack_offer": "💡 Use it often? A pack is cheaper:",
        "pack_button": "🎟 {n} conversions for {price} ⭐",
        "pack_title": "FileBox — conversion pack",
        "pack_desc": "{n} conversions for {price} ⭐.",
        "pack_label": "{n} conversions",
        "pack_added": "🎟 +{n} conversions added! Balance: <b>{credits}</b>. Just send a file 🎁",
        "credit_used": "🎟 Used 1 conversion from your pack. Left: <b>{credits}</b>.",
        "err_fraud": "🚫 Too many refunds — payments are temporarily unavailable.",
        "free_used": "🆓 Free conversion ({left} left this week).",
        "share_button": "📤 Share",
        "share_text": "Convert any file for free in Telegram 👉",
        "ref_reward": "🎁 Your friend used the bot — you got +{n} free conversions!",
        "help": (
            "🧰 <b>FileBox</b> — your universal file master.\n\n"
            "How to use:\n"
            "1️⃣ Open the menu — /menu\n"
            "2️⃣ Pick a category and a tool\n"
            "3️⃣ Send your file(s)\n"
            "4️⃣ Get the result 🎁\n\n"
            "Commands: /menu · /language · /help\n"
            "Limits: incoming file up to 20 MB, result up to 50 MB.\n"
            "💫 Free for selected users; others pay {stars} ⭐ per conversion.\n"
            "✏️ Send a text message to name your output file (e.g. my.pdf)."
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
        "prompt_any": "📎 <b>Ягон файл</b> фиристед.",
        "stage_prepare": "Омода мекунам…",
        "stage_process": "Коркард мекунам…",
        "stage_send": "Мефиристам…",
        "progress_frame": "⚙️ <b>{stage}</b>\n\n{bar}  <b>{pct}%</b>",
        "result_caption": "🎁 Тайёр!",
        "result_text": "📝 <b>Натиҷа:</b>",
        "ready_again": "✨ Тайёр! Абзори навбатиро интихоб кунед — /menu",
        "err_generic": "😕 Коркард нашуд. Файлро санҷед ва боз кӯшиш кунед.",
        "err_timeout": "⌛ Коркард хеле тӯл кашид ва қатъ шуд. Файли хурдтарро кӯшиш кунед.",
        "err_rate": "🚦 Дар як соат хеле зиёд коркард. Каме интизор шавед ва боз кӯшиш кунед.",
        "pay_refunded": "↩️ Вазифа бекор шуд, барои ҳамин ситораҳоятонро баргардондам. Аз нав оғоз кунед — /menu",
        "busy": "⏳ Лутфан интизор шавед — ман ҳанӯз файли қаблиро коркард мекунам…",
        "err_too_big_in": "⚠️ Файл аз <b>20 МБ</b> зиёд аст — Telegram ба ман иҷозаи боргирӣ намедиҳад. Хурдтарашро фиристед.",
        "err_too_big_out": "⚠️ Натиҷа аз <b>50 МБ</b> зиёд аст — фиристода наметавонам. Фишурда кунед ё камтар файл.",
        "err_wrong_type": "🤔 Навъи файл нодуруст. Лутфан фиристед: {hint}",
        "err_no_files": "🤔 Шумо ҳанӯз чизе нафиристодед.",
        "cleared": "🗑 Тоза шуд.",
        "name_hint": "💡 Метавонед <b>номи файл</b>-ро фиристед (мисол: <code>файл.pdf</code>).",
        "name_set": "✅ Номи файл: <b>{name}</b>",
        "pay_prompt": "🔒 Коркард <b>{stars} ⭐</b> меарзад. Барои идома пардохт кунед 👇",
        "pay_title": "FileBox — коркарди файл",
        "pay_desc": "Пардохти {stars} ⭐ барои як коркард.",
        "pay_label": "1 коркард",
        "pay_thanks": "✅ Пардохт қабул шуд, ташаккур! Коркард мекунам…",
        "pack_offer": "💡 Тез-тез истифода мебаред? Баста арзонтар аст:",
        "pack_button": "🎟 {n} коркард ба {price} ⭐",
        "pack_title": "FileBox — бастаи коркард",
        "pack_desc": "{n} коркард ба {price} ⭐.",
        "pack_label": "{n} коркард",
        "pack_added": "🎟 +{n} коркард илова шуд! Дар баланс: <b>{credits}</b>. Танҳо файл фиристед 🎁",
        "credit_used": "🎟 1 коркард аз баста истифода шуд. Боқӣ: <b>{credits}</b>.",
        "err_fraud": "🚫 Хеле зиёд баргардонида шуд — пардохт муваққатан дастнорас аст.",
        "free_used": "🆓 Коркарди ройгон ({left} дар ин ҳафта мондааст).",
        "share_button": "📤 Мубодила",
        "share_text": "Ҳар файлро дар Telegram ройгон табдил медиҳам 👉",
        "ref_reward": "🎁 Дӯстат аз бот истифода кард — ба ту +{n} коркарди ройгон!",
        "help": (
            "🧰 <b>FileBox</b> — устоди универсалии файлҳо.\n\n"
            "Тарзи истифода:\n"
            "1️⃣ Менюро кушоед — /menu\n"
            "2️⃣ Категория ва абзорро интихоб кунед\n"
            "3️⃣ Файл(ҳо)ро фиристед\n"
            "4️⃣ Натиҷаро гиред 🎁\n\n"
            "Фармонҳо: /menu · /language · /help\n"
            "Маҳдудият: файли воридотӣ то 20 МБ, натиҷа то 50 МБ.\n"
            "💫 Барои интихобшудагон ройгон; барои дигарон — {stars} ⭐ барои коркард.\n"
            "✏️ Матн фиристед, то ба файл ном диҳед (мисол: файл.pdf)."
        ),
    },
    "uz": {
        "choose_language": "🌍 <b>Tilni tanlang</b>\nChoose your language\nВыберите язык",
        "lang_set": "✅ Til: <b>{name}</b>",
        "menu_title": "🧰 <b>FileBox</b> — fayl bilan nima qilamiz?\nToifani tanlang 👇",
        "cat_title": "<b>{cat}</b>\nAsbobni tanlang 👇",
        "pick_param": "⚙️ Variantni tanlang:",
        "btn_back": "◀️ Orqaga",
        "btn_home": "🏠 Menyu",
        "btn_run": "▶️ Tayyor",
        "btn_clear": "🗑 Tozalash",
        "btn_lang": "🌐 Til",
        "btn_help": "❓ Yordam",
        "collected": "📎 Yig'ildi: <b>{n}</b>\nYana yuboring yoki <b>«▶️ Tayyor»</b> tugmasini bosing.",
        "prompt_images": "🖼 <b>Rasmlar</b> yuboring (xohlaganingizcha), keyin <b>«▶️ Tayyor»</b> tugmasini bosing.",
        "prompt_image": "🖼 <b>Bitta rasm</b> yuboring.",
        "prompt_pdf": "📄 <b>PDF fayl</b> yuboring.",
        "prompt_pdfs": "📄 <b>Bir nechta PDF</b> yuboring, keyin <b>«▶️ Tayyor»</b> tugmasini bosing.",
        "prompt_office": "📝 <b>Hujjat</b> yuboring (Word, Excel, PowerPoint, TXT…).",
        "prompt_files": "📎 <b>Fayllar</b> (istalgan) yuboring, keyin <b>«▶️ Tayyor»</b> tugmasini bosing.",
        "prompt_zip": "🗜 <b>ZIP arxiv</b> yuboring.",
        "prompt_video": "🎬 <b>Video</b> yuboring.",
        "prompt_audio": "🎵 <b>Audio</b> yoki ovozli xabar yuboring.",
        "prompt_text": "🔳 <b>Matn yoki havola</b> yuboring — QR-kod yasayman.",
        "prompt_any": "📎 <b>Istalgan fayl</b> yuboring.",
        "stage_prepare": "Tayyorlayapman…",
        "stage_process": "Ishlayapman…",
        "stage_send": "Yuboryapman…",
        "progress_frame": "⚙️ <b>{stage}</b>\n\n{bar}  <b>{pct}%</b>",
        "result_caption": "🎁 Tayyor!",
        "result_text": "📝 <b>Natija:</b>",
        "ready_again": "✨ Tayyor! Keyingi asbobni tanlang — /menu",
        "err_generic": "😕 Ishlab bo'lmadi. Faylni tekshirib, qayta urinib ko'ring.",
        "err_timeout": "⌛ Ishlov juda uzoq davom etdi va to'xtatildi. Kichikroq fayl yuboring.",
        "err_rate": "🚦 Bir soatda juda ko'p ishlov. Biroz kuting va qayta urinib ko'ring.",
        "pay_refunded": "↩️ Vazifa bekor qilindi, shuning uchun yulduzlarni qaytardim. Qaytadan boshlang — /menu",
        "busy": "⏳ Kuting — men hali oldingi faylni ishlayapman…",
        "err_too_big_in": "⚠️ Fayl <b>20 MB</b> dan katta — Telegram uni yuklab olishga ruxsat bermaydi. Kichikroq yuboring.",
        "err_too_big_out": "⚠️ Natija <b>50 MB</b> dan katta — yubora olmayman. Siqib ko'ring yoki kamroq fayl.",
        "err_wrong_type": "🤔 Fayl turi noto'g'ri. Yuboring: {hint}",
        "err_no_files": "🤔 Siz hali hech narsa yubormadingiz.",
        "cleared": "🗑 Tozalandi.",
        "name_hint": "💡 Chiqadigan <b>fayl nomini</b> yuborishingiz mumkin (masalan, <code>fayl.pdf</code>).",
        "name_set": "✅ Fayl nomi: <b>{name}</b>",
        "pay_prompt": "🔒 Ishlov <b>{stars} ⭐</b> turadi. Davom etish uchun to'lang 👇",
        "pay_title": "FileBox — fayl ishlovi",
        "pay_desc": "Bitta fayl ishlovi uchun {stars} ⭐ to'lov.",
        "pay_label": "1 ishlov",
        "pay_thanks": "✅ To'lov qabul qilindi, rahmat! Ishlayapman…",
        "pack_offer": "💡 Tez-tez ishlatasizmi? Paket arzonroq:",
        "pack_button": "🎟 {n} ishlov {price} ⭐ ga",
        "pack_title": "FileBox — ishlov paketi",
        "pack_desc": "{n} ishlov {price} ⭐ ga.",
        "pack_label": "{n} ishlov",
        "pack_added": "🎟 +{n} ishlov qo'shildi! Balans: <b>{credits}</b>. Shunchaki fayl yuboring 🎁",
        "credit_used": "🎟 Paketdan 1 ishlov ishlatildi. Qoldi: <b>{credits}</b>.",
        "err_fraud": "🚫 Juda ko'p qaytarish — to'lov vaqtincha mavjud emas.",
        "free_used": "🆓 Bepul ishlov ({left} bu hafta qoldi).",
        "share_button": "📤 Ulashish",
        "share_text": "Telegram'da istalgan faylni bepul o'giraman 👉",
        "ref_reward": "🎁 Do'stingiz botdan foydalandi — sizga +{n} bepul ishlov!",
        "help": (
            "🧰 <b>FileBox</b> — universal fayl ustasi.\n\n"
            "Qanday ishlatish:\n"
            "1️⃣ Menyuni oching — /menu\n"
            "2️⃣ Toifa va asbobni tanlang\n"
            "3️⃣ Fayl(lar)ni yuboring\n"
            "4️⃣ Natijani oling 🎁\n\n"
            "Buyruqlar: /menu · /language · /help\n"
            "Cheklov: kiruvchi fayl 20 MB gacha, natija 50 MB gacha.\n"
            "💫 Tanlanganlar uchun bepul; boshqalar uchun — {stars} ⭐ har ishlov.\n"
            "✏️ Chiqadigan faylga nom berish uchun matn yuboring (masalan, fayl.pdf)."
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
    "image_rotate": {"ru": "🔄 Повернуть фото", "en": "🔄 Rotate image", "tg": "🔄 Гардондани акс"},
    "grayscale": {"ru": "⚫ Чёрно-белое", "en": "⚫ Grayscale", "tg": "⚫ Сиёҳу сафед"},
    "negative": {"ru": "🎞 Негатив", "en": "🎞 Negative", "tg": "🎞 Негатив"},
    "remove_bg": {"ru": "🪄 Убрать фон", "en": "🪄 Remove background", "tg": "🪄 Хориҷи замина"},
    "files_to_zip": {"ru": "📦 Файлы в ZIP", "en": "📦 Files to ZIP", "tg": "📦 Файлҳо ба ZIP"},
    "unzip": {"ru": "📂 Распаковать ZIP", "en": "📂 Unzip", "tg": "📂 Кушодани ZIP"},
    "text_to_qr": {"ru": "🔳 Текст в QR", "en": "🔳 Text to QR", "tg": "🔳 Матн ба QR"},
    "qr_to_text": {"ru": "📷 QR в текст", "en": "📷 QR to text", "tg": "📷 QR ба матн"},
    "ocr_image": {"ru": "👁 Текст с фото", "en": "👁 Image to text", "tg": "👁 Матн аз акс"},
    "file_hash": {"ru": "#️⃣ Хэш файла", "en": "#️⃣ File hash", "tg": "#️⃣ Ҳэши файл"},
    "video_to_gif": {"ru": "🎥 Видео в GIF", "en": "🎥 Video to GIF", "tg": "🎥 Видео ба GIF"},
    "video_to_audio": {"ru": "🔇 Видео в MP3", "en": "🔇 Video to MP3", "tg": "🔇 Видео ба MP3"},
    "compress_video": {"ru": "🗜 Сжать видео", "en": "🗜 Compress video", "tg": "🗜 Фишурдани видео"},
    "audio_convert": {"ru": "🎵 Конверт. аудио", "en": "🎵 Convert audio", "tg": "🎵 Табдили аудио"},
}

# Uzbek (beta) labels merged into CATS/OPS
CATS_UZ = {
    "pdf": "📄 PDF", "office": "📝 Hujjatlar", "image": "🖼 Rasmlar",
    "archive": "🗜 Arxivlar", "utils": "🔧 Vositalar", "media": "🎬 Media",
}
OPS_UZ = {
    "photos_to_pdf": "🖼→📄 Rasm → PDF", "pdf_to_images": "📄→🖼 PDF → rasm",
    "merge_pdf": "🔗 PDF birlashtirish", "split_pdf": "✂️ PDF bo'lish",
    "compress_pdf": "🗜 PDF siqish", "rotate_pdf": "🔄 PDF burish",
    "pdf_to_text": "🔤 PDF → matn", "office_to_pdf": "📘 Office → PDF",
    "pdf_to_word": "📄→📘 PDF → Word", "image_convert": "🔄 Formatni o'zgartirish",
    "compress_image": "🗜 Rasmni siqish", "resize_image": "📐 O'lchamni o'zgartirish",
    "images_to_gif": "🎞 Rasm → GIF", "strip_exif": "🧹 Metadatani tozalash",
    "image_rotate": "🔄 Rasmni burish", "grayscale": "⚫ Oq-qora",
    "negative": "🎞 Negativ", "remove_bg": "🪄 Fonni olib tashlash",
    "files_to_zip": "📦 Fayl → ZIP", "unzip": "📂 ZIP ochish",
    "text_to_qr": "🔳 Matn → QR", "qr_to_text": "📷 QR → matn",
    "ocr_image": "👁 Rasmdan matn", "file_hash": "#️⃣ Fayl hash",
    "video_to_gif": "🎥 Video → GIF", "video_to_audio": "🔇 Video → MP3",
    "compress_video": "🗜 Video siqish", "audio_convert": "🎵 Audio o'zgartirish",
}
for _k, _v in CATS_UZ.items():
    CATS.setdefault(_k, {})["uz"] = _v
for _k, _v in OPS_UZ.items():
    OPS.setdefault(_k, {})["uz"] = _v


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
    if code.startswith("uz"):
        return "uz"
    return "en"
