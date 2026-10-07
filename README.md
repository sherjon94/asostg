# 📄 Asosnoma Generator Telegram Bot

Antiplagiat (`antiplag.uz`) tizimidan olingan PDF hisobotlardan OAK talablariga toʻliq mos keluvchi rasmiy **Asosnoma (.docx)** hujjatini avtomatik yaratib beruvchi Telegram bot.

Loyihaning veb talqini: [https://github.com/sherjon94/asosnoma](https://github.com/sherjon94/asosnoma)

---

## 🚀 Imkoniyatlari

- **4 ta tilda va yozuvda Asosnoma tayyorlash:**
  - 🇺🇿 Oʻzbekcha (Kirill)
  - 🇺🇿 Oʻzbekcha (Lotin)
  - 🇷🇺 Ruscha
  - 🇬🇧 Inglizcha
- **Hisobot fayllarini avtomatik aniqlash (Smart Detector):**
  - Oʻzbekcha hisobot (`uz.pdf`)
  - Ruscha hisobot (`ru.pdf`)
  - Inglizcha hisobot (`eng.pdf`)
  - Sunʼiy intellekt (SI) hisoboti (`si.pdf`)
  - Ixtiyoriy namuna hujjati (`namuna.docx` – maxsus iboralar uchun)
- **Titul varaqasidan rekvizitlarni avtomatik oʻqish:**
  - Muallif / tadqiqotchi F.I.Sh
  - OTM / Muassasa nomi
  - Dissertatsiya mavzusi
  - Ixtisoslik shifrlari va nomlari
  - Ilmiy daraja (PhD / DSc)
  - Tadqiqotchi maqomi (Tayanch doktorant / Mustaqil izlanuvchi)
- **Ekspert komissiyasi aʼzolari imzo blokini avtomatik toʻldirish:**
  - Rais, kotib, aʼzolar va ilmiy rahbarlar
  - Muallifning qisqartma F.I.Sh ini avtomatik qoʻyish (masalan: `Ш.О. Гайбуллаев`)
- **Interaktiv tahrirlash:**
  - Telegram bot orqali har qanday maydonni toʻgʻridan-toʻgʻri oʻzgartirish imkoniyati.
- **Mukammal formatlangan Word (.docx) hujjati:**
  - Albom (Landscape) format
  - Times New Roman shrifti
  - Standart jadval chiziqlari va fon ranglari
  - Toʻliq statistik tahlil xabari

---

## 🛠 Oʻrnatish va Ishga tushirish

### 1. Bogʻliqliklarni oʻrnatish:
```bash
pip install -r requirements.txt
```

### 2. Bot tokenini sozlash:
`@BotFather` orqali yangi bot oching va olingan tokenni `.env` fayliga kiriting:
```env
BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRstuVWXyz
```

### 3. Botni ishga tushirish:
Windows'da `run_bot.bat` faylini ikki marta bosing yoki terminalda:
```bash
python bot.py
```

---

## 💻 Konsoldan (CLI) toʻgʻridan-toʻgʻri foydalanish

Telegram botsiz ham konsoldan fayllarni yaratish mumkin:
```bash
python generate_local.py --lang uz-cyrl
```
Boshqa tillar:
```bash
python generate_local.py --lang uz-latn
python generate_local.py --lang ru
python generate_local.py --lang en
```

---

- **ZIP, RAR va 7Z arxivlarni toʻgʻridan-toʻgʻri qabul qilish:**
  - Barcha fayllarni bitta arxivda yuborish imkoniyati.
- **Skanerlangan (rasm) PDF larni aniqlash:**
  - Matn qatlami boʻlmagan skanerlangan fayllarni darhol aniqlab, toʻgʻri yoʻnaltirish.
- **Admin boshqaruv paneli (`/admin`):**
  - Foydalanuvchilar va generatsiyalar statistikasi.
  - Foydalanuvchilar roʻyxati (@username bilan birga).
  - Barcha foydalanuvchilarga xabar tarqatish (Broadcast).
  - Majburiy kanal obunasini boshqarish (Force Subscription).
- **Fikr-mulohaza va Texnik yordam (`/feedback`):**
  - Foydalanuvchilar toʻgʻridan-toʻgʻri adminga savol, rasm yoki shikoyat yuborishi.
  - Adminning bevosita Telegramdan javob yozish imkoniyati.
- **Avtomatlashtirilgan xavfsizlik va barqarorlik:**
  - Anti-flood va navbat (rate limiting) himoyasi.
  - Asosnoma yaratilganda adminga nusxasini yuborish.
  - Donat boʻlimi (`/donate`).

---

## 📁 Loyiha tuzilishi

```text
├── bot.py                  # Telegram botning asosiy ishga tushirish fayli
├── config.py               # Sozlamalar va yo'llar
├── generate_local.py       # Konsol orqali to'g'ridan-to'g'ri docx yaratish vositasi
├── run_bot.bat             # Botni bir bosishda ishga tushiruvchi batch fayl
├── requirements.txt        # Kerakli kutubxonalar
├── .env.example            # Sozlamalar namunasi
├── core/
│   ├── archive.py          # ZIP, RAR, 7Z arxivlarini ochish
│   ├── asosnoma.py         # PDF parser va Word generator
│   ├── db.py               # SQLite ma'lumotlar bazasi
│   ├── detector.py         # Aqlli fayl va skaner aniqlovchi modul
│   ├── i18n.py             # 4 ta tildagi matnlar va tarjimalar
│   ├── limiter.py          # Rate limiting va oqim nazorati
│   └── translit.py         # Kirill <-> Lotin transliteratsiya
└── handlers/
    ├── admin.py            # Admin boshqaruv paneli (/admin)
    ├── commission.py       # Ekspert komissiyasini boshqarish
    ├── delete_file.py      # Fayllarni tanlab o'chirish va tozalash
    ├── edit_meta.py        # Rekvizitlarni tahrirlash va til tanlash
    ├── feedback.py         # Fikr-mulohaza va admin javoblari (/feedback)
    ├── generate.py         # Asosnoma .docx yaratish va adminga yuborish
    ├── sample.py           # Namunaviy fayllarni sinash
    ├── start.py            # /start, /help va /donate buyruqlari
    ├── sub_check.py        # Majburiy kanal a'zoligi nazorati
    └── upload.py           # Fayllarni yuklab olish va tekshirish
```
