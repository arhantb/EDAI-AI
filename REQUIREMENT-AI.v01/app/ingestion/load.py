from pathlib import Path
from typing import List, Dict, Iterable

import fitz  # PyMuPDF
from pdf2image import convert_from_path
import pytesseract
from PIL import Image


def list_input_files(input_dir: str | Path, exts: Iterable[str] = (".pdf", ".txt", ".png", ".jpg", ".jpeg")) -> List[Path]:
    base = Path(input_dir)
    files: List[Path] = []
    for ext in exts:
        files.extend(base.rglob(f"*{ext}"))
    return files


def read_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_text_from_pdf(path: Path) -> str:
    doc = fitz.open(path)
    texts: List[str] = []
    for page in doc:
        text = page.get_text("text")
        if not text or text.strip() == "":
            # fallback to OCR for image-based pages
            pix = page.get_pixmap(dpi=200)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img)
        texts.append(text)
    return "\n\n".join(texts)


def ocr_image(path: Path) -> str:
    img = Image.open(path)
    return pytesseract.image_to_string(img)


def load_and_normalize(path: Path) -> Dict:
    ext = path.suffix.lower()
    if ext == ".txt":
        text = read_txt(path)
    elif ext == ".pdf":
        text = extract_text_from_pdf(path)
    elif ext in {".png", ".jpg", ".jpeg"}:
        text = ocr_image(path)
    else:
        text = ""
    return {"source": str(path), "text": text}


