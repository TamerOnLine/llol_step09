# routes/resume_display.py
from flask import Blueprint, render_template, request
from main.extensions import db
from main.models.resume_section import ResumeSection


from main.models.resume_paragraph import ResumeParagraph
from main.models.resume_field import ResumeField

template01_bp = Blueprint("template01", __name__)

@template01_bp.route("/resume")
def display_resume():
    lang = request.args.get("lang", "en")  # اللغة الافتراضية "en"
    
    sections = (
        ResumeSection.query
        .filter_by(is_visible=True)
        .order_by(ResumeSection.order)
        .all()
    )
    

    # بناء الهيكل المنظم للسيرة الذاتية
    resume_data = []
    for section in sections:
        section_title = section.title_translations.get(lang, section.title) if section.title_translations else section.title
        
        paragraphs_data = []
        for paragraph in section.paragraphs:
            if not paragraph.is_visible:
                continue
            paragraph_title = paragraph.title_translations.get(lang, "") if paragraph.title_translations else ""
            
            fields_data = []
            for field in paragraph.fields:
                if not field.is_visible:
                    continue
                fields_data.append({
                    "label": field.label,
                    "value": field.value,
                    "description": field.description,
                    "type": field.field_type,
                })
            
            paragraphs_data.append({
                "title": paragraph_title,
                "type": paragraph.field_type,
                "location": paragraph.location,
                "fields": fields_data
            })
        
        resume_data.append({
            "title": section_title,
            "paragraphs": paragraphs_data
        })

    return render_template("resume_templates/template01.j2", resume_data=resume_data, lang=lang)