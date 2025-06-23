from flask import Blueprint, render_template, request, redirect, url_for
from main.models import db
from main.models.resume_section import ResumeSection
from main.models.resume_paragraph import ResumeParagraph
from main.models.resume_field import ResumeField
from main.models.resume_setting import Setting
from main.models.Section import Section
from main.models.LanguageOption import LanguageOption
from main.models.NavigationLink import NavigationLink

from flask_babel import force_locale
from main.i18n_runtime import get_locale
import json

from . import admin_bp


@admin_bp.route("/sections", methods=["GET", "POST"])
def manage_sections():
    """
    Handle GET and POST requests for managing resume sections.

    Returns:
        Response: Rendered template or redirect.
    """
    if request.method == "POST":
        for section_id, content in request.form.items():
            section = Section.query.get(int(section_id))
            if section:
                section.content = content
        db.session.commit()
        return redirect(url_for("admin.manage_sections"))

    sections = Section.query.all()
    return render_template("admin/sections.html.j2", sections=sections)


@admin_bp.route("/settings", methods=["GET", "POST"])
def manage_settings():
    """
    Manage and save styling and configuration settings.

    Returns:
        Response: Rendered template or redirect.
    """
    error = None
    settings = Setting.query.all()

    if request.method == "POST":
        try:
            font_size = request.form.get("section_title_css_font_size")
            color = request.form.get("section_title_css_color")
            weight = request.form.get("section_title_css_weight")
            if not font_size or not color or not weight:
                raise ValueError("Section title CSS values cannot be empty.")
            css_json = {
                "font-size": font_size,
                "color": color,
                "font-weight": weight
            }
            setting = Setting.query.filter_by(key="section_title_css").first()
            if setting:
                setting.value = json.dumps(css_json)

            p_font_size = request.form.get("paragraph_css_font_size")
            p_color = request.form.get("paragraph_css_color")
            if not p_font_size or not p_color:
                raise ValueError("Paragraph CSS values cannot be empty.")
            paragraph_css_json = {
                "font-size": p_font_size,
                "color": p_color
            }
            p_setting = Setting.query.filter_by(key="paragraph_css").first()
            if p_setting:
                p_setting.value = json.dumps(paragraph_css_json)

            body_font = request.form.get("body_font")
            b_setting = Setting.query.filter_by(key="body_font").first()
            if b_setting:
                b_setting.value = body_font

            json_keys = ["section_title_css", "paragraph_css"]
            skip_keys = [
                "section_title_css_font_size", "section_title_css_color", "section_title_css_weight",
                "paragraph_css_font_size", "paragraph_css_color",
                "body_font", "dark_mode_enabled"
            ]

            for key, value in request.form.items():
                if key in skip_keys:
                    continue
                s = Setting.query.filter_by(key=key).first()
                if s:
                    if key in json_keys:
                        try:
                            json.loads(value.replace("'", '"'))
                        except Exception:
                            raise ValueError(f"Invalid JSON value for setting: {key}")
                    s.value = value

            dark_value = request.form.get("dark_mode_enabled", "false")
            dark_setting = Setting.query.filter_by(key="dark_mode_enabled").first()
            if dark_setting:
                dark_setting.value = dark_value

            db.session.commit()

            action = request.form.get("action")
            if action == "save_and_preview":
                return redirect(url_for("public.resume"))
            return redirect(url_for("admin.manage_settings"))

        except Exception as e:
            error = f"Error in JSON format: {str(e)}"

    section_title_css_data = {
        "font-size": "20px",
        "color": "#000000",
        "font-weight": "normal"
    }

    paragraph_css_data = {
        "font-size": "14px",
        "color": "#444444"
    }

    body_font_value = "Arial, sans-serif"

    for s in settings:
        if s.key == "section_title_css":
            try:
                section_title_css_data = json.loads(s.value.replace("'", '"'))
            except Exception:
                pass
        elif s.key == "paragraph_css":
            try:
                paragraph_css_data = json.loads(s.value.replace("'", '"'))
            except Exception:
                pass
        elif s.key == "body_font":
            body_font_value = s.value

    with force_locale(get_locale()):
        settings_dict = {s.key: s.value for s in settings}
        return render_template(
            "admin/settings.html.j2",
            settings=settings,
            settings_dict=settings_dict,
            error=error,
            section_title_css_data=section_title_css_data,
            paragraph_css_data=paragraph_css_data,
            body_font_value=body_font_value
        )
