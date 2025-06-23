from flask import Blueprint, render_template, request, redirect, url_for, flash
from main.extensions import db
from main.models.resume_section import ResumeSection
from main.models.resume_paragraph import ResumeParagraph
from main.i18n_runtime import get_locale
from flask_babel import force_locale, gettext as _
from . import admin_bp

# عرض فقرات قسم محدد
@admin_bp.route('/section/<int:section_id>/view')
def single_section_view(section_id):
    section = ResumeSection.query.get_or_404(section_id)
    paragraphs = section.paragraphs
    with force_locale(get_locale()):
        return render_template('admin/single_section_view.html.j2', section=section, paragraphs=paragraphs)

# إضافة فقرة جديدة إلى قسم
@admin_bp.route('/paragraph/add/<int:section_id>', methods=['POST'])
def add_paragraph(section_id):
    section = ResumeSection.query.get_or_404(section_id)
    paragraph_type = request.form.get('type', 'basic')
    order = int(request.form.get('order', 0))
    is_visible = 'is_visible' in request.form
    location = request.form.get('location', 'main')

    paragraph = ResumeParagraph(
        resume_section_id=section.id,
        field_type=paragraph_type,
        order=order,
        is_visible=is_visible,
        location=location
    )
    db.session.add(paragraph)
    db.session.commit()
    with force_locale(get_locale()):
        flash(_("Paragraph added successfully"), "success")
    return redirect(url_for('admin.single_section_view', section_id=section.id))

# تعديل فقرة
@admin_bp.route('/paragraph/edit/<int:paragraph_id>', methods=['POST'])
def edit_paragraph(paragraph_id):
    paragraph = ResumeParagraph.query.get_or_404(paragraph_id)
    paragraph.field_type = request.form.get('type', paragraph.field_type)
    paragraph.order = int(request.form.get('order', paragraph.order))
    paragraph.is_visible = 'is_visible' in request.form
    paragraph.location = request.form.get('location', paragraph.location)
    db.session.commit()
    with force_locale(get_locale()):
        flash(_("Paragraph updated successfully"), "success")
    return redirect(url_for('admin.single_section_view', section_id=paragraph.resume_section_id))

# حذف فقرة
@admin_bp.route('/paragraph/delete/<int:paragraph_id>', methods=['POST'])
def delete_paragraph(paragraph_id):
    paragraph = ResumeParagraph.query.get_or_404(paragraph_id)
    section_id = paragraph.resume_section_id
    db.session.delete(paragraph)
    db.session.commit()
    with force_locale(get_locale()):
        flash(_("Paragraph deleted"), "danger")
    return redirect(url_for('admin.single_section_view', section_id=section_id))

# تبديل حالة الظهور للفقرة
@admin_bp.route('/paragraph/toggle_visibility/<int:paragraph_id>', methods=['POST'])
def toggle_paragraph_visibility(paragraph_id):
    paragraph = ResumeParagraph.query.get_or_404(paragraph_id)
    paragraph.is_visible = not paragraph.is_visible
    db.session.commit()
    with force_locale(get_locale()):
        if paragraph.is_visible:
            flash(_("Paragraph is now visible"), "success")
        else:
            flash(_("Paragraph is now hidden"), "warning")
    return redirect(url_for('admin.single_section_view', section_id=paragraph.resume_section_id))

# تحريك فقرة لأعلى
@admin_bp.route('/paragraph/move_up/<int:paragraph_id>', methods=['POST'])
def move_paragraph_up(paragraph_id):
    paragraph = ResumeParagraph.query.get_or_404(paragraph_id)
    section = paragraph.resume_section
    previous = ResumeParagraph.query.filter(
        ResumeParagraph.resume_section_id == section.id,
        ResumeParagraph.order < paragraph.order
    ).order_by(ResumeParagraph.order.desc()).first()
    if previous:
        paragraph.order, previous.order = previous.order, paragraph.order
        db.session.commit()
        with force_locale(get_locale()):
            flash(_("Paragraph moved up"), "info")
    else:
        with force_locale(get_locale()):
            flash(_("Already at the top"), "warning")
    return redirect(url_for('admin.single_section_view', section_id=section.id))

# تحريك فقرة لأسفل
@admin_bp.route('/paragraph/move_down/<int:paragraph_id>', methods=['POST'])
def move_paragraph_down(paragraph_id):
    paragraph = ResumeParagraph.query.get_or_404(paragraph_id)
    section = paragraph.resume_section
    next_item = ResumeParagraph.query.filter(
        ResumeParagraph.resume_section_id == section.id,
        ResumeParagraph.order > paragraph.order
    ).order_by(ResumeParagraph.order.asc()).first()
    if next_item:
        paragraph.order, next_item.order = next_item.order, paragraph.order
        db.session.commit()
        with force_locale(get_locale()):
            flash(_("Paragraph moved down"), "info")
    else:
        with force_locale(get_locale()):
            flash(_("Already at the bottom"), "warning")
    return redirect(url_for('admin.single_section_view', section_id=section.id))


@admin_bp.route('/paragraph/<int:paragraph_id>/fields')
def manage_fields(paragraph_id):
    paragraph = ResumeParagraph.query.get_or_404(paragraph_id)
    fields = paragraph.fields  # إذا كانت العلاقة معرفة
    return render_template('admin/manage_fields.html.j2', paragraph=paragraph, fields=fields)
