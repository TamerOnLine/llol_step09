from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from main.models.models import db, Section, Setting, ResumeSection, ResumeParagraph, ResumeField
from flask_babel import force_locale, gettext as _
from main.i18n_runtime import get_locale

from . import admin_bp


# View fields of a paragraph
@admin_bp.route('/paragraph/<int:paragraph_id>/fields')
def view_paragraph_fields(paragraph_id):
    paragraph = ResumeParagraph.query.get_or_404(paragraph_id)
    with force_locale(get_locale()):
        return render_template(
            'admin/paragraph_fields.html.j2',
            paragraph=paragraph,
            fields=paragraph.fields
        )


# Add a new field
@admin_bp.route('/field/add/<int:paragraph_id>', methods=['POST'])
def add_field(paragraph_id):
    paragraph = ResumeParagraph.query.get_or_404(paragraph_id)
    key = request.form.get('key')
    value = request.form.get('value')
    field_type = request.form.get('type', 'text')
    order = int(request.form.get('order', 0))
    is_visible = 'is_visible' in request.form

    field = ResumeField(
        resume_paragraph_id=paragraph.id,
        key=key,
        value=value,
        field_type=field_type,
        order=order,
        is_visible=is_visible
    )
    db.session.add(field)
    db.session.commit()
    with force_locale(get_locale()):
        flash(_("Field added successfully"), "success")
    return redirect(url_for('admin.view_paragraph_fields', paragraph_id=paragraph.id))


# Edit a field
@admin_bp.route('/field/edit/<int:field_id>', methods=['POST'])
def edit_field(field_id):
    field = ResumeField.query.get_or_404(field_id)
    field.key = request.form.get('key')
    field.value = request.form.get('value')
    field.field_type = request.form.get('type')
    field.order = int(request.form.get('order', 0))
    field.is_visible = 'is_visible' in request.form
    db.session.commit()
    with force_locale(get_locale()):
        flash(_("Field updated successfully"), "success")
    return redirect(url_for('admin.view_paragraph_fields', paragraph_id=field.resume_paragraph_id))


# Delete a field
@admin_bp.route('/field/delete/<int:field_id>', methods=['POST'])
def delete_field(field_id):
    field = ResumeField.query.get_or_404(field_id)
    paragraph_id = field.resume_paragraph_id
    db.session.delete(field)
    db.session.commit()
    with force_locale(get_locale()):
        flash(_("Field deleted"), "danger")
    return redirect(url_for('admin.view_paragraph_fields', paragraph_id=paragraph_id))


# Move a field up
@admin_bp.route('/field/move_up/<int:field_id>', methods=['POST'])
def move_field_up(field_id):
    field = ResumeField.query.get_or_404(field_id)
    paragraph = field.paragraph
    above = ResumeField.query.filter(
        ResumeField.resume_paragraph_id == paragraph.id,
        ResumeField.order < field.order
    ).order_by(ResumeField.order.desc()).first()

    if above:
        field.order, above.order = above.order, field.order
        db.session.commit()
        with force_locale(get_locale()):
            flash(_("Field moved up"), "info")
    else:
        with force_locale(get_locale()):
            flash(_("Already at the top"), "warning")
    return redirect(url_for('admin.view_paragraph_fields', paragraph_id=paragraph.id))


# Move a field down
@admin_bp.route('/field/move_down/<int:field_id>', methods=['POST'])
def move_field_down(field_id):
    field = ResumeField.query.get_or_404(field_id)
    paragraph = field.paragraph
    below = ResumeField.query.filter(
        ResumeField.resume_paragraph_id == paragraph.id,
        ResumeField.order > field.order
    ).order_by(ResumeField.order.asc()).first()

    if below:
        field.order, below.order = below.order, field.order
        db.session.commit()
        with force_locale(get_locale()):
            flash(_("Field moved down"), "info")
    else:
        with force_locale(get_locale()):
            flash(_("Already at the bottom"), "warning")
    return redirect(url_for('admin.view_paragraph_fields', paragraph_id=paragraph.id))


# Toggle field visibility
@admin_bp.route('/field/toggle_visibility/<int:field_id>', methods=['POST'])
def toggle_field_visibility(field_id):
    field = ResumeField.query.get_or_404(field_id)
    field.is_visible = not field.is_visible
    db.session.commit()
    with force_locale(get_locale()):
        if field.is_visible:
            flash(_("Field is now visible"), "success")
        else:
            flash(_("Field is now hidden"), "warning")
    return redirect(url_for('admin.view_paragraph_fields', paragraph_id=field.resume_paragraph_id))
