from typing import Any, Dict
from fastapi import Request

import re
import markdown
import bleach

ALLOWED_TAGS = set(bleach.sanitizer.ALLOWED_TAGS) | {
    "p", "br", "hr", "pre", "code", "img",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "ul", "ol", "li", "strong", "em", "blockquote",
    "table", "thead", "tbody", "tr", "th", "td"
}

ALLOWED_ATTRIBUTES = dict(bleach.sanitizer.ALLOWED_ATTRIBUTES)
ALLOWED_ATTRIBUTES.update({
    "img": ["src", "alt", "title", "width", "height", "loading"],
    "a": ["href", "title", "target", "rel"],
})

ALLOWED_PROTOCOLS = set(bleach.sanitizer.ALLOWED_PROTOCOLS) | {"data"}


def preprocess_markdown(md_text: str) -> str:
    """
    Исправляет Markdown:
    - добавляет пустую строку перед списками
    - добавляет пустую строку перед строками вида 'Здесь:' если дальше идёт список
    """
    if not md_text:
        return ""

    lines = md_text.split("\n")
    result = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # 1. Если строка заканчивается ":" и следующая строка — список
        if (
            stripped.endswith(":")
            and i + 1 < len(lines)
            and lines[i + 1].strip().startswith(("- ", "* ", "1. "))
        ):
            # Добавляем пустую строку перед этой строкой
            if result and result[-1].strip() != "":
                result.append("")
            result.append(line)
            continue

        # 2. Стандартное правило: пустая строка перед списками
        if (
            stripped.startswith(("- ", "* ", "1. "))
            and result
            and result[-1].strip() != ""
        ):
            result.append("")

        result.append(line)

    return "\n".join(result)


def md_to_safe_html(md_text: str) -> str:
    """
    Markdown -> HTML -> безопасный HTML.
    Переносы строк делает расширение nl2br.
    """
    if not md_text:
        return ""

    try:
        md_text = preprocess_markdown(md_text)

        html = markdown.markdown(
            md_text,
            extensions=[
                "extra",    # списки, таблицы, и т.п.
                "nl2br",    # ОДИНАРНЫЕ \n -> <br>
                "tables",
            ],
        )

        clean = bleach.clean(
            html,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            protocols=list(ALLOWED_PROTOCOLS),
            strip=True,
        )

        return clean

    except Exception:
        return bleach.clean(md_text, strip=True)


def ensure_dict(obj: Any) -> Dict:
    """
    Ensure obj is a plain dict. If it's a pydantic/sqlmodel object with .dict(), use it.
    """
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "dict") and callable(getattr(obj, "dict")):
        try:
            return obj.dict()
        except Exception:
            pass
    try:
        return dict(obj)
    except Exception:
        return {}


def build_image_url(request: Request, image_obj: Dict) -> str:
    """
    Build a public URL for an image.
    Priority:
      1) if image_obj has 'url' and it looks absolute (starts with http/https) -> return as is
      2) if image_obj has 'url' and starts with '/' -> return as is
      3) if image_obj has 'path' or 'filename' -> use request.url_for('static', path='img/<filename>')
      4) fallback: if image_obj has 'url' (relative) -> prefix with /static/
      5) empty string if nothing found
    """
    url = image_obj.get("url") or image_obj.get("src") or ""
    if url:
        if url.startswith("http://") or url.startswith("https://"):
            return url
        if url.startswith("/"):
            return url
        # relative path like "img/azores1.jpg" or "azores1.jpg"
        if url.startswith("img/") or url.startswith("static/") or "/" in url:
            # if it already contains img/ assume it's relative to static root
            return "/static/" + url.lstrip("/")
        # otherwise treat as filename
        return request.url_for("static", path=f"img/{url}")
    # try path/filename fields
    filename = image_obj.get("filename") or image_obj.get("path") or image_obj.get("file")
    if filename:
        # if filename already contains img/ prefix
        if filename.startswith("img/"):
            return request.url_for("static", path=filename[len("img/"):]) if False else "/static/" + filename.lstrip("/")
        return request.url_for("static", path=f"img/{filename}")
    return ""
