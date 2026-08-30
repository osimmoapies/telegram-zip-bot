# -*- coding: utf-8 -*-
"""
Persistent state for FileBox, stored in a PRIVATE GitHub Gist.

Holds all-time stats, per-user credit balances (bought packs), a payment log
and refund counters. Fully optional: if GIST_ID / GH_GIST_TOKEN are not set,
everything works in-memory (resets on the ~6h handoff) and nothing breaks.

Only ONE bot instance runs at a time (workflow concurrency), so writes never
race across instances; within a run they are serialized by a lock.
"""

import asyncio
import json
import logging
import os

logger = logging.getLogger("filebox.store")

GIST_ID = os.environ.get("GIST_ID", "").strip()
GIST_TOKEN = os.environ.get("GH_GIST_TOKEN", "").strip()
GIST_FILE = "filebox_state.json"
ENABLED = bool(GIST_ID and GIST_TOKEN)

_lock = asyncio.Lock()
_dirty = False
_state = {
    "stats": {"conversions": 0, "stars": 0, "by_op": {}},
    "credits": {},
    "payments": [],
    "refunds": {},
    "free": {},
    "referrals": {},
}


def _headers():
    return {"Authorization": f"Bearer {GIST_TOKEN}", "Accept": "application/vnd.github+json"}


def _normalize():
    _state.setdefault("stats", {})
    _state["stats"].setdefault("conversions", 0)
    _state["stats"].setdefault("stars", 0)
    _state["stats"].setdefault("by_op", {})
    _state.setdefault("credits", {})
    _state.setdefault("payments", [])
    _state.setdefault("refunds", {})
    _state.setdefault("free", {})
    _state.setdefault("referrals", {})


async def load():
    _normalize()
    if not ENABLED:
        return
    try:
        import aiohttp
        async with aiohttp.ClientSession() as s:
            async with s.get(f"https://api.github.com/gists/{GIST_ID}", headers=_headers()) as r:
                data = await r.json()
        content = (data.get("files") or {}).get(GIST_FILE, {}).get("content")
        if content:
            loaded = json.loads(content)
            if isinstance(loaded, dict):
                _state.update(loaded)
                _normalize()
                logger.info("state loaded from gist")
    except Exception:
        logger.exception("gist load failed")


async def save():
    global _dirty
    if not ENABLED:
        _dirty = False
        return False
    async with _lock:
        try:
            import aiohttp
            body = {"files": {GIST_FILE: {"content": json.dumps(_state, ensure_ascii=False)}}}
            async with aiohttp.ClientSession() as s:
                async with s.patch(
                    f"https://api.github.com/gists/{GIST_ID}", headers=_headers(), json=body
                ) as r:
                    ok = r.status == 200
                    if not ok:
                        logger.warning("gist save http %s", r.status)
            _dirty = False
            return ok
        except Exception:
            logger.exception("gist save failed")
            return False


async def periodic_saver(interval=45):
    while True:
        await asyncio.sleep(interval)
        if _dirty:
            await save()


# --- credits (paid packs) ---
def credits_of(uid):
    return int(_state["credits"].get(str(uid), 0))


def add_credits(uid, n):
    global _dirty
    _state["credits"][str(uid)] = max(0, credits_of(uid) + int(n))
    _dirty = True


def use_credit(uid):
    global _dirty
    if credits_of(uid) > 0:
        _state["credits"][str(uid)] = credits_of(uid) - 1
        _dirty = True
        return True
    return False


# --- stats ---
def bump_stat(op_id):
    global _dirty
    st = _state["stats"]
    st["conversions"] += 1
    st["by_op"][op_id] = st["by_op"].get(op_id, 0) + 1
    _dirty = True


def add_stars(n):
    global _dirty
    _state["stats"]["stars"] += int(n)
    _dirty = True


def stats():
    return _state["stats"]


# --- payments & antifraud ---
def record_payment(uid, kind, stars, op=None):
    global _dirty
    _state["payments"].append({"user": str(uid), "kind": kind, "stars": int(stars), "op": op})
    _state["payments"] = _state["payments"][-1000:]
    _dirty = True


def refunds_of(uid):
    return int(_state["refunds"].get(str(uid), 0))


def bump_refund(uid):
    global _dirty
    _state["refunds"][str(uid)] = refunds_of(uid) + 1
    _dirty = True


# --- weekly free tier ---
def free_count(uid, week):
    rec = _state.get("free", {}).get(str(uid))
    if not rec or rec.get("week") != week:
        return 0
    return int(rec.get("count", 0))


def use_free(uid, week):
    global _dirty
    _state.setdefault("free", {})[str(uid)] = {"week": week, "count": free_count(uid, week) + 1}
    _dirty = True


# --- referrals ---
def set_referrer(uid, by):
    global _dirty
    _state.setdefault("referrals", {})[str(uid)] = {"by": str(by), "rewarded": False}
    _dirty = True


def get_referrer(uid):
    return _state.get("referrals", {}).get(str(uid))


def mark_referral_rewarded(uid):
    global _dirty
    r = _state.get("referrals", {}).get(str(uid))
    if r:
        r["rewarded"] = True
        _dirty = True
