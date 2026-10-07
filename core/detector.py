# -*- coding: utf-8 -*-
"""Smart detector for Antiplagiat report PDF and DOCX template types."""
import os
import re
import fitz


def detect_file_type(file_bytes: bytes, filename: str = "") -> str:
    """
    Returns one of: 'uz', 'ru', 'eng', 'ai', 'docx', 'unknown'
    """
    lower_fn = os.path.basename(filename).lower()

    if lower_fn.endswith(".docx") or lower_fn.endswith(".doc"):
        return "docx"

    if not lower_fn.endswith(".pdf"):
        # If no extension or other, check magic bytes for PDF
        if not file_bytes.startswith(b"%PDF"):
            return "unknown"

    # 1. Page 0 inspection (Antiplagiat headers and report metadata)
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        if doc.page_count > 0:
            p0_txt = doc[0].get_text()[:3000].lower()

            # 1a. AI detector report
            if any(term in p0_txt for term in [
                "si detektor", "sun'iy intellekt", "sun’iy intellekt",
                "ehtimoliy sun'iy", "ehtimoliy sun’iy", "original matn",
                "детектор ии", "искусственный интеллект"
            ]):
                return "ai"

            # 1b. Antiplagiat system "Hujjat nomi:" / "Имя документа:" prefix
            # Example: "Hujjat nomi: original_uz_Dissertatsiya...", "translate_en_..."
            m_nomi = re.search(r'(?i)(?:hujjat nomi|имя документа|название документа):\s*([^\n\r]+)', p0_txt)
            if m_nomi:
                doc_title = m_nomi.group(1).lower()
                if "translate_en" in doc_title or "original_en" in doc_title:
                    return "eng"
                if "translate_ru" in doc_title or "original_ru" in doc_title:
                    return "ru"
                if "original_uz" in doc_title or "translate_uz" in doc_title:
                    return "uz"

            # 1c. Document title in page 0 with explicit language brackets
            if re.search(r'\(\s*(?:o[\'ʻ’`]?zbekcha|o[\'ʻ’`]?zbek\s+tilida)\b', p0_txt):
                return "uz"
            if re.search(r'\(\s*(?:ruscha|русский|на\s+русском)\b', p0_txt):
                return "ru"
            if re.search(r'\(\s*(?:inglizcha|english|на\s+английском)\b', p0_txt):
                return "eng"

    except Exception:
        pass

    # 2. Filename patterns
    # UZ patterns
    if re.search(r'(^|[^a-zа-яё])(uz|uzb|уз|узб|o[\'ʻ’`]?zbek)($|[^a-zа-яё])', lower_fn):
        return "uz"
    # RU patterns
    if re.search(r'(^|[^a-zа-яё])(ru|rus|ру|рус|russian)($|[^a-zа-яё])', lower_fn):
        return "ru"
    # ENG patterns
    if re.search(r'(^|[^a-zа-яё])(en|eng|ing|english)($|[^a-zа-яё])', lower_fn):
        return "eng"
    # SI / AI patterns
    if re.search(r'(^|[^a-zа-яё])(si|си|ai|ii|ии)($|[^a-zа-яё])', lower_fn):
        return "ai"

    # 3. Content language inspection from text (pages 1 to 5)
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        combined_text = ""
        for p in range(min(5, doc.page_count)):
            combined_text += " " + doc[p].get_text()

        txt_low = combined_text.lower()

        # Check for language-specific indicators
        # Uzbek specific letters / words
        uz_score = (
            len(re.findall(r'[ўқғҳ]', txt_low)) * 3 +
            len(re.findall(r"\b(bo[\'ʻ’`]?yicha|haqida|uchun|natijalari|dissertatsiyasi|mavzusidagi|maqom|daraja)\b", txt_low)) * 2
        )
        # Russian specific letters / words
        ru_score = (
            len(re.findall(r'[ыэъщ]', txt_low)) * 3 +
            len(re.findall(r'\b(диссертация|исследование|результаты|соискание|степень|литература|источник)\b', txt_low)) * 2
        )
        # English specific words
        eng_score = (
            len(re.findall(r'\b(dissertation|results|study|research|abstract|conclusion|university|chapter|sources)\b', txt_low)) * 2
        )

        if uz_score > ru_score and uz_score > eng_score and uz_score >= 4:
            return "uz"
        if ru_score > uz_score and ru_score > eng_score and ru_score >= 4:
            return "ru"
        if eng_score > uz_score and eng_score > ru_score and eng_score >= 4:
            return "eng"

        # Fallback domain search if scores are inconclusive
        if "elibrary.ru" in txt_low or "dlib.rsl.ru" in txt_low:
            return "ru"
        if "natlib.uz" in txt_low or "ziyonet.uz" in txt_low:
            return "uz"
    except Exception:
        pass

    return "unknown"


def is_scanned_pdf(file_bytes: bytes) -> bool:
    """
    Checks if a PDF contains only scanned images without selectable text layer.
    Antiplagiat reports always contain hundreds to thousands of characters of selectable text.
    If a document has pages and image objects with practically no text across pages, it is a scanned raster PDF.
    """
    if not file_bytes.startswith(b"%PDF"):
        return False
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        if doc.page_count == 0:
            return False
        total_text = ""
        has_images = False
        for p in range(min(5, doc.page_count)):
            page = doc[p]
            txt = page.get_text()
            if txt:
                total_text += txt.strip()
            if len(page.get_images()) > 0:
                has_images = True

        if len(total_text.strip()) < 40 and has_images:
            return True
        return False
    except Exception:
        return False

