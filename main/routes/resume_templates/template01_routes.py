# main/routes/resume_templates/template01_routes.py
from flask import Blueprint, render_template, url_for
from ...models.models import ResumeSection
from ...extensions import db

template01_bp = Blueprint('template01', __name__, url_prefix='/resume/template01')


@template01_bp.route("/")
def show_template01():
    sections = (
        ResumeSection.query
        .filter_by(is_visible=True)
        .order_by(ResumeSection.order)
        .all()
    )

    return render_template("resume_templates/template01.j2", sections=sections)





