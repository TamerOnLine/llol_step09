from flask import Blueprint, render_template
from ...models.Section import Section
from ...models.resume_paragraph import ResumeParagraph
from ...models.resume_field import ResumeField
from collections import defaultdict

template01_bp = Blueprint("template01", __name__, url_prefix="/resume/template01")

@template01_bp.route("/")
def show_template01():
    sections = Section.query.order_by(Section.order).all()
    section_paragraphs = defaultdict(list)

    for section in sections:
        paragraphs = ResumeParagraph.query.filter_by(resume_section_id=section.id).order_by(ResumeParagraph.order).all()
        for paragraph in paragraphs:
            fields = ResumeField.query.filter_by(resume_paragraph_id=paragraph.id).order_by(ResumeField.order).all()
            section_paragraphs[section.id].append({
                "paragraph": paragraph,
                "fields": fields
            })

    return render_template(
        "resume_templates/template01.j2",
        sections=sections,
        section_paragraphs=section_paragraphs
    )
