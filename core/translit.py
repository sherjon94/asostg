# -*- coding: utf-8 -*-
"""Uzbek Latin <-> Cyrillic transliterator."""
import re

# Cyrillic -> Latin (multi-char outputs handled with case awareness)
CYR2LAT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
    'ж': 'j', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'x', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh',
    'ъ': 'ʼ', 'ы': 'i', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    'ў': 'oʻ', 'қ': 'q', 'ғ': 'gʻ', 'ҳ': 'h',
}

# Latin -> Cyrillic, longest keys first
LAT2CYR_DIGRAPHS = [
    ("oʻ", 'ў'), ("oʼ", 'ў'), ("o'", 'ў'), ("o`", 'ў'), ("oʹ", 'ў'),
    ("gʻ", 'ғ'), ("gʼ", 'ғ'), ("g'", 'ғ'), ("g`", 'ғ'),
    ("sh", 'ш'), ("ch", 'ч'), ("yo", 'ё'), ("yu", 'ю'), ("ya", 'я'),
    ("ye", 'е'), ("ts", 'ц'),
]
LAT2CYR_SINGLE = {
    'a': 'а', 'b': 'б', 'd': 'д', 'e': 'е', 'f': 'ф', 'g': 'г', 'h': 'ҳ',
    'i': 'и', 'j': 'ж', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о',
    'p': 'п', 'q': 'қ', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у', 'v': 'в',
    'w': 'в', 'x': 'х', 'y': 'й', 'z': 'з', 'c': 'к',
    "'": 'ъ', 'ʼ': 'ъ', 'ʻ': 'ъ', '`': 'ъ',
}


def cyr2lat(text):
    if not text:
        return text
    res = []
    for i, ch in enumerate(text):
        low = ch.lower()
        if low in CYR2LAT:
            out = CYR2LAT[low]
            if ch.isupper() and out:
                nxt = text[i + 1] if i + 1 < len(text) else ''
                prv = text[i - 1] if i > 0 else ''
                allcaps = (nxt.isalpha() and nxt.isupper()) or (prv.isalpha() and prv.isupper())
                if len(out) > 1:
                    out = out.upper() if allcaps else out[0].upper() + out[1:]
                else:
                    out = out.upper()
            res.append(out)
        else:
            res.append(ch)
    return ''.join(res)


def lat2cyr(text):
    if not text:
        return text
    res = []
    i = 0
    n = len(text)
    while i < n:
        matched = False
        for lat, cyr in LAT2CYR_DIGRAPHS:
            seg = text[i:i + len(lat)]
            if seg.lower() == lat.lower():
                if seg[0].isupper():
                    nxt = text[i + len(lat)] if i + len(lat) < n else ''
                    out = cyr.upper() if (len(seg) > 1 and seg[-1].isupper()) or (nxt.isupper()) else cyr.upper()[0] + cyr[1:]
                    out = cyr.upper() if seg.isupper() else cyr[0].upper() + cyr[1:]
                else:
                    out = cyr
                res.append(out)
                i += len(lat)
                matched = True
                break
        if matched:
            continue
        ch = text[i]
        low = ch.lower()
        if low in LAT2CYR_SINGLE:
            out = LAT2CYR_SINGLE[low]
            if low == 'e':
                prev = text[i - 1] if i > 0 else ''
                if not prev.isalpha():
                    out = 'э'
            if ch.isupper() and out:
                out = out.upper()
            res.append(out)
        else:
            res.append(ch)
        i += 1
    return ''.join(res)


def transliterate(text, direction):
    if direction == 'lat2cyr':
        return lat2cyr(text)
    return cyr2lat(text)
