# -*- coding: utf-8 -*-
"""
FileBox — a multilingual (RU/EN/TG) Telegram file-conversion bot.

Menu → category → tool → send file(s) → animated progress → result.
Runs 24/7 for free on GitHub Actions (polling, with a graceful ~6h handoff).
"""

import asyncio
import html
import logging
import os
import shutil
import tempfile
import time
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
    LabeledPrice,
    Message,
    PreCheckoutQuery,
)

import converters as C
import i18n
import store
from i18n import cat_label, detect_lang, op_label, prompt_for, t

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger("filebox")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
BASE_DIR = Path(tempfile.gettempdir()) / "filebox"
MAX_DOWNLOAD = 20 * 1024 * 1024   # Telegram getFile limit (incoming)
MAX_SEND = 49 * 1024 * 1024       # Telegram send limit (outgoing), small margin

# Monetization: whitelisted users are free & unlimited; everyone else pays Stars.
FREE_IDS = {x.strip() for x in os.environ.get("FREE_IDS", "").split(",") if x.strip()}
PRICE_STARS = int(os.environ.get("PRICE_STARS", "1") or "1")


def is_free(user_id):
    return str(user_id) in FREE_IDS


CONV_TIMEOUT = 180                      # hard cap per conversion (seconds)
CONCURRENCY = asyncio.Semaphore(3)      # max simultaneous heavy conversions
MAX_PER_HOUR = 30                       # per-user conversions / hour (non-free)
PACK_SIZE = int(os.environ.get("PACK_SIZE", "10") or "10")
PACK_PRICE = int(os.environ.get("PACK_PRICE", "20") or "20")
FRAUD_LIMIT = 10                        # block payments after this many refunds
STARTED = time.time()

IMG_EXT = {"jpg", "jpeg", "png", "webp", "bmp", "tiff", "tif", "gif", "heic", "heif"}
OFFICE_EXT = {"doc", "docx", "xls", "xlsx", "ppt", "pptx", "odt", "ods", "odp", "rtf", "txt", "csv"}
VIDEO_EXT = {"mp4", "mov", "avi", "mkv", "webm", "m4v"}
AUDIO_EXT = {"mp3", "wav", "ogg", "m4a", "flac", "aac", "opus"}

sessions = {}  # user_id -> session dict
dp = Dispatcher()


# --------------------------------------------------------------------------- #
# session
# --------------------------------------------------------------------------- #
def get_session(user_id, lang_hint=None):
    s = sessions.get(user_id)
    if s is None:
        s = {
            "lang": lang_hint or "en",
            "view": "menu",
            "cat": None,
            "op": None,
            "files": [],
            "params": {},
            "collect_msg_id": None,
            "panel_task": None,
            "lock": asyncio.Lock(),
            "conv_times": [],
            "dir": BASE_DIR / str(user_id),
        }
        sessions[user_id] = s
    return s


def _cancel_panel(s):
    task = s.get("panel_task")
    if task and not task.done():
        task.cancel()
    s["panel_task"] = None


def reset_job(s):
    _cancel_panel(s)
    s["op"] = None
    s["files"] = []
    s["params"] = {}
    s["collect_msg_id"] = None
    shutil.rmtree(s["dir"], ignore_errors=True)


# --------------------------------------------------------------------------- #
# keyboards
# --------------------------------------------------------------------------- #
def kb_lang():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="setlang:ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="setlang:en"),
        ],
        [
            InlineKeyboardButton(text="🇹🇯 Тоҷикӣ", callback_data="setlang:tg"),
            InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="setlang:uz"),
        ],
    ])


def kb_menu(lang):
    rows, row = [], []
    for cat in C.CATEGORY_ORDER:
        row.append(InlineKeyboardButton(text=cat_label(lang, cat), callback_data=f"cat:{cat}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([
        InlineKeyboardButton(text=t(lang, "btn_lang"), callback_data="lang"),
        InlineKeyboardButton(text=t(lang, "btn_help"), callback_data="help"),
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def kb_category(lang, cat):
    rows = [
        [InlineKeyboardButton(text=op_label(lang, op["id"]), callback_data=f"op:{op['id']}")]
        for op in C.OPERATIONS if op["cat"] == cat
    ]
    rows.append([InlineKeyboardButton(text=t(lang, "btn_back"), callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def kb_param(lang, op):
    choices = C.param_choices_for(op) or []
    rows, row = [], []
    for value, label in choices:
        row.append(InlineKeyboardButton(text=label, callback_data=f"opt:{value}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([InlineKeyboardButton(text=t(lang, "btn_back"), callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def kb_collect(lang, multi):
    if multi:
        rows = [
            [InlineKeyboardButton(text=t(lang, "btn_run"), callback_data="run")],
            [
                InlineKeyboardButton(text=t(lang, "btn_clear"), callback_data="clear"),
                InlineKeyboardButton(text=t(lang, "btn_home"), callback_data="home"),
            ],
        ]
    else:
        rows = [[InlineKeyboardButton(text=t(lang, "btn_home"), callback_data="home")]]
    return InlineKeyboardMarkup(inline_keyboard=rows)


# --------------------------------------------------------------------------- #
# progress bar
# --------------------------------------------------------------------------- #
PROGRESS_BLOCKS = 12


def _bar(pct):
    filled = max(0, min(PROGRESS_BLOCKS, int(round(pct / 100 * PROGRESS_BLOCKS))))
    return "▰" * filled + "▱" * (PROGRESS_BLOCKS - filled)


async def _progress(bot, chat_id, msg_id, lang, pct, stage_key):
    text = t(lang, "progress_frame", stage=t(lang, stage_key), bar=_bar(pct), pct=pct)
    try:
        await bot.edit_message_text(text=text, chat_id=chat_id, message_id=msg_id)
    except Exception:
        pass


# --------------------------------------------------------------------------- #
# commands
# --------------------------------------------------------------------------- #
@dp.message(CommandStart())
async def on_start(message: Message):
    lang = detect_lang(message.from_user.language_code)
    s = get_session(message.from_user.id, lang)
    if s["lock"].locked():
        await message.answer(t(s["lang"], "busy"))
        return
    reset_job(s)
    s["view"] = "menu"
    await message.answer(t(s["lang"], "choose_language"), reply_markup=kb_lang())


@dp.message(Command("menu"))
async def on_menu(message: Message):
    s = get_session(message.from_user.id, detect_lang(message.from_user.language_code))
    if s["lock"].locked():
        await message.answer(t(s["lang"], "busy"))
        return
    await open_menu(message, s)


@dp.message(Command("language"))
async def on_language(message: Message):
    s = get_session(message.from_user.id, detect_lang(message.from_user.language_code))
    await message.answer(t(s["lang"], "choose_language"), reply_markup=kb_lang())


@dp.message(Command("help"))
async def on_help(message: Message):
    s = get_session(message.from_user.id, detect_lang(message.from_user.language_code))
    await message.answer(t(s["lang"], "help", stars=PRICE_STARS))


@dp.message(Command("id"))
async def on_id(message: Message):
    await message.answer(f"🆔 <code>{message.from_user.id}</code>")


@dp.message(Command("stats"))
async def on_stats(message: Message):
    if not is_free(message.from_user.id):
        return  # owner-only, silent for others
    st = store.stats()
    up = int(time.time() - STARTED)
    top = sorted(st.get("by_op", {}).items(), key=lambda kv: -kv[1])[:8]
    rows = "\n".join(f"• {i18n.op_label('ru', k)}: <b>{v}</b>" for k, v in top) or "—"
    scope = "всё время 💾" if store.ENABLED else "текущий запуск"
    await message.answer(
        f"📊 <b>Статистика ({scope})</b>\n\n"
        f"Обработок: <b>{st.get('conversions', 0)}</b>\n"
        f"Заработано: <b>{st.get('stars', 0)} ⭐</b>\n"
        f"Аптайм текущего запуска: {up // 3600}ч {up % 3600 // 60}м\n\n"
        f"{rows}"
    )


# --------------------------------------------------------------------------- #
# payments (Telegram Stars)
# --------------------------------------------------------------------------- #
async def gate_and_run(message: Message, s, user_id):
    """Free users run instantly; others must pay Stars first."""
    if s["lock"].locked():
        await message.answer(t(s["lang"], "busy"))
        return
    # per-user hourly rate limit (whitelisted users are exempt)
    now = time.time()
    s["conv_times"] = [x for x in s["conv_times"] if now - x < 3600]
    if not is_free(user_id) and len(s["conv_times"]) >= MAX_PER_HOUR:
        await message.answer(t(s["lang"], "err_rate"))
        return
    if is_free(user_id):
        await run_current(message, s)
        return
    # antifraud: too many refunds → block paid access
    if store.refunds_of(user_id) >= FRAUD_LIMIT:
        await message.answer(t(s["lang"], "err_fraud"))
        return
    # use a pre-paid pack credit if available
    if store.use_credit(user_id):
        asyncio.create_task(store.save())
        await message.answer(t(s["lang"], "credit_used", credits=store.credits_of(user_id)))
        await run_current(message, s)
        return
    await request_payment(message, s)


async def request_payment(message: Message, s):
    lang = s["lang"]
    await message.answer(t(lang, "pay_prompt", stars=PRICE_STARS))
    await message.answer_invoice(
        title=t(lang, "pay_title"),
        description=t(lang, "pay_desc", stars=PRICE_STARS),
        payload=f"filebox:one:{s.get('op')}",
        currency="XTR",
        prices=[LabeledPrice(label=t(lang, "pay_label"), amount=PRICE_STARS)],
        provider_token="",
    )
    # offer a discounted pack of conversions
    await message.answer(
        t(lang, "pack_offer", n=PACK_SIZE, price=PACK_PRICE),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text=t(lang, "pack_button", n=PACK_SIZE, price=PACK_PRICE),
                callback_data="buypack",
            )
        ]]),
    )


@dp.callback_query(F.data == "buypack")
async def cb_buypack(cb: CallbackQuery):
    s = get_session(cb.from_user.id)
    await cb.answer()
    await cb.message.answer_invoice(
        title=t(s["lang"], "pack_title"),
        description=t(s["lang"], "pack_desc", n=PACK_SIZE, price=PACK_PRICE),
        payload="filebox:pack",
        currency="XTR",
        prices=[LabeledPrice(label=t(s["lang"], "pack_label", n=PACK_SIZE), amount=PACK_PRICE)],
        provider_token="",
    )


@dp.pre_checkout_query()
async def on_pre_checkout(q: PreCheckoutQuery):
    await q.answer(ok=True)


async def _refund(message: Message, sp):
    try:
        await message.bot.refund_star_payment(
            user_id=message.from_user.id,
            telegram_payment_charge_id=sp.telegram_payment_charge_id,
        )
    except Exception:
        logger.exception("refund failed")


@dp.message(F.successful_payment)
async def on_paid(message: Message):
    s = get_session(message.from_user.id, detect_lang(message.from_user.language_code))
    lang = s["lang"]
    uid = message.from_user.id
    sp = message.successful_payment
    parts = (sp.invoice_payload or "").split(":")
    kind = parts[1] if len(parts) > 1 else ""

    if kind == "pack":
        store.add_credits(uid, PACK_SIZE)
        if store.ENABLED and not await store.save():
            store.add_credits(uid, -PACK_SIZE)  # couldn't persist → undo and refund
            await _refund(message, sp)
            await message.answer(t(lang, "pay_refunded"))
            return
        store.record_payment(uid, "pack", PACK_PRICE)
        store.add_stars(PACK_PRICE)
        await message.answer(t(lang, "pack_added", n=PACK_SIZE, credits=store.credits_of(uid)))
        return

    # single conversion — the paid job must still be the active one
    paid_op = parts[2] if len(parts) > 2 else ""
    op = C.OP_BY_ID.get(paid_op)
    valid = op is not None and s.get("op") == paid_op and (s["files"] or op["input"] in C.TEXT_INPUTS)
    if not valid:
        await _refund(message, sp)
        store.bump_refund(uid)
        asyncio.create_task(store.save())
        await message.answer(t(lang, "pay_refunded"))
        return
    store.record_payment(uid, "one", PRICE_STARS, paid_op)
    store.add_stars(PRICE_STARS)
    asyncio.create_task(store.save())
    await message.answer(t(lang, "pay_thanks"))
    await run_current(message, s)


async def open_menu(message: Message, s):
    reset_job(s)
    s["view"] = "menu"
    await message.answer(t(s["lang"], "menu_title"), reply_markup=kb_menu(s["lang"]))


# --------------------------------------------------------------------------- #
# callbacks (menu navigation)
# --------------------------------------------------------------------------- #
@dp.callback_query(F.data.startswith("setlang:"))
async def cb_setlang(cb: CallbackQuery):
    lang = cb.data.split(":", 1)[1]
    s = get_session(cb.from_user.id)
    if await _cb_busy(cb, s):
        return
    s["lang"] = lang if lang in i18n.LANGS else "en"
    reset_job(s)
    s["view"] = "menu"
    await _safe_edit(cb, t(s["lang"], "menu_title"), kb_menu(s["lang"]))
    await cb.answer(t(s["lang"], "lang_set", name=i18n.LANG_NAMES[s["lang"]]))


@dp.callback_query(F.data == "lang")
async def cb_lang(cb: CallbackQuery):
    s = get_session(cb.from_user.id)
    await _safe_edit(cb, t(s["lang"], "choose_language"), kb_lang())
    await cb.answer()


@dp.callback_query(F.data == "help")
async def cb_help(cb: CallbackQuery):
    s = get_session(cb.from_user.id)
    await cb.message.answer(t(s["lang"], "help", stars=PRICE_STARS))
    await cb.answer()


@dp.callback_query(F.data == "home")
async def cb_home(cb: CallbackQuery):
    s = get_session(cb.from_user.id)
    if await _cb_busy(cb, s):
        return
    reset_job(s)
    s["view"] = "menu"
    await _safe_edit(cb, t(s["lang"], "menu_title"), kb_menu(s["lang"]))
    await cb.answer()


@dp.callback_query(F.data == "back")
async def cb_back(cb: CallbackQuery):
    s = get_session(cb.from_user.id)
    if await _cb_busy(cb, s):
        return
    if s["view"] in ("param", "collect") and s.get("cat"):
        s["view"] = "cat"
        reset_job_keep_cat(s)
        await _safe_edit(
            cb, t(s["lang"], "cat_title", cat=cat_label(s["lang"], s["cat"])),
            kb_category(s["lang"], s["cat"]),
        )
    else:
        reset_job(s)
        s["view"] = "menu"
        await _safe_edit(cb, t(s["lang"], "menu_title"), kb_menu(s["lang"]))
    await cb.answer()


def reset_job_keep_cat(s):
    cat = s["cat"]
    reset_job(s)
    s["cat"] = cat


@dp.callback_query(F.data.startswith("cat:"))
async def cb_cat(cb: CallbackQuery):
    s = get_session(cb.from_user.id)
    cat = cb.data.split(":", 1)[1]
    s["cat"] = cat
    s["view"] = "cat"
    await _safe_edit(cb, t(s["lang"], "cat_title", cat=cat_label(s["lang"], cat)), kb_category(s["lang"], cat))
    await cb.answer()


@dp.callback_query(F.data.startswith("op:"))
async def cb_op(cb: CallbackQuery):
    s = get_session(cb.from_user.id)
    if await _cb_busy(cb, s):
        return
    op_id = cb.data.split(":", 1)[1]
    op = C.OP_BY_ID.get(op_id)
    if not op:
        await cb.answer()
        return
    reset_job_keep_cat(s)
    s["op"] = op_id
    if op.get("param"):
        s["view"] = "param"
        await _safe_edit(cb, t(s["lang"], "pick_param"), kb_param(s["lang"], op))
    else:
        await _enter_collect(cb, s, op)
    await cb.answer()


@dp.callback_query(F.data.startswith("opt:"))
async def cb_opt(cb: CallbackQuery):
    s = get_session(cb.from_user.id)
    if await _cb_busy(cb, s):
        return
    op = C.OP_BY_ID.get(s.get("op"))
    if not op:
        await cb.answer()
        return
    s["params"][op["param"]] = cb.data.split(":", 1)[1]
    await _enter_collect(cb, s, op)
    await cb.answer()


async def _enter_collect(cb: CallbackQuery, s, op):
    s["view"] = "collect"
    lang = s["lang"]
    multi = op["input"] in C.MULTI_INPUTS
    text = prompt_for(lang, op["input"])
    if op["input"] not in C.TEXT_INPUTS:
        text += "\n\n" + t(lang, "name_hint")
    await _safe_edit(cb, text, kb_collect(lang, multi))
    s["collect_msg_id"] = cb.message.message_id


@dp.callback_query(F.data == "clear")
async def cb_clear(cb: CallbackQuery):
    s = get_session(cb.from_user.id)
    if await _cb_busy(cb, s):
        return
    _cancel_panel(s)
    for p in s["files"]:
        try:
            Path(p).unlink(missing_ok=True)
        except Exception:
            pass
    s["files"] = []
    op = C.OP_BY_ID.get(s.get("op"))
    if op:
        lang = s["lang"]
        text = prompt_for(lang, op["input"])
        if op["input"] not in C.TEXT_INPUTS:
            text += "\n\n" + t(lang, "name_hint")
        await _safe_edit(cb, text, kb_collect(lang, True))
        s["collect_msg_id"] = cb.message.message_id
    await cb.answer(t(s["lang"], "cleared"))


@dp.callback_query(F.data == "run")
async def cb_run(cb: CallbackQuery):
    s = get_session(cb.from_user.id)
    _cancel_panel(s)
    await cb.answer()
    await gate_and_run(cb.message, s, cb.from_user.id)


# --------------------------------------------------------------------------- #
# incoming media / text
# --------------------------------------------------------------------------- #
def _kind_from_doc(doc):
    name = (doc.file_name or "").lower()
    ext = name.rsplit(".", 1)[-1] if "." in name else ""
    mime = doc.mime_type or ""
    if ext in IMG_EXT or mime.startswith("image/"):
        return "image"
    if ext == "pdf" or mime == "application/pdf":
        return "pdf"
    if ext in OFFICE_EXT:
        return "office"
    if ext == "zip" or "zip" in mime:
        return "zip"
    if ext in VIDEO_EXT or mime.startswith("video/"):
        return "video"
    if ext in AUDIO_EXT or mime.startswith("audio/"):
        return "audio"
    return "other"


def _incoming(message: Message):
    """Return (downloadable, filename, size, kind) for whatever media is present."""
    if message.photo:
        ph = message.photo[-1]
        return ph, f"photo_{ph.file_unique_id}.jpg", ph.file_size, "image"
    if message.document:
        d = message.document
        return d, d.file_name or f"file_{d.file_unique_id}", d.file_size, _kind_from_doc(d)
    if message.video:
        v = message.video
        return v, v.file_name or f"video_{v.file_unique_id}.mp4", v.file_size, "video"
    if message.audio:
        a = message.audio
        return a, a.file_name or f"audio_{a.file_unique_id}.mp3", a.file_size, "audio"
    if message.voice:
        vo = message.voice
        return vo, f"voice_{vo.file_unique_id}.ogg", vo.file_size, "audio"
    return None


def _accepts(op_input, kind):
    if op_input in ("images", "image"):
        return kind == "image"
    if op_input in ("pdfs", "pdf"):
        return kind == "pdf"
    if op_input == "office":
        return kind == "office"
    if op_input == "zip":
        return kind == "zip"
    if op_input == "video":
        return kind == "video"
    if op_input == "audio":
        return kind == "audio"
    if op_input == "files":
        return kind in ("image", "pdf", "office", "zip", "video", "audio", "other")
    if op_input == "any":
        return True
    return False


def _safe_name(name):
    name = Path(name).name
    keep = "".join(c for c in name if c.isalnum() or c in "._- ")
    return keep.strip() or "file"


def _apply_name(path: Path, outname):
    """Rename the result to the user's chosen name, keeping the real extension."""
    ext = path.suffix
    base = _safe_name(outname)
    if "." in base:
        base = base.rsplit(".", 1)[0]
    base = base.strip()
    if not base:
        return path
    new_path = path.with_name(base + ext)
    try:
        path.rename(new_path)
        return new_path
    except Exception:
        return path


@dp.message(F.photo | F.document | F.video | F.audio | F.voice)
async def on_media(message: Message):
    s = get_session(message.from_user.id, detect_lang(message.from_user.language_code))
    lang = s["lang"]
    if s["lock"].locked():
        await message.answer(t(lang, "busy"))
        return
    if s.get("view") != "collect" or not s.get("op"):
        await open_menu(message, s)
        return
    op = C.OP_BY_ID[s["op"]]
    inc = _incoming(message)
    if not inc:
        return
    file_obj, filename, size, kind = inc
    if not _accepts(op["input"], kind):
        await message.answer(t(lang, "err_wrong_type", hint=prompt_for(lang, op["input"])))
        return
    if size and size > MAX_DOWNLOAD:
        await message.answer(t(lang, "err_too_big_in"))
        return
    s["dir"].mkdir(parents=True, exist_ok=True)
    dest = s["dir"] / f"{len(s['files']) + 1:03d}_{_safe_name(filename)}"
    try:
        await message.bot.download(file_obj, destination=dest)
    except Exception:
        logger.exception("download failed")
        await message.answer(t(lang, "err_too_big_in"))
        return
    s["files"].append(dest)
    if op["input"] in C.MULTI_INPUTS:
        _schedule_panel(message, s)
    else:
        await gate_and_run(message, s, message.from_user.id)


@dp.message(F.text)
async def on_text(message: Message):
    s = get_session(message.from_user.id, detect_lang(message.from_user.language_code))
    if s["lock"].locked():
        await message.answer(t(s["lang"], "busy"))
        return
    op = C.OP_BY_ID.get(s.get("op"))
    if s.get("view") == "collect" and op:
        if op["input"] == "text":
            s["params"]["text"] = message.text
            await gate_and_run(message, s, message.from_user.id)
        else:
            # any text while collecting = custom output file name
            raw = (message.text or "").strip()
            if 0 < len(raw) <= 60:
                name = _safe_name(raw)
                if "." in name:
                    name = name.rsplit(".", 1)[0]
                if name:
                    s["params"]["outname"] = name
                    await message.answer(t(s["lang"], "name_set", name=html.escape(name)))
        return
    await open_menu(message, s)


def _schedule_panel(message: Message, s):
    """Debounced: re-post the Done/Clear panel at the bottom after the last photo."""
    _cancel_panel(s)
    s["panel_task"] = asyncio.create_task(_panel_after_delay(message, s))


async def _panel_after_delay(message: Message, s):
    try:
        await asyncio.sleep(1.0)
    except asyncio.CancelledError:
        return
    await _post_panel(message, s)


async def _post_panel(message: Message, s):
    lang = s["lang"]
    old = s.get("collect_msg_id")
    try:
        m = await message.answer(
            t(lang, "collected", n=len(s["files"])), reply_markup=kb_collect(lang, True)
        )
        s["collect_msg_id"] = m.message_id
    except Exception:
        return
    if old:
        await _delete(message.bot, message.chat.id, old)


# --------------------------------------------------------------------------- #
# run the conversion
# --------------------------------------------------------------------------- #
async def run_current(message: Message, s):
    lang = s["lang"]
    _cancel_panel(s)
    op = C.OP_BY_ID.get(s.get("op"))
    if not op:
        await open_menu(message, s)
        return
    if not s["files"] and op["input"] not in C.TEXT_INPUTS:
        await message.answer(t(lang, "err_no_files"))
        return
    if s["lock"].locked():
        await message.answer(t(lang, "busy"))
        return
    async with s["lock"]:
        await _do_conversion(message, s, op)


async def _do_conversion(message: Message, s, op):
    lang = s["lang"]
    s["conv_times"].append(time.time())
    bot = message.bot
    chat_id = message.chat.id
    prog = await message.answer(
        t(lang, "progress_frame", stage=t(lang, "stage_prepare"), bar=_bar(0), pct=0)
    )

    try:
        async with CONCURRENCY:
            task = asyncio.create_task(
                asyncio.to_thread(op["fn"], list(s["files"]), s["dir"], dict(s["params"]))
            )
            for pct, stage in ((20, "stage_prepare"), (55, "stage_process"), (85, "stage_process")):
                await asyncio.sleep(0.4)
                if task.done():
                    break
                await _progress(bot, chat_id, prog.message_id, lang, pct, stage)
            outputs = await asyncio.wait_for(task, timeout=CONV_TIMEOUT)
    except asyncio.TimeoutError:
        logger.warning("conversion timeout: %s", op["id"])
        await _delete(bot, chat_id, prog.message_id)
        await message.answer(t(lang, "err_timeout"))
        reset_job(s)
        s["view"] = "menu"
        return
    except Exception:
        logger.exception("conversion failed: %s", op["id"])
        await _delete(bot, chat_id, prog.message_id)
        await message.answer(t(lang, "err_generic"))
        reset_job(s)
        s["view"] = "menu"
        return

    await _progress(bot, chat_id, prog.message_id, lang, 100, "stage_send")
    try:
        await bot.send_chat_action(chat_id=chat_id, action="upload_document")
    except Exception:
        pass

    outname = s["params"].get("outname")
    if outname and len(outputs) == 1 and op["id"] not in C.TEXT_OUTPUT_OPS:
        outputs = [_apply_name(Path(outputs[0]), outname)]

    sent = 0
    for out in outputs[:25]:
        out = Path(out)
        if not out.exists():
            continue
        try:
            if out.stat().st_size > MAX_SEND:
                await message.answer(t(lang, "err_too_big_out"))
                continue
            await _send_output(message, lang, op["id"], out)
            sent += 1
        except Exception:
            logger.exception("send failed")
            await message.answer(t(lang, "err_too_big_out"))

    await _delete(bot, chat_id, prog.message_id)
    if sent == 0:
        await message.answer(t(lang, "err_generic"))
    else:
        store.bump_stat(op["id"])
    reset_job(s)
    s["view"] = "menu"
    await message.answer(t(lang, "ready_again"), reply_markup=kb_menu(lang))


async def _send_output(message: Message, lang, op_id, path: Path):
    if op_id in C.TEXT_OUTPUT_OPS:
        text = path.read_text("utf-8", errors="ignore").strip() or "—"
        if len(text) <= 3500:
            await message.answer(t(lang, "result_text") + "\n<code>" + html.escape(text) + "</code>")
            return
    if op_id in C.GIF_OUTPUT_OPS:
        await message.answer_animation(FSInputFile(path), caption=t(lang, "result_caption"))
    else:
        await message.answer_document(
            FSInputFile(path, filename=path.name), caption=t(lang, "result_caption")
        )


# --------------------------------------------------------------------------- #
# small utils
# --------------------------------------------------------------------------- #
async def _cb_busy(cb: CallbackQuery, s):
    """Block state-changing callbacks while a conversion is running."""
    if s["lock"].locked():
        await cb.answer(t(s["lang"], "busy"))
        return True
    return False


async def _safe_edit(cb: CallbackQuery, text, markup):
    try:
        await cb.message.edit_text(text, reply_markup=markup)
    except Exception:
        try:
            await cb.message.answer(text, reply_markup=markup)
        except Exception:
            pass


async def _delete(bot, chat_id, msg_id):
    try:
        await bot.delete_message(chat_id, msg_id)
    except Exception:
        pass


# --------------------------------------------------------------------------- #
# startup / run modes
# --------------------------------------------------------------------------- #
async def _set_commands(bot: Bot):
    await bot.set_my_commands([
        BotCommand(command="menu", description="Menu / Меню / Меню"),
        BotCommand(command="language", description="Language / Язык / Забон"),
        BotCommand(command="help", description="Help / Помощь / Кӯмак"),
    ])


async def run_polling(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=False)
    port = os.environ.get("PORT")
    if port:
        from aiohttp import web

        async def health(_r):
            return web.Response(text="ok")

        app = web.Application()
        app.router.add_get("/", health)
        runner = web.AppRunner(app)
        await runner.setup()
        await web.TCPSite(runner, "0.0.0.0", int(port)).start()
        logger.info("Health server on :%s", port)

    asyncio.create_task(store.periodic_saver())

    run_seconds = int(os.environ.get("RUN_SECONDS", "0") or "0")
    if run_seconds > 0:
        logger.info("POLLING for %ss then graceful handoff", run_seconds)
        poll_task = asyncio.create_task(dp.start_polling(bot, handle_signals=False))
        await asyncio.sleep(run_seconds)
        logger.info("RUN_SECONDS reached — stopping for next shift")
        await dp.stop_polling()
        await poll_task
        await store.save()  # persist final state before handoff
    else:
        logger.info("POLLING (no time limit)")
        await dp.start_polling(bot)


async def run_webhook(bot: Bot, webhook_url: str):
    from aiohttp import web
    from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

    path = "/webhook"
    await bot.set_webhook(webhook_url.rstrip("/") + path, drop_pending_updates=True)
    app = web.Application()

    async def health(_r):
        return web.Response(text="ok")

    app.router.add_get("/", health)
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=path)
    setup_application(app, dp, bot=bot)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", "8080"))).start()
    logger.info("WEBHOOK on %s%s", webhook_url, path)
    await asyncio.Event().wait()


async def main():
    if not BOT_TOKEN:
        raise SystemExit("BOT_TOKEN is not set. Get one from @BotFather.")
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    await store.load()
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
