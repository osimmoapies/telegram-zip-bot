# -*- coding: utf-8 -*-
"""
Telegram Zip Photo Bot
----------------------
Users send as many photos as they want, then tap "Done" and get a .zip back.
Multilingual: Russian / English / Tajik. Publicly usable, 24/7 in the cloud.

Run modes (auto-detected):
  * WEBHOOK  — if WEBHOOK_URL or RENDER_EXTERNAL_URL is set (best for Render).
  * POLLING  — otherwise; also starts a tiny health server on $PORT when set
               (needed by Koyeb / Railway / Fly health checks).
"""

import asyncio
import logging
import os
import shutil
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    BotCommand,
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from i18n import BUTTON_ACTIONS, LANG_NAMES, detect_lang, t

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("zipbot")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
BASE_DIR = Path(tempfile.gettempdir()) / "zipbot"
# Telegram Bot API limit for sending documents is 50 MB; leave a little margin.
MAX_ZIP_BYTES = 49 * 1024 * 1024

# In-memory per-user sessions. Fine for this use case (stateless restarts are OK).
sessions = {}  # user_id -> {"lang", "count", "status_id", "dir"}

dp = Dispatcher()


# --------------------------------------------------------------------------- #
# Session helpers
# --------------------------------------------------------------------------- #
def get_session(user_id, lang_hint=None):
    s = sessions.get(user_id)
    if s is None:
        s = {
            "lang": lang_hint or "en",
            "count": 0,
            "status_id": None,
            "dir": BASE_DIR / str(user_id),
        }
        sessions[user_id] = s
    return s


def reset_files(s):
    s["count"] = 0
    s["status_id"] = None
    shutil.rmtree(s["dir"], ignore_errors=True)


# --------------------------------------------------------------------------- #
# Keyboards
# --------------------------------------------------------------------------- #
def lang_inline():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
                InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
                InlineKeyboardButton(text="🇹🇯 Тоҷикӣ", callback_data="lang:tg"),
            ]
        ]
    )


def controls(lang):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang, "btn_done"))],
            [
                KeyboardButton(text=t(lang, "btn_clear")),
                KeyboardButton(text=t(lang, "btn_lang")),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="📸 …",
    )


# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #
@dp.message(CommandStart())
async def on_start(message: Message):
    lang = detect_lang(message.from_user.language_code)
    s = get_session(message.from_user.id, lang)
    reset_files(s)
    await message.answer(t(s["lang"], "choose_language"), reply_markup=lang_inline())


@dp.message(Command("language"))
async def on_language(message: Message):
    s = get_session(message.from_user.id, detect_lang(message.from_user.language_code))
    await message.answer(t(s["lang"], "choose_language"), reply_markup=lang_inline())


@dp.message(Command("help"))
async def on_help(message: Message):
    s = get_session(message.from_user.id, detect_lang(message.from_user.language_code))
    await message.answer(t(s["lang"], "help"), reply_markup=controls(s["lang"]))


@dp.callback_query(F.data.startswith("lang:"))
async def on_lang_chosen(cb: CallbackQuery):
    lang = cb.data.split(":", 1)[1]
    if lang not in LANG_NAMES:
        lang = "en"
    s = get_session(cb.from_user.id)
    s["lang"] = lang
    try:
        await cb.message.edit_text(t(lang, "lang_set", name=LANG_NAMES[lang]))
    except Exception:
        pass
    await cb.message.answer(t(lang, "instructions"), reply_markup=controls(lang))
    await cb.answer()


# --------------------------------------------------------------------------- #
# Photo / document collection
# --------------------------------------------------------------------------- #
async def _save_and_update(message: Message, s, file_obj, filename):
    s["dir"].mkdir(parents=True, exist_ok=True)
    await message.bot.download(file_obj, destination=s["dir"] / filename)
    s["count"] += 1
    await _update_status(message, s)


@dp.message(F.photo)
async def on_photo(message: Message):
    s = get_session(message.from_user.id, detect_lang(message.from_user.language_code))
    filename = f"photo_{s['count'] + 1:03d}.jpg"
    await _save_and_update(message, s, message.photo[-1], filename)


@dp.message(F.document)
async def on_document(message: Message):
    s = get_session(message.from_user.id, detect_lang(message.from_user.language_code))
    doc = message.document
    if not (doc.mime_type or "").startswith("image/"):
        await message.answer(t(s["lang"], "not_a_photo"), reply_markup=controls(s["lang"]))
        return
    name = doc.file_name or f"image_{s['count'] + 1:03d}.jpg"
    # Prefix with an index to avoid duplicate filenames inside the zip.
    filename = f"{s['count'] + 1:03d}_{name}"
    await _save_and_update(message, s, doc, filename)


async def _update_status(message: Message, s):
    lang = s["lang"]
    text = t(lang, "collected", n=s["count"])
    if s["status_id"] is None:
        m = await message.answer(text, reply_markup=controls(lang))
        s["status_id"] = m.message_id
        return
    try:
        await message.bot.edit_message_text(
            text=text, chat_id=message.chat.id, message_id=s["status_id"]
        )
    except Exception:
        # Message too old, rate-limited, or unchanged — post a fresh status line.
        try:
            m = await message.answer(text)
            s["status_id"] = m.message_id
        except Exception:
            pass


# --------------------------------------------------------------------------- #
# Text buttons (Done / Clear / Language) + fallback hint
# --------------------------------------------------------------------------- #
@dp.message(F.text)
async def on_text(message: Message):
    s = get_session(message.from_user.id, detect_lang(message.from_user.language_code))
    action = BUTTON_ACTIONS.get(message.text.strip())
    if action == "done":
        await do_done(message, s)
    elif action == "clear":
        reset_files(s)
        await message.answer(t(s["lang"], "cleared"), reply_markup=controls(s["lang"]))
    elif action == "lang":
        await message.answer(t(s["lang"], "choose_language"), reply_markup=lang_inline())
    else:
        await message.answer(t(s["lang"], "send_photos_hint"), reply_markup=controls(s["lang"]))


async def do_done(message: Message, s):
    lang = s["lang"]
    if s["count"] == 0:
        await message.answer(t(lang, "no_photos"), reply_markup=controls(lang))
        return

    await message.answer(t(lang, "packing"))
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_path = BASE_DIR / f"photos_{message.from_user.id}_{stamp}.zip"

    def _make_zip():
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for p in sorted(s["dir"].iterdir()):
                if p.is_file():
                    zf.write(p, arcname=p.name)
        return zip_path.stat().st_size

    try:
        size = await asyncio.to_thread(_make_zip)
    except Exception:
        logger.exception("Failed to build zip")
        await message.answer(t(lang, "too_large"), reply_markup=controls(lang))
        return

    if size > MAX_ZIP_BYTES:
        await message.answer(t(lang, "too_large"), reply_markup=controls(lang))
        zip_path.unlink(missing_ok=True)
        return

    count = s["count"]
    try:
        await message.answer_document(
            FSInputFile(zip_path, filename=zip_path.name),
            caption=t(lang, "done_caption", n=count),
        )
    finally:
        zip_path.unlink(missing_ok=True)
        reset_files(s)

    await message.answer(t(lang, "ready_again"), reply_markup=controls(lang))


# --------------------------------------------------------------------------- #
# Startup / run modes
# --------------------------------------------------------------------------- #
async def _set_commands(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Start / Начать / Оғоз"),
            BotCommand(command="language", description="Language / Язык / Забон"),
            BotCommand(command="help", description="Help / Помощь / Кӯмак"),
        ]
    )


async def run_polling(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=False)
    port = os.environ.get("PORT")
    if port:
        # Keep a minimal HTTP endpoint alive for PaaS health checks (Koyeb, etc.).
        from aiohttp import web

        async def health(_request):
            return web.Response(text="ok")

        app = web.Application()
        app.router.add_get("/", health)
        app.router.add_get("/health", health)
        runner = web.AppRunner(app)
        await runner.setup()
        await web.TCPSite(runner, "0.0.0.0", int(port)).start()
        logger.info("Health server listening on :%s", port)

    logger.info("Starting in POLLING mode")
    await dp.start_polling(bot)


async def run_webhook(bot: Bot, webhook_url: str):
    from aiohttp import web
    from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

    path = "/webhook"
    full_url = webhook_url.rstrip("/") + path
    await bot.set_webhook(full_url, drop_pending_updates=True)
    logger.info("Starting in WEBHOOK mode -> %s", full_url)

    app = web.Application()

    async def health(_request):
        return web.Response(text="ok")

    app.router.add_get("/", health)
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=path)
    setup_application(app, dp, bot=bot)

    port = int(os.environ.get("PORT", "8080"))
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", port).start()
    logger.info("Webhook server listening on :%s", port)
    await asyncio.Event().wait()  # run forever


async def main():
    if not BOT_TOKEN:
        raise SystemExit(
            "BOT_TOKEN is not set. Get a token from @BotFather and set it as an env var."
        )
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await _set_commands(bot)

    webhook_url = os.environ.get("WEBHOOK_URL") or os.environ.get("RENDER_EXTERNAL_URL")
    if webhook_url:
        await run_webhook(bot, webhook_url)
    else:
        await run_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
