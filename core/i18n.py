# -*- coding: utf-8 -*-
"""Multi-language localization (i18n) for Bot interface."""

BOT_LANGUAGES = {
    "uz-latn": "🇺🇿 Oʻzbekcha (Lotin)",
    "uz-cyrl": "🇺🇿 Ўзбекча (Кирилл)",
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
}

DOC_LANGUAGES = {
    "uz-latn": "🇺🇿 Oʻzbekcha (Lotin)",
    "uz-cyrl": "🇺🇿 Ўзбекча (Кирилл)",
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
}

TEXTS = {
    "uz-latn": {
        "welcome": (
            "👋 <b>Assalomu alaykum!</b>\n\n"
            "<b>Asosnoma Generator Bot</b>ga xush kelibsiz!\n"
            "Ushbu bot <b>antiplag.uz</b> tizimidan yuklab olingan PDF hisobotlar asosida "
            "OAK talablariga toʻliq mos keluvchi rasmiy <b>«Asosnoma» (.docx)</b> hujjatini "
            "avtomatik ravishda tayyorlab beradi.\n\n"
            "👨‍💻 <b>Bot admini:</b> @{admin}\n\n"
            "📥 <b>Boshlash uchun:</b>\n"
            "Antiplagiat hisobot fayllarini (PDF) botga yuboring yoki quyidagi "
            "<b>«🧪 Namunaviy test fayllari»</b> tugmasi orqali sinab koʻring!\n\n"
        ),
        "help": (
            "📖 <b>BOTDAN FOYDALANISH BOʻYICHA YOʻRIQNOMA</b>\n\n"
            "1️⃣ <b>Fayllarni yuklash:</b>\n"
            "• <b>uz.pdf</b> – Oʻzbekcha matn plagiat hisoboti\n"
            "• <b>ru.pdf</b> – Ruscha matn plagiat hisoboti\n"
            "• <b>eng.pdf</b> – Inglizcha matn plagiat hisoboti\n"
            "• <b>si.pdf</b> – Sunʼiy intellekt (SI) hisoboti\n"
            "• <b>namuna.docx</b> – Oldingi asosnoma namunasi (ixtiyoriy)\n"
            "• 📦 <b>ZIP / RAR</b> – Barcha fayllarni bitta arxivda yuborish ham mumkin\n\n"
            "2️⃣ <b>Avtomatik toʻldirish:</b>\n"
            "PDF fayllardan muallif F.I.Sh, mavzu, muassasa va ixtisosliklar avtomatik aniqlanadi.\n\n"
            "3️⃣ <b>Tahrirlash:</b>\n"
            "«✏️ Rekvizitlarni tahrirlash» orqali istalgan maʼlumotni oʻzgartirish mumkin.\n\n"
            "4️⃣ <b>Asosnoma yaratish:</b>\n"
            "Kamida bitta hisobot yuklangach, «🚀 Asosnoma yaratish» tugmasi paydo boʻladi.\n\n"
            "👨‍💻 <b>Admin:</b> @{admin}\n"
        ),
        "admin": (
            "👨‍💻 <b>BOT ADMINISTRATORI:</b>\n\n"
            "• <b>Admin:</b> @{admin}\n"
            "• <b>Telegram profil:</b> <a href='{url}'>t.me/{admin}</a>\n\n"
            "Savollar, takliflar yoki texnik masalalar boʻyicha bemalol murojaat qilishingiz mumkin!"
        ),
        "files_header": "📊 <b>HISOBOT FAYLLARI HOLATI:</b>",
        "meta_header": "📋 <b>HUJJAT REKVIZITLARI:</b>",
        "rep_uz": "🇺🇿 Oʻzbekcha hisobot",
        "rep_ru": "🇷🇺 Ruscha hisobot",
        "rep_eng": "🇬🇧 Inglizcha hisobot",
        "rep_ai": "🤖 Sunʼiy intellekt hisoboti",
        "rep_sample": "📄 Namuna (.docx)",
        "not_uploaded": "❌ <i>Yuklanmagan</i>",
        "sample_active": "✅ faol (maxsus iboralar qoʻllaniladi)",
        "sample_optional": "➖ <i>Ixtiyoriy (standart iboralar)</i>",
        "sources_count": "{cnt} ta manba",
        "fio_label": "👤 <b>F.I.Sh:</b>",
        "uni_label": "🏛 <b>Muassasa:</b>",
        "status_label": "🎓 <b>Maqom:</b>",
        "topic_label": "📚 <b>Mavzu:</b>",
        "spec_label": "🔬 <b>Ixtisoslik:</b>",
        "degree_label": "📜 <b>Daraja:</b>",
        "bot_lang_label": "🌐 <b>Bot tili:</b>",
        "doc_lang_label": "📄 <b>Hujjat tili:</b>",
        "admin_label": "👨‍💻 <b>Admin:</b>",
        "tip_files": "<i>💡 Fayllarni (PDF, DOCX yoki ZIP/RAR arxiv) botga yuborishingiz mumkin. Maʼlumotlar avtomatik oʻqib olinadi.</i>",
        "empty": "Kiritilmagan",
        
        # Buttons
        "btn_generate": "🚀 Asosnoma yaratish (DOCX)",
        "btn_edit_meta": "✏️ Rekvizitlarni tahrirlash",
        "btn_bot_lang": "🌐 Bot tilini oʻzgartirish",
        "btn_doc_lang": "📄 Hujjat tilini tanlash",
        "btn_commission": "👥 Komissiya aʼzolari",
        "btn_sample_test": "🧪 Namunaviy test fayllari",
        "btn_clear": "🗑 Tozalash / Qayta boshlash",
        "btn_help": "ℹ️ Yordam",
        "btn_admin_chat": "👨‍💻 Admin: @{admin}",
        "btn_donate": "☕️ Loyihani qoʻllab-quvvatlash (Donat)",
        "btn_taps_link": "☕️ Taps.uz orqali donat qilish",
        "btn_feedback": "✍️ Fikr / Murojaat",
        "btn_check_sub": "✅ Aʼzolikni tekshirish",
        "btn_sub_channel": "📢 Kanalga aʼzo boʻlish",
        "btn_back": "⬅️ Bosh menyuga qaytish",
        "btn_cancel": "❌ Bekor qilish",

        "feedback_prompt": (
            "✍️ <b>Adminga taklif, savol yoki shikoyatingizni yozing:</b>\n\n"
            "<i>(Istalgan matn, rasm yoki fayl yuborishingiz mumkin. Xabaringiz toʻgʻridan-toʻgʻri adminga yetkaziladi)</i>"
        ),
        "feedback_sent": "✅ <b>Xabaringiz adminga muvaffaqiyatli yetkazildi!</b>\n\nTez orada javob qaytariladi. Rahmat!",
        "err_scanned_pdf": (
            "⚠️ <b>Ushbu PDF fayl skaner qilingan (rasm) formatida!</b>\n\n"
            "Unda matn qatlami mavjud boʻlmaganligi sababli maʼlumotlarni avtomatik oʻqib boʻlmadi.\n"
            "Iltimos, Antiplagiat tizimidan yuklab olingan <b>original elektron PDF</b> faylni yuboring."
        ),
        "force_sub_prompt": (
            "📢 <b>DIQQAT: KANALGA AʼZO BOʻLISH TALAB ETILADI!</b>\n\n"
            "Botdan toʻliq foydalanish uchun rasmiy kanalimizga aʼzo boʻlishingiz lozim.\n\n"
            "1. Quyidagi <b>«📢 Kanalga aʼzo boʻlish»</b> tugmasi orqali aʼzo boʻling;\n"
            "2. Soʻngra <b>«✅ Aʼzolikni tekshirish»</b> tugmasini bosing."
        ),

        # Lang selection
        "choose_bot_lang": "🌐 <b>BOT INTERFEYSI TILINI TANLANG:</b>\n\nBot xabarlari va menyusi qaysi tilda koʻrinsin?",
        "bot_lang_changed": "✅ <b>Bot tili oʻzgartirildi:</b> {lang}",
        "choose_doc_lang": (
            "📄 <b>ASOSNOMA HUJJATINING TILINI TANLANG:</b>\n\n"
            "Tanlangan tilga mos ravishda Word hujjati sarlavhasi, jadval ustunlari, "
            "izoh matnlari va imzo bloki shakllantiriladi."
        ),
        "doc_lang_changed": "✅ <b>Asosnoma hujjati tili belgilandi:</b> {lang}",

        # Meta editing
        "edit_menu_title": "✏️ <b>REKVIZITARNI TAHRIRLASH:</b>",
        "btn_edit_fio": "👤 F.I.Sh",
        "btn_edit_uni": "🏛 Muassasa",
        "btn_edit_topic": "📚 Mavzu",
        "btn_edit_spec": "🔬 Ixtisosliklar",
        "prompt_fio": "Iltimos, tadqiqotchi/muallifning toʻliq F.I.Sh ini yozib yuboring:\n(Masalan: <code>Gʻaybullayev Sherzod Obid oʻgʻli</code>)",
        "prompt_uni": "Iltimos, OTM yoki ilmiy muassasa nomini yozib yuboring:\n(Masalan: <code>Samarqand davlat tibbiyot universiteti</code>)",
        "prompt_topic": "Iltimos, dissertatsiya mavzusini yozib yuboring:\n(Masalan: <code>Magnit-rezonans tomografiya tekshiruvida aniqlangan bosh miya oʻsmalarining patomorfologik xususiyatlari</code>)",
        "prompt_spec": "Iltimos, ixtisoslik shifri va nomini yozib yuboring:\n(Masalan: <code>14.00.15 – Patologik anatomiya, 14.00.19 – Klinik radiologiya</code>)",
        "meta_saved": "✅ <b>Maʼlumot muvaffaqiyatli saqlandi!</b>",

        # Commission
        "comm_title": "👥 <b>EKSPERT KOMISSIYASI AʼZOLARI:</b>\n",
        "comm_empty": "(boʻsh — Wordda/imzo uchun toʻldiriladi)",
        "btn_comm_edit": "✏️ {num}-aʼzoni kiritish",
        "btn_comm_reset": "🔄 Standart namunaga qaytarish",
        "comm_reset_done": "Standart komissiya aʼzolari tiklandi.",

        # Generation
        "generating": "⏳ <b>Asosnoma (.docx) hujjati shakllantirilmoqda...</b>",
        "gen_success": "✅ <b>Asosnoma hujjati muvaffaqiyatli tayyorlandi! ({lang})</b>",
        "gen_btn_other_lang": "<i>Boshqa tilda yuklab olish uchun quyidagi tugmalardan birini bosing:</i>",
        "need_report": "❌ Asosnoma yaratish uchun kamida bitta (Oʻzbekcha, Ruscha yoki Inglizcha) plagiat hisoboti zarur!",
        "cleared": "🗑 <b>Barcha maʼlumotlar va fayllar tozalandi.</b>",

        # Donate
        "donate_text": (
            "💝 <b>LOYIHANI QOʻLLAB-QUVVATLASH (DONAT)</b>\n\n"
            "Asosnoma Generator boti barcha ilmiy izlanuvchilar va tadqiqotchilar uchun bepul xizmat qiladi.\n\n"
            "Agar bot dissertatsiyangizni tayyorlashda ishingizni osonlashtirgan boʻlsa, uning server xarajatlarini qoplash, barqaror ishlashi va yanada yangi qulayliklar qoʻshilishi uchun loyihani qoʻllab-quvvatlashingiz mumkin!\n\n"
            "☕️ <b>Donat qilish havolasi:</b>\n"
            "👉 <a href='{url}'>taps.uz/shergaybullayev</a>\n\n"
            "Har qanday eʼtibor va samimiy qoʻllab-quvvatlashingiz uchun katta rahmat! 🙏"
        ),
    },

    "uz-cyrl": {
        "welcome": (
            "👋 <b>Ассалому алайкум!</b>\n\n"
            "<b>Асоснома Генератор Бот</b>га хуш келибсиз!\n"
            "Ушбу бот <b>antiplag.uz</b> тизимидан юклаб олинган PDF ҳисоботлар асосида "
            "ОАК талабларига тўлиқ мос келувчи расмий <b>«Асоснома» (.docx)</b> ҳужжатини "
            "автоматик равишда тайёрлаб беради.\n\n"
            "👨‍💻 <b>Бот админи:</b> @{admin}\n\n"
            "📥 <b>Бошлаш учун:</b>\n"
            "Антиплагиат ҳисобот файлларини (PDF) ботга юборинг ёки қуйидаги "
            "<b>«🧪 Намунавий тест файллари»</b> тугмаси орқали синаб кўринг!\n\n"
        ),
        "help": (
            "📖 <b>БОТДАН ФОЙДАЛАНИШ БЎЙИЧА ЙЎРИҚНОМА</b>\n\n"
            "1️⃣ <b>Файлларни юклаш:</b>\n"
            "• <b>uz.pdf</b> – Ўзбекча матн плагиат ҳисоботи\n"
            "• <b>ru.pdf</b> – Русча матн плагиат ҳисоботи\n"
            "• <b>eng.pdf</b> – Инглизча матн плагиат ҳисоботи\n"
            "• <b>si.pdf</b> – Сунъий интеллект (СИ) ҳисоботи\n"
            "• <b>namuna.docx</b> – Олдинги асоснома намунаси (ихтиёрий)\n"
            "• 📦 <b>ZIP / RAR</b> – Барча файлларни битта архивда юбориш ҳам мумкин\n\n"
            "2️⃣ <b>Автоматик тўлдириш:</b>\n"
            "PDF файллардан муаллиф Ф.И.Ш, мавзу, муассаса ва ихтисосликлар автоматик аниқланади.\n\n"
            "3️⃣ <b>Таҳрирлаш:</b>\n"
            "«✏️ Реквизитларни таҳрирлаш» орқали исталган маълумотни ўзгартириш мумкин.\n\n"
            "4️⃣ <b>Асоснома яратиш:</b>\n"
            "Камида битта ҳисобот юклангач, «🚀 Асоснома яратиш» тугмаси пайдо бўлади.\n\n"
            "👨‍💻 <b>Админ:</b> @{admin}\n"
        ),
        "admin": (
            "👨‍💻 <b>БОТ АДМИНИСТРАТОРИ:</b>\n\n"
            "• <b>Админ:</b> @{admin}\n"
            "• <b>Телеграм профил:</b> <a href='{url}'>t.me/{admin}</a>\n\n"
            "Саволлар, таклифлар ёки техник масалалар бўйича бемалол мурожаат қилишингиз мумкин!"
        ),
        "files_header": "📊 <b>ҲИСОБОТ ФАЙЛЛАРИ ҲОЛАТИ:</b>",
        "meta_header": "📋 <b>ҲУЖЖАТ РЕКВИЗИТЛАРИ:</b>",
        "rep_uz": "🇺🇿 Ўзбекча ҳисобот",
        "rep_ru": "🇷🇺 Русча ҳисобот",
        "rep_eng": "🇬🇧 Инглизча ҳисобот",
        "rep_ai": "🤖 Сунъий интеллект ҳисоботи",
        "rep_sample": "📄 Намуна (.docx)",
        "not_uploaded": "❌ <i>Юкланмаган</i>",
        "sample_active": "✅ фаол (махсус иборалар қўлланилади)",
        "sample_optional": "➖ <i>Ихтиёрий (стандарт иборалар)</i>",
        "sources_count": "{cnt} та манба",
        "fio_label": "👤 <b>Ф.И.Ш:</b>",
        "uni_label": "🏛 <b>Муассаса:</b>",
        "status_label": "🎓 <b>Мақом:</b>",
        "topic_label": "📚 <b>Мавзу:</b>",
        "spec_label": "🔬 <b>Ихтисослик:</b>",
        "degree_label": "📜 <b>Даража:</b>",
        "bot_lang_label": "🌐 <b>Бот тили:</b>",
        "doc_lang_label": "📄 <b>Ҳужжат тили:</b>",
        "admin_label": "👨‍💻 <b>Админ:</b>",
        "tip_files": "<i>💡 Файлларни (PDF, DOCX ёки ZIP/RAR архив) ботга юборишингиз мумкин. Маълумотлар автоматик ўқиб олинади.</i>",
        "empty": "Киритилмаган",
        
        # Buttons
        "btn_generate": "🚀 Асоснома яратиш (DOCX)",
        "btn_edit_meta": "✏️ Реквизитларни таҳрирлаш",
        "btn_bot_lang": "🌐 Бот тилини ўзгартириш",
        "btn_doc_lang": "📄 Ҳужжат тилини танлаш",
        "btn_commission": "👥 Комиссия аъзолари",
        "btn_sample_test": "🧪 Намунавий тест файллари",
        "btn_clear": "🗑 Тозалаш / Қайта бошлаш",
        "btn_help": "ℹ️ Ёрдам",
        "btn_admin_chat": "👨‍💻 Админ: @{admin}",
        "btn_donate": "☕️ Лойиҳани қўллаб-қувватлаш (Донат)",
        "btn_taps_link": "☕️ Taps.uz орқали донат қилиш",
        "btn_feedback": "✍️ Фикр / Мурожаат",
        "btn_check_sub": "✅ Аъзоликни текшириш",
        "btn_sub_channel": "📢 Каналга аъзо бўлиш",
        "btn_back": "⬅️ Бош менюга қайтиш",
        "btn_cancel": "❌ Бекор қилиш",

        "feedback_prompt": (
            "✍️ <b>Админга таклиф, савол ёки шикоятингизни ёзинг:</b>\n\n"
            "<i>(Исталган матн, расм ёки файл юборишингиз мумкин. Хабарингиз тўғридан-тўғри админга етказилади)</i>"
        ),
        "feedback_sent": "✅ <b>Хабарингиз админга муваффақиятли етказилди!</b>\n\nТез орада жавоб қайтарилади. Раҳмат!",
        "err_scanned_pdf": (
            "⚠️ <b>Ушбу PDF файл сканерланган (расм) форматида!</b>\n\n"
            "Унда матн қатлами мавжуд бўлмаганлиги сабабли маълумотларни автоматик ўқиб бўлмади.\n"
            "Илтимос, Антиплагиат тизимидан юклаб олинган <b>оригинал электрон PDF</b> файлни юборинг."
        ),
        "force_sub_prompt": (
            "📢 <b>ДИҚҚАТ: КАНАЛГА АЪЗО БЎЛИШ ТАЛАБ ЭТИЛАДИ!</b>\n\n"
            "Ботдан тўлиқ фойдаланиш учун расмий каналимизга аъзо бўлишингиз лозим.\n\n"
            "1. Қуйидаги <b>«📢 Каналга аъзо бўлиш»</b> тугмаси орқали аъзо бўлинг;\n"
            "2. Сўнгра <b>«✅ Аъзоликни текшириш»</b> тугмасини босинг."
        ),

        # Lang selection
        "choose_bot_lang": "🌐 <b>БОТ ИНТЕРФЕЙСИ ТИЛИНИ ТАНЛАНГ:</b>\n\nБот хабарлари ва менюси қайси тилда кўринсин?",
        "bot_lang_changed": "✅ <b>Бот тили ўзгартирилди:</b> {lang}",
        "choose_doc_lang": (
            "📄 <b>АСОСНОМА ҲУЖЖАТИНИНГ ТИЛИНИ ТАНЛАНГ:</b>\n\n"
            "Танланган тилга мос равишда Word ҳужжати сарлавҳаси, жадвал устунлари, "
            "изоҳ матнлари ва имзо блоки шакллантирилади."
        ),
        "doc_lang_changed": "✅ <b>Асоснома ҳужжати тили белгиланди:</b> {lang}",

        # Meta editing
        "edit_menu_title": "✏️ <b>РЕКВИЗИТАРНИ ТАҲРИРЛАШ:</b>",
        "btn_edit_fio": "👤 Ф.И.Ш",
        "btn_edit_uni": "🏛 Муассаса",
        "btn_edit_topic": "📚 Мавзу",
        "btn_edit_spec": "🔬 Ихтисосликлар",
        "prompt_fio": "Илтимос, тадқиқотчи/муаллифнинг тўлиқ Ф.И.Ш ини ёзиб юборинг:\n(Масалан: <code>Гайбуллаев Шерзод Обид ўғли</code>)",
        "prompt_uni": "Илтимос, ОТМ ёки илмий муассаса номини ёзиб юборинг:\n(Масалан: <code>Самарқанд давлат тиббиёт университети</code>)",
        "prompt_topic": "Илтимос, диссертация мавзусини ёзиб юборинг:\n(Масалан: <code>Магнит-резонанс томография текширувида аниқланган бош мия ўсмаларининг патоморфологик хусусиятлари</code>)",
        "prompt_spec": "Илтимос, ихтисослик шифри ва номини ёзиб юборинг:\n(Масалан: <code>14.00.15 – Патологик анатомия, 14.00.19 – Клиник радиология</code>)",
        "meta_saved": "✅ <b>Маълумот муваффақиятли сақланди!</b>",

        # Commission
        "comm_title": "👥 <b>ЭКСПЕРТ КОМИССИЯСИ АЪЗОЛАРИ:</b>\n",
        "comm_empty": "(бўш — Wordда/имзо учун тўлдирилади)",
        "btn_comm_edit": "✏️ {num}-аъзони киритиш",
        "btn_comm_reset": "🔄 Стандарт намунага қайтариш",
        "comm_reset_done": "Стандарт комиссия аъзолари тикланди.",

        # Generation
        "generating": "⏳ <b>Асоснома (.docx) ҳужжати шакллантирилмоқда...</b>",
        "gen_success": "✅ <b>Асоснома ҳужжати муваффақиятли тайёрланди! ({lang})</b>",
        "gen_btn_other_lang": "<i>Бошқа тилда юклаб олиш учун қуйидаги тугмалардан бирини босинг:</i>",
        "need_report": "❌ Асоснома яратиш учун камида битта (Ўзбекча, Русча ёки Инглизча) плагиат ҳисоботи зарур!",
        "cleared": "🗑 <b>Барча маълумотлар ва файллар тозаланди.</b>",

        # Donate
        "donate_text": (
            "💝 <b>ЛОЙИҲАНИ ҚЎЛЛАБ-ҚУВВАТЛАШ (ДОНАТ)</b>\n\n"
            "Асоснома Генератор боти барча илмий изланувчилар ва тадқиқотчилар учун бепул хизмат қилади.\n\n"
            "Агар бот диссертациянгизни тайёрлашда ишингизни осонлаштирган бўлса, унинг сервер харажатларини қоплаш, барқарор ишлаши ва янада янги қулайликлар қўшилиши учун лойиҳани қўллаб-қувватлашингиз мумкин!\n\n"
            "☕️ <b>Донат қилиш ҳаволаси:</b>\n"
            "👉 <a href='{url}'>taps.uz/shergaybullayev</a>\n\n"
            "Ҳар қандай эътибор ва самимий қўллаб-қувватлашингиз учун катта раҳмат! 🙏"
        ),
    },

    "ru": {
        "welcome": (
            "👋 <b>Здравствуйте!</b>\n\n"
            "Добро пожаловать в <b>Бот-генератор Обоснования (Асоснома)</b>!\n"
            "Бот автоматически формирует официальный документ <b>«Обоснование» (.docx)</b>, "
            "соответствующий всем требованиям ВАК, на основе PDF-отчетов <b>antiplag.uz</b>.\n\n"
            "👨‍💻 <b>Администратор бота:</b> @{admin}\n\n"
            "📥 <b>Чтобы начать:</b>\n"
            "Отправьте боту PDF-отчеты проверки или протестируйте с помощью кнопки "
            "<b>«🧪 Тестовые образцы»</b>!\n\n"
        ),
        "help": (
            "📖 <b>ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ БОТА</b>\n\n"
            "1️⃣ <b>Загрузка файлов:</b>\n"
            "• <b>uz.pdf</b> – Отчет антиплагиата на узбекском\n"
            "• <b>ru.pdf</b> – Отчет антиплагиата на русском\n"
            "• <b>eng.pdf</b> – Отчет антиплагиата на английском\n"
            "• <b>si.pdf</b> – Отчет проверки на искусственный интеллект (ИИ)\n"
            "• <b>namuna.docx</b> – Образец предыдущего обоснования (необязательно)\n"
            "• 📦 <b>ZIP / RAR</b> – Можно отправить все файлы одним архивом\n\n"
            "2️⃣ <b>Автозаполнение:</b>\n"
            "Ф.И.О., тема, учреждение и специальности автоматически извлекаются из PDF.\n\n"
            "3️⃣ <b>Редактирование:</b>\n"
            "С помощью кнопки «✏️ Редактировать реквизиты» можно изменить любые данные.\n\n"
            "4️⃣ <b>Генерация документа:</b>\n"
            "После загрузки отчетов нажмите «🚀 Создать обоснование».\n\n"
            "👨‍💻 <b>Админ:</b> @{admin}\n"
        ),
        "admin": (
            "👨‍💻 <b>АДМИНИСТРАТОР БОТА:</b>\n\n"
            "• <b>Админ:</b> @{admin}\n"
            "• <b>Ссылка:</b> <a href='{url}'>t.me/{admin}</a>\n\n"
            "По вопросам и предложениям обращайтесь к администратору!"
        ),
        "files_header": "📊 <b>СОСТОЯНИЕ ФАЙЛОВ ОТЧЕТОВ:</b>",
        "meta_header": "📋 <b>РЕКВИЗИТЫ ДОКУМЕНТА:</b>",
        "rep_uz": "🇺🇿 Отчет на узбекском",
        "rep_ru": "🇷🇺 Отчет на русском",
        "rep_eng": "🇬🇧 Отчет на английском",
        "rep_ai": "🤖 Отчет проверки на ИИ",
        "rep_sample": "📄 Образец (.docx)",
        "not_uploaded": "❌ <i>Не загружен</i>",
        "sample_active": "✅ активен (используются фразы образца)",
        "sample_optional": "➖ <i>Необязательно (стандартные фразы)</i>",
        "sources_count": "{cnt} источников",
        "fio_label": "👤 <b>Ф.И.О:</b>",
        "uni_label": "🏛 <b>Учреждение:</b>",
        "status_label": "🎓 <b>Статус:</b>",
        "topic_label": "📚 <b>Тема:</b>",
        "spec_label": "🔬 <b>Специальности:</b>",
        "degree_label": "📜 <b>Степень:</b>",
        "bot_lang_label": "🌐 <b>Язык бота:</b>",
        "doc_lang_label": "📄 <b>Язык документа:</b>",
        "admin_label": "👨‍💻 <b>Админ:</b>",
        "tip_files": "<i>💡 Отправляйте файлы (PDF, DOCX или ZIP/RAR архив) боту. Данные считываются автоматически.</i>",
        "empty": "Не указано",
        
        # Buttons
        "btn_generate": "🚀 Создать обоснование (DOCX)",
        "btn_edit_meta": "✏️ Редактировать реквизиты",
        "btn_bot_lang": "🌐 Сменить язык бота",
        "btn_doc_lang": "📄 Выбрать язык документа",
        "btn_commission": "👥 Члены комиссии",
        "btn_sample_test": "🧪 Тестовые образцы",
        "btn_clear": "🗑 Очистить данные",
        "btn_help": "ℹ️ Помощь",
        "btn_admin_chat": "👨‍💻 Админ: @{admin}",
        "btn_donate": "☕️ Поддержать проект (Донат)",
        "btn_taps_link": "☕️ Поддержать через Taps.uz",
        "btn_feedback": "✍️ Обратная связь",
        "btn_check_sub": "✅ Проверить подписку",
        "btn_sub_channel": "📢 Подписаться на канал",
        "btn_back": "⬅️ В главное меню",
        "btn_cancel": "❌ Отмена",

        "feedback_prompt": (
            "✍️ <b>Напишите ваш вопрос, предложение или сообщение админу:</b>\n\n"
            "<i>(Вы можете отправить текст, фото или файл. Ваше сообщение будет передано администратору)</i>"
        ),
        "feedback_sent": "✅ <b>Ваше сообщение успешно отправлено администратору!</b>\n\nОтвет поступит в ближайшее время.",
        "err_scanned_pdf": (
            "⚠️ <b>Этот PDF-файл представляет собой отсканированное изображение!</b>\n\n"
            "В нем отсутствует текстовый слой, поэтому данные невозможно считать автоматически.\n"
            "Пожалуйста, отправьте оригинальный электронный PDF-файл из системы «Антиплагиат»."
        ),
        "force_sub_prompt": (
            "📢 <b>ВНИМАНИЕ: ТРЕБУЕТСЯ ПОДПИСКА НА КАНАЛ!</b>\n\n"
            "Для использования бота необходимо подписаться на наш официальный канал.\n\n"
            "1. Нажмите <b>«📢 Подписаться на канал»</b>;\n"
            "2. Затем нажмите <b>«✅ Проверить подписку»</b>."
        ),

        # Lang selection
        "choose_bot_lang": "🌐 <b>ВЫБЕРИТЕ ЯЗЫК ИНТЕРФЕЙСА БОТА:</b>\n\nНа каком языке отображать меню и сообщения?",
        "bot_lang_changed": "✅ <b>Язык бота изменен:</b> {lang}",
        "choose_doc_lang": (
            "📄 <b>ВЫБЕРИТЕ ЯЗЫК ДОКУМЕНТА (ОБОСНОВАНИЯ):</b>\n\n"
            "В соответствии с выбранным языком формируются заголовок, колонки таблицы, "
            "примечания и блок подписей комиссии."
        ),
        "doc_lang_changed": "✅ <b>Язык документа установлен:</b> {lang}",

        # Meta editing
        "edit_menu_title": "✏️ <b>РЕДАКТИРОВАНИЕ РЕКВИЗИТОВ:</b>",
        "btn_edit_fio": "👤 Ф.И.О",
        "btn_edit_uni": "🏛 Учреждение",
        "btn_edit_topic": "📚 Тема",
        "btn_edit_spec": "🔬 Специальности",
        "prompt_fio": "Введите полное Ф.И.О автора:\n(Например: <code>Гайбуллаев Шерзод Обид ўғли</code>)",
        "prompt_uni": "Введите название учреждения:\n(Например: <code>Самаркандский государственный медицинский университет</code>)",
        "prompt_topic": "Введите тему диссертации:\n(Например: <code>Патоморфологические особенности опухолей головного мозга...</code>)",
        "prompt_spec": "Введите шифр и наименования специальностей:\n(Например: <code>14.00.15 – Патологическая анатомия...</code>)",
        "meta_saved": "✅ <b>Данные успешно сохранены!</b>",

        # Commission
        "comm_title": "👥 <b>ЧЛЕНЫ ЭКСПЕРТНОЙ КОМИССИИ:</b>\n",
        "comm_empty": "(пусто — для подписи в Word)",
        "btn_comm_edit": "✏️ Ввести {num}-го члена",
        "btn_comm_reset": "🔄 Сбросить к стандарту",
        "comm_reset_done": "Стандартные члены комиссии восстановлены.",

        # Generation
        "generating": "⏳ <b>Формирование документа Обоснование (.docx)...</b>",
        "gen_success": "✅ <b>Документ успешно сформирован! ({lang})</b>",
        "gen_btn_other_lang": "<i>Для скачивания на другом языке нажмите одну из кнопок ниже:</i>",
        "need_report": "❌ Для создания обоснования требуется хотя бы один отчет антиплагиата!",
        "cleared": "🗑 <b>Все данные и файлы очищены.</b>",

        # Donate
        "donate_text": (
            "💝 <b>ПОДДЕРЖКА ПРОЕКТА (ДОНАТ)</b>\n\n"
            "Бот Асоснома Генератор создан для бесплатной помощи исследователям и ученым.\n\n"
            "Если бот помог вам сэкономить время при подготовке диссертации, вы можете поддержать проект для покрытия расходов на сервер и внедрения новых функций!\n\n"
            "☕️ <b>Ссылка для доната:</b>\n"
            "👉 <a href='{url}'>taps.uz/shergaybullayev</a>\n\n"
            "Искренне благодарим за внимание и поддержку! 🙏"
        ),
    },

    "en": {
        "welcome": (
            "👋 <b>Welcome!</b>\n\n"
            "Welcome to the <b>Asosnoma Generator Bot</b>!\n"
            "This bot automatically generates an official <b>Justification / Asosnoma (.docx)</b> "
            "document based on <b>antiplag.uz</b> PDF reports.\n\n"
            "👨‍💻 <b>Bot admin:</b> @{admin}\n\n"
            "📥 <b>To get started:</b>\n"
            "Send your PDF reports to the bot or test it using the "
            "<b>«🧪 Sample test files»</b> button below!\n\n"
        ),
        "help": (
            "📖 <b>USER GUIDE</b>\n\n"
            "1️⃣ <b>Upload files:</b>\n"
            "• <b>uz.pdf</b> – Uzbek anti-plagiarism report\n"
            "• <b>ru.pdf</b> – Russian anti-plagiarism report\n"
            "• <b>eng.pdf</b> – English anti-plagiarism report\n"
            "• <b>si.pdf</b> – AI-detector report\n"
            "• <b>namuna.docx</b> – Previous template docx (optional)\n"
            "• 📦 <b>ZIP / RAR</b> – You can send all files in a single archive\n\n"
            "2️⃣ <b>Auto-filling:</b>\n"
            "Author's name, topic, institution, and specialities are parsed automatically from PDFs.\n\n"
            "3️⃣ <b>Editing:</b>\n"
            "Use «✏️ Edit metadata» to modify any field.\n\n"
            "4️⃣ <b>Generate document:</b>\n"
            "Once reports are uploaded, click «🚀 Generate Asosnoma».\n\n"
            "👨‍💻 <b>Admin:</b> @{admin}\n"
        ),
        "admin": (
            "👨‍💻 <b>BOT ADMINISTRATOR:</b>\n\n"
            "• <b>Admin:</b> @{admin}\n"
            "• <b>Telegram:</b> <a href='{url}'>t.me/{admin}</a>\n\n"
            "Feel free to reach out for questions and suggestions!"
        ),
        "files_header": "📊 <b>REPORT FILES STATUS:</b>",
        "meta_header": "📋 <b>DOCUMENT METADATA:</b>",
        "rep_uz": "🇺🇿 Uzbek report",
        "rep_ru": "🇷🇺 Russian report",
        "rep_eng": "🇬🇧 English report",
        "rep_ai": "🤖 AI detector report",
        "rep_sample": "📄 Sample (.docx)",
        "not_uploaded": "❌ <i>Not uploaded</i>",
        "sample_active": "✅ active (custom phrases applied)",
        "sample_optional": "➖ <i>Optional (standard phrases)</i>",
        "sources_count": "{cnt} sources",
        "fio_label": "👤 <b>Author name:</b>",
        "uni_label": "🏛 <b>Institution:</b>",
        "status_label": "🎓 <b>Status:</b>",
        "topic_label": "📚 <b>Topic:</b>",
        "spec_label": "🔬 <b>Specialities:</b>",
        "degree_label": "📜 <b>Degree:</b>",
        "bot_lang_label": "🌐 <b>Bot language:</b>",
        "doc_lang_label": "📄 <b>Doc language:</b>",
        "admin_label": "👨‍💻 <b>Admin:</b>",
        "tip_files": "<i>💡 Send files (PDF, DOCX, or ZIP/RAR archive) to the bot. Metadata is extracted automatically.</i>",
        "empty": "Not set",
        
        # Buttons
        "btn_generate": "🚀 Generate Justification (DOCX)",
        "btn_edit_meta": "✏️ Edit metadata",
        "btn_bot_lang": "🌐 Change Bot Language",
        "btn_doc_lang": "📄 Change Document Language",
        "btn_commission": "👥 Commission members",
        "btn_sample_test": "🧪 Sample test files",
        "btn_clear": "🗑 Clear / Reset",
        "btn_help": "ℹ️ Help",
        "btn_admin_chat": "👨‍💻 Admin: @{admin}",
        "btn_donate": "☕️ Support Project (Donate)",
        "btn_taps_link": "☕️ Donate via Taps.uz",
        "btn_feedback": "✍️ Feedback / Support",
        "btn_check_sub": "✅ Check Subscription",
        "btn_sub_channel": "📢 Subscribe to Channel",
        "btn_back": "⬅️ Back to Main Menu",
        "btn_cancel": "❌ Cancel",

        "feedback_prompt": (
            "✍️ <b>Write your message, question, or feedback to the admin:</b>\n\n"
            "<i>(You can send text, a photo, or a file. Your message will be forwarded directly to the admin)</i>"
        ),
        "feedback_sent": "✅ <b>Your message has been successfully delivered to the admin!</b>\n\nYou will receive a response soon. Thank you!",
        "err_scanned_pdf": (
            "⚠️ <b>This PDF is a scanned image!</b>\n\n"
            "It does not contain an electronic text layer, so metadata could not be read.\n"
            "Please upload the <b>original electronic PDF</b> report downloaded from the Antiplagiat system."
        ),
        "force_sub_prompt": (
            "📢 <b>ATTENTION: CHANNEL SUBSCRIPTION REQUIRED!</b>\n\n"
            "To use this bot, you must subscribe to our official channel.\n\n"
            "1. Click <b>«📢 Subscribe to Channel»</b> below;\n"
            "2. Then click <b>«✅ Check Subscription»</b>."
        ),

        # Lang selection
        "choose_bot_lang": "🌐 <b>CHOOSE BOT INTERFACE LANGUAGE:</b>\n\nIn which language would you like the bot messages and menus?",
        "bot_lang_changed": "✅ <b>Bot language updated:</b> {lang}",
        "choose_doc_lang": (
            "📄 <b>CHOOSE JUSTIFICATION DOCUMENT LANGUAGE:</b>\n\n"
            "The title, table columns, comments, and signature blocks in Word will be generated in the selected language."
        ),
        "doc_lang_changed": "✅ <b>Document language updated:</b> {lang}",

        # Meta editing
        "edit_menu_title": "✏️ <b>EDIT METADATA:</b>",
        "btn_edit_fio": "👤 Author F.I.O",
        "btn_edit_uni": "🏛 Institution",
        "btn_edit_topic": "📚 Topic",
        "btn_edit_spec": "🔬 Specialities",
        "prompt_fio": "Please enter the author's full name:\n(Example: <code>Sherzod Obid ugli Gaybullayev</code>)",
        "prompt_uni": "Please enter institution name:\n(Example: <code>Samarkand State Medical University</code>)",
        "prompt_topic": "Please enter dissertation topic:",
        "prompt_spec": "Please enter specialities code and title:",
        "meta_saved": "✅ <b>Saved successfully!</b>",

        # Commission
        "comm_title": "👥 <b>EXPERT COMMISSION MEMBERS:</b>\n",
        "comm_empty": "(blank — for signature in Word)",
        "btn_comm_edit": "✏️ Enter #{num} member",
        "btn_comm_reset": "🔄 Reset to standard",
        "comm_reset_done": "Commission members reset to default.",

        # Generation
        "generating": "⏳ <b>Generating Justification (.docx) document...</b>",
        "gen_success": "✅ <b>Justification document successfully generated! ({lang})</b>",
        "gen_btn_other_lang": "<i>To download in another language, click one of the buttons below:</i>",
        "need_report": "❌ At least one anti-plagiarism report is required to generate the justification!",
        "cleared": "🗑 <b>All data and uploaded files have been cleared.</b>",

        # Donate
        "donate_text": (
            "💝 <b>SUPPORT THE PROJECT (DONATE)</b>\n\n"
            "Asosnoma Generator bot is provided free of charge for researchers and scientists.\n\n"
            "If the bot has helped save your time, you are welcome to support the project to cover server maintenance and encourage future features!\n\n"
            "☕️ <b>Donation link:</b>\n"
            "👉 <a href='{url}'>taps.uz/shergaybullayev</a>\n\n"
            "Thank you warmly for your attention and encouragement! 🙏"
        ),
    }
}


def t(key: str, lang: str = "uz-latn", **kwargs) -> str:
    """Translate key to specified language with optional formatting."""
    lang_dict = TEXTS.get(lang, TEXTS["uz-latn"])
    text = lang_dict.get(key, TEXTS["uz-latn"].get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
