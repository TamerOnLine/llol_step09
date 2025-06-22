from pathlib import Path
import os
import polib
from main.extensions import db
from main.models.models import NavigationLink  # ← عدّل هذا حسب مكان الكلاس
from main import create_app

LANGUAGES = ["ar", "de"]

def create_clean_po(language_code):
    po = polib.POFile()
    po.metadata = {
        'Project-Id-Version': 'Resume Project',
        'Report-Msgid-Bugs-To': 'EMAIL@ADDRESS',
        'POT-Creation-Date': '2025-06-11 14:15+0200',
        'PO-Revision-Date': 'YEAR-MO-DA HO:MI+ZONE',
        'Last-Translator': 'FULL NAME <EMAIL@ADDRESS>',
        'Language-Team': f'{language_code} <LL@li.org>',
        'Language': language_code,
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Transfer-Encoding': '8bit',
        'Generated-By': 'Custom i18n Tool',
    }
    return po

def ensure_labels_in_po(labels, po_path: Path, lang_code: str):
    po_path.parent.mkdir(parents=True, exist_ok=True)  # <-- حل الخطأ النهائي

    if not po_path.exists() or os.path.getsize(po_path) < 10:
        print(f"⚠️ ملف {po_path} غير موجود أو فاسد. يتم إنشاؤه...")
        po = create_clean_po(lang_code)
        po.save(str(po_path))  # ← نحفظ الملف بعد إنشاءه
    try:
        po = polib.pofile(str(po_path))
    except Exception as e:
        print(f"❌ فشل فتح الملف {po_path.name}: {e}")
        po = create_clean_po(lang_code)
        po.save(str(po_path))

    existing_msgids = {entry.msgid for entry in po}
    added = 0

    for label in labels:
        if label and label not in existing_msgids:
            po.append(polib.POEntry(msgid=label, msgstr=""))
            added += 1

    if added:
        po.save(str(po_path))
        print(f"✅ تمت إضافة {added} عبارة جديدة إلى: {po_path.name}")
    else:
        print(f"ℹ️ لا توجد عبارات جديدة في: {po_path.name}")


# التشغيل داخل التطبيق
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        labels = [link.label for link in NavigationLink.query.all()]
        for lang in LANGUAGES:
            po_path = Path(f"main/translations/{lang}/LC_MESSAGES/messages.po")
            ensure_labels_in_po(labels, po_path, lang)
