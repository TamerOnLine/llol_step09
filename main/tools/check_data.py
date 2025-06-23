from flask import Flask
from main import create_app
from main.models.resume_section import ResumeSection
from main.models.resume_paragraph import ResumeParagraph
from main.models.resume_field import ResumeField
from main.models.resume_setting import Setting
from main.models.LanguageOption import LanguageOption
from main.models.NavigationLink import NavigationLink
from main.extensions import db


app = create_app()


def get_translation(translations, lang="de"):
    return translations.get(lang) if translations else "—"

with app.app_context():
    print("🧩 الأقسام والفقرات والحقول:\n")
    sections = ResumeSection.query.order_by(ResumeSection.order).all()
    for sec in sections:
        print(f"{sec.order}: {sec.title} ({len(sec.paragraphs)} فقرات)")
        for para in sec.paragraphs:
            print(f"    - فقرة ID {para.id}: {get_translation(para.title_translations)} ({len(para.fields)} حقول)")

    print("\n⚙️ الإعدادات الموجودة:\n")
    for s in Setting.query.all():
        print(f"  - {s.key}: {s.value}")

    print("\n🌐 اللغات المدعومة:\n")
    for lang in LanguageOption.query.order_by(LanguageOption.order).all():
        print(f"  - {lang.code} – {lang.name} (الترتيب: {lang.order})")

    print("\n🔗 روابط التنقل:\n")
    for link in NavigationLink.query.order_by(NavigationLink.order).all():
        print(f"  - {link.label} ({link.endpoint}) – ترتيب: {link.order}")
