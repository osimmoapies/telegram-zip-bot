# -*- coding: utf-8 -*-
"""
All file conversions for FileBox.

Every converter has the signature:  fn(inputs: list[Path], out: Path, params: dict) -> list[Path]
It returns the list of produced output files. On failure it raises — the bot
catches the exception and shows a friendly, localized error (never crashes).

Heavy libraries are imported lazily inside each function so the bot starts fast
and still runs even if an optional engine is missing.
"""

from __future__ import annotations

import subprocess
import uuid
import zipfile
from pathlib import Path


# --------------------------------------------------------------------------- #
# small helpers
# --------------------------------------------------------------------------- #
def _run(cmd, timeout=180):
    """Run a subprocess, raising RuntimeError with stderr on failure."""
    proc = subprocess.run(cmd, capture_output=True, timeout=timeout)
    if proc.returncode != 0:
        err = (proc.stderr or b"").decode("utf-8", "ignore")[:400]
        raise RuntimeError(f"{cmd[0]} failed: {err}")
    return proc


def _zip_files(files, out_zip: Path) -> Path:
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in files:
            p = Path(p)
            if p.is_file():
                zf.write(p, arcname=p.name)
    return out_zip


def _open_image(path):
    """Open an image, transparently supporting HEIC/HEIF."""
    from PIL import Image
    try:
        from pillow_heif import register_heif_opener
        register_heif_opener()
    except Exception:
        pass
    return Image.open(path)


def _soffice(src: Path, out: Path, target: str, timeout=150) -> Path:
    """Convert an office/pdf file with a private LibreOffice profile (avoids lock)."""
    profile = out / f"lo_{uuid.uuid4().hex}"
    _run(
        [
            "soffice",
            f"-env:UserInstallation=file://{profile}",
            "--headless", "--norestore", "--nolockcheck",
            "--convert-to", target, "--outdir", str(out), str(src),
        ],
        timeout=timeout,
    )
    ext = target.split(":")[0]
    result = out / f"{src.stem}.{ext}"
    if not result.exists():
        raise RuntimeError("LibreOffice produced no output")
    return result


# --------------------------------------------------------------------------- #
# PDF
# --------------------------------------------------------------------------- #
def photos_to_pdf(inputs, out, params):
    imgs = [_open_image(p).convert("RGB") for p in inputs]
    dst = out / "photos.pdf"
    imgs[0].save(dst, save_all=True, append_images=imgs[1:])
    return [dst]


def pdf_to_images(inputs, out, params):
    from pdf2image import convert_from_path
    pages = convert_from_path(str(inputs[0]), dpi=150)
    files = []
    for i, page in enumerate(pages, 1):
        p = out / f"page_{i:03d}.png"
        page.save(p, "PNG")
        files.append(p)
    return [_zip_files(files, out / "pages.zip")]


def merge_pdf(inputs, out, params):
    from pypdf import PdfWriter
    writer = PdfWriter()
    for p in inputs:
        writer.append(str(p))
    dst = out / "merged.pdf"
    with open(dst, "wb") as f:
        writer.write(f)
    return [dst]


def split_pdf(inputs, out, params):
    from pypdf import PdfReader, PdfWriter
    reader = PdfReader(str(inputs[0]))
    files = []
    for i, page in enumerate(reader.pages, 1):
        w = PdfWriter()
        w.add_page(page)
        p = out / f"page_{i:03d}.pdf"
        with open(p, "wb") as f:
            w.write(f)
        files.append(p)
    return [_zip_files(files, out / "pages.zip")]


def compress_pdf(inputs, out, params):
    dst = out / "compressed.pdf"
    _run([
        "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/ebook", "-dNOPAUSE", "-dQUIET", "-dBATCH",
        f"-sOutputFile={dst}", str(inputs[0]),
    ])
    return [dst]


def rotate_pdf(inputs, out, params):
    from pypdf import PdfReader, PdfWriter
    angle = int(params.get("angle", "90"))
    reader = PdfReader(str(inputs[0]))
    w = PdfWriter()
    for page in reader.pages:
        page.rotate(angle)
        w.add_page(page)
    dst = out / "rotated.pdf"
    with open(dst, "wb") as f:
        w.write(f)
    return [dst]


def pdf_to_text(inputs, out, params):
    import pdfplumber
    parts = []
    with pdfplumber.open(str(inputs[0])) as pdf:
        for page in pdf.pages:
            parts.append(page.extract_text() or "")
    dst = out / "text.txt"
    dst.write_text("\n\n".join(parts).strip() or "(no text found)", encoding="utf-8")
    return [dst]


# --------------------------------------------------------------------------- #
# Office
# --------------------------------------------------------------------------- #
def office_to_pdf(inputs, out, params):
    return [_soffice(Path(inputs[0]), out, "pdf")]


def pdf_to_word(inputs, out, params):
    from pdf2docx import Converter
    dst = out / "document.docx"
    cv = Converter(str(inputs[0]))
    try:
        cv.convert(str(dst))
    finally:
        cv.close()
    return [dst]


# --------------------------------------------------------------------------- #
# Images
# --------------------------------------------------------------------------- #
def image_convert(inputs, out, params):
    fmt = params.get("fmt", "jpg").lower()
    im = _open_image(inputs[0])
    if fmt in ("jpg", "jpeg", "pdf"):
        im = im.convert("RGB")
    ext = "jpg" if fmt == "jpeg" else fmt
    dst = out / f"image.{ext}"
    save_fmt = {"jpg": "JPEG", "png": "PNG", "webp": "WEBP", "pdf": "PDF"}.get(fmt, "PNG")
    im.save(dst, save_fmt)
    return [dst]


def compress_image(inputs, out, params):
    im = _open_image(inputs[0]).convert("RGB")
    dst = out / "compressed.jpg"
    im.save(dst, "JPEG", quality=60, optimize=True)
    return [dst]


def resize_image(inputs, out, params):
    from PIL import Image
    side = int(params.get("max", "1280"))
    im = _open_image(inputs[0])
    im.thumbnail((side, side), Image.Resampling.LANCZOS)
    ext = "png" if im.mode in ("RGBA", "P") else "jpg"
    dst = out / f"resized.{ext}"
    im.save(dst, "PNG" if ext == "png" else "JPEG", quality=90)
    return [dst]


def images_to_gif(inputs, out, params):
    frames = [_open_image(p).convert("RGB") for p in inputs]
    dst = out / "animation.gif"
    frames[0].save(
        dst, save_all=True, append_images=frames[1:], duration=600, loop=0
    )
    return [dst]


def strip_exif(inputs, out, params):
    from PIL import Image
    im = _open_image(inputs[0])
    clean = Image.new(im.mode, im.size)
    clean.putdata(list(im.getdata()))
    ext = "png" if im.mode in ("RGBA", "P") else "jpg"
    dst = out / f"clean.{ext}"
    clean.save(dst, "PNG" if ext == "png" else "JPEG", quality=95)
    return [dst]


def remove_bg(inputs, out, params):
    from rembg import remove  # heavy: downloads model on first use
    im = _open_image(inputs[0]).convert("RGBA")
    result = remove(im)
    dst = out / "no_bg.png"
    result.save(dst, "PNG")
    return [dst]


# --------------------------------------------------------------------------- #
# Archives
# --------------------------------------------------------------------------- #
def files_to_zip(inputs, out, params):
    return [_zip_files(inputs, out / "archive.zip")]


def unzip(inputs, out, params):
    extract_dir = out / "unzipped"
    extract_dir.mkdir(exist_ok=True)
    with zipfile.ZipFile(inputs[0]) as zf:
        # basic zip-bomb guard: cap total uncompressed size
        total = sum(info.file_size for info in zf.infolist())
        if total > 200 * 1024 * 1024:
            raise RuntimeError("archive too large when unpacked")
        zf.extractall(extract_dir)
    files = [p for p in extract_dir.rglob("*") if p.is_file()]
    if not files:
        raise RuntimeError("archive is empty")
    return files


# --------------------------------------------------------------------------- #
# Utilities
# --------------------------------------------------------------------------- #
def text_to_qr(inputs, out, params):
    import qrcode
    text = params.get("text", "")
    img = qrcode.make(text)
    dst = out / "qr.png"
    img.save(dst)
    return [dst]


def qr_to_text(inputs, out, params):
    from pyzbar.pyzbar import decode
    results = decode(_open_image(inputs[0]))
    if not results:
        raise RuntimeError("no QR/barcode found")
    text = "\n".join(r.data.decode("utf-8", "ignore") for r in results)
    dst = out / "qr_text.txt"
    dst.write_text(text, encoding="utf-8")
    return [dst]


def ocr_image(inputs, out, params):
    import pytesseract
    text = pytesseract.image_to_string(_open_image(inputs[0]), lang="rus+eng")
    dst = out / "ocr.txt"
    dst.write_text(text.strip() or "(no text recognized)", encoding="utf-8")
    return [dst]


# --------------------------------------------------------------------------- #
# Media (ffmpeg)
# --------------------------------------------------------------------------- #
def video_to_gif(inputs, out, params):
    dst = out / "video.gif"
    _run([
        "ffmpeg", "-y", "-i", str(inputs[0]),
        "-vf", "fps=10,scale=480:-1:flags=lanczos", "-t", "15", str(dst),
    ])
    return [dst]


def video_to_audio(inputs, out, params):
    dst = out / "audio.mp3"
    _run(["ffmpeg", "-y", "-i", str(inputs[0]), "-q:a", "0", "-map", "a", str(dst)])
    return [dst]


def compress_video(inputs, out, params):
    dst = out / "compressed.mp4"
    _run([
        "ffmpeg", "-y", "-i", str(inputs[0]),
        "-c:v", "libx264", "-preset", "fast", "-crf", "30",
        "-c:a", "aac", "-b:a", "128k", str(dst),
    ])
    return [dst]


def audio_convert(inputs, out, params):
    fmt = params.get("fmt", "mp3").lower()
    codec = {"mp3": "libmp3lame", "m4a": "aac", "wav": "pcm_s16le", "ogg": "libvorbis"}.get(fmt, "libmp3lame")
    dst = out / f"audio.{fmt}"
    _run(["ffmpeg", "-y", "-i", str(inputs[0]), "-c:a", codec, str(dst)])
    return [dst]


# --------------------------------------------------------------------------- #
# Registry: categories, operations, inputs, params
# --------------------------------------------------------------------------- #
CATEGORY_ORDER = ["pdf", "office", "image", "archive", "utils", "media"]

# input kinds: images/pdfs/files = MULTI, single-file kinds = SINGLE, text = TEXT
MULTI_INPUTS = {"images", "pdfs", "files"}
TEXT_INPUTS = {"text"}

# operations that return plain text to show inline
TEXT_OUTPUT_OPS = {"pdf_to_text", "qr_to_text", "ocr_image"}
# operations whose single output is an animated GIF
GIF_OUTPUT_OPS = {"images_to_gif", "video_to_gif"}

OPERATIONS = [
    # PDF
    {"id": "photos_to_pdf", "cat": "pdf", "input": "images", "fn": photos_to_pdf},
    {"id": "pdf_to_images", "cat": "pdf", "input": "pdf", "fn": pdf_to_images},
    {"id": "merge_pdf", "cat": "pdf", "input": "pdfs", "fn": merge_pdf},
    {"id": "split_pdf", "cat": "pdf", "input": "pdf", "fn": split_pdf},
    {"id": "compress_pdf", "cat": "pdf", "input": "pdf", "fn": compress_pdf},
    {"id": "rotate_pdf", "cat": "pdf", "input": "pdf", "fn": rotate_pdf, "param": "angle"},
    {"id": "pdf_to_text", "cat": "pdf", "input": "pdf", "fn": pdf_to_text},
    # Office
    {"id": "office_to_pdf", "cat": "office", "input": "office", "fn": office_to_pdf},
    {"id": "pdf_to_word", "cat": "office", "input": "pdf", "fn": pdf_to_word},
    # Images
    {"id": "image_convert", "cat": "image", "input": "image", "fn": image_convert, "param": "fmt"},
    {"id": "compress_image", "cat": "image", "input": "image", "fn": compress_image},
    {"id": "resize_image", "cat": "image", "input": "image", "fn": resize_image, "param": "max"},
    {"id": "images_to_gif", "cat": "image", "input": "images", "fn": images_to_gif},
    {"id": "strip_exif", "cat": "image", "input": "image", "fn": strip_exif},
    # Archives
    {"id": "files_to_zip", "cat": "archive", "input": "files", "fn": files_to_zip},
    {"id": "unzip", "cat": "archive", "input": "zip", "fn": unzip},
    # Utilities
    {"id": "text_to_qr", "cat": "utils", "input": "text", "fn": text_to_qr},
    {"id": "qr_to_text", "cat": "utils", "input": "image", "fn": qr_to_text},
    {"id": "ocr_image", "cat": "utils", "input": "image", "fn": ocr_image},
    # Media
    {"id": "video_to_gif", "cat": "media", "input": "video", "fn": video_to_gif},
    {"id": "video_to_audio", "cat": "media", "input": "video", "fn": video_to_audio},
    {"id": "compress_video", "cat": "media", "input": "video", "fn": compress_video},
    {"id": "audio_convert", "cat": "media", "input": "audio", "fn": audio_convert, "param": "fmt"},
]

OP_BY_ID = {op["id"]: op for op in OPERATIONS}

# choices for operations that need a parameter (labels are language-neutral)
PARAM_CHOICES = {
    "angle": [("90", "90°"), ("180", "180°"), ("270", "270°")],
    "fmt_image": [("jpg", "JPG"), ("png", "PNG"), ("webp", "WEBP"), ("pdf", "PDF")],
    "max": [("640", "640px"), ("1280", "1280px · HD"), ("1920", "1920px · Full HD")],
    "fmt_audio": [("mp3", "MP3"), ("m4a", "M4A"), ("wav", "WAV"), ("ogg", "OGG")],
}


def param_choices_for(op):
    """Return the list of (value, label) choices for an operation's parameter."""
    p = op.get("param")
    if not p:
        return None
    if op["id"] == "image_convert":
        return PARAM_CHOICES["fmt_image"]
    if op["id"] == "audio_convert":
        return PARAM_CHOICES["fmt_audio"]
    return PARAM_CHOICES.get(p)
