# -*- coding: utf-8 -*-
"""Local CLI tool to generate Asosnoma from PDF files without running Telegram bot."""
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import argparse
from pathlib import Path
import config
from core import build_docx, parse_report, parse_ai, extract_meta_from_pdf, format_short_name

def main():
    parser = argparse.ArgumentParser(description="Asosnoma Generator CLI")
    parser.add_argument("--uz", type=str, default=str(config.SAMPLE_FILES["uz"]), help="Path to uz.pdf")
    parser.add_argument("--ru", type=str, default=str(config.SAMPLE_FILES["ru"]), help="Path to ru.pdf")
    parser.add_argument("--eng", type=str, default=str(config.SAMPLE_FILES["eng"]), help="Path to eng.pdf")
    parser.add_argument("--si", type=str, default=str(config.SAMPLE_FILES["ai"]), help="Path to si.pdf")
    parser.add_argument("--lang", type=str, default="uz-cyrl", choices=["uz-cyrl", "uz-latn", "ru", "en"], help="Output language")
    parser.add_argument("--out", type=str, default="", help="Output docx path")
    args = parser.parse_args()

    reports = {}
    meta = {}

    for key, path_str in [("uz", args.uz), ("ru", args.ru), ("eng", args.eng)]:
        p = Path(path_str)
        if p.exists():
            print(f"📖 Oʻqilmoqda: {p.name}...")
            data = p.read_bytes()
            reports[key] = parse_report(data)
            print(f"   └ {len(reports[key])} ta manba topildi.")
            if not meta:
                ext = extract_meta_from_pdf(data)
                if ext:
                    meta.update(ext)

    ai_pcts = None
    si_path = Path(args.si)
    if si_path.exists():
        print(f"📖 Oʻqilmoqda SI: {si_path.name}...")
        si_data = si_path.read_bytes()
        ai_pcts = parse_ai(si_data)
        if ai_pcts:
            print(f"   └ SI: {ai_pcts[0]}%, Ehtimoliy: {ai_pcts[1]}%, Original: {ai_pcts[2]}%")

    if not reports:
        print("❌ Kamida bitta plagiat hisoboti mavjud boʻlishi kerak!")
        sys.exit(1)

    # Use standard commission matching the academic council format (names blank for council members)
    meta['commission'] = [
        ['Илмий даражалар берувчи илмий кенгаш раиси', ''],
        ['Илмий даражалар берувчи илмий кенгаш котиби', ''],
        ['Илмий даражалар берувчи илмий кенгаш аъзоси', ''],
        ['Илмий раҳбар', ''],
        ['Илмий раҳбар', ''],
        ['Таянч докторант', format_short_name(meta.get('fio', ''))],
    ]

    out_file = args.out
    if not out_file:
        fio_clean = (meta.get('fio') or 'asosnoma').split()[0]
        out_file = f"ASOSNOMA_{fio_clean}_{args.lang}.docx"

    print(f"⚙️ Asosnoma shakllantirilmoqda (til: {args.lang})...")
    buf, counts = build_docx(reports, ai_pcts, lang=args.lang, meta=meta)
    
    with open(out_file, "wb") as f:
        f.write(buf.getvalue())

    print(f"✅ Muvaffaqiyatli saqlandi: {out_file}")
    print(f"📊 Statistika: {counts}")

if __name__ == "__main__":
    main()
