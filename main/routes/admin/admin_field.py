from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_babel import force_locale, gettext as _

from main.models.resume_field import ResumeField
from main.models.resume_paragraph import ResumeParagraph
from main.i18n_runtime import get_locale
from main.extensions import db

from . import admin_bp


@admin_bp.route('/paragraph/<int:paragraph_id>/fields')
def view_paragraph_fields(paragraph_id):
    paragraph = ResumeParagraph.query.get_or_404(paragraph_id)
    with force_locale(get_locale()):
        return render_template(
            'admin/paragraph_fields.html.j2',
            paragraph=paragraph,
            fields=paragraph.fields
        )


@admin_bp.route('/paragraph/<int:paragraph_id>/fields/add', methods=['POST'])
def add_field(paragraph_id):
    paragraph = ResumeParagraph.query.get_or_404(paragraph_id)
    
    field_type = request.form.get('field_type', 'text')
    order = request.form.get('order', 0)
    label = request.form.get('label', '').strip()
    value = request.form.get('value', '').strip()
    description = request.form.get('description', '').strip()
    is_visible = 'is_visible' in request.form

    try:
        order = int(order)
    except ValueError:
        order = 0

    new_field = ResumeField(
        resume_paragraph_id=paragraph.id,
        field_type=field_type,
        order=order,
        label=label or None,
        value=value or None,
        description=description or None,
        is_visible=is_visible
    )

    db.session.add(new_field)
    db.session.commit()
    flash(_("Field added successfully"), "success")
    return redirect(url_for('admin.manage_fields', paragraph_id=paragraph.id))



@admin_bp.route('/field/edit/<int:field_id>', methods=['POST'])
def edit_field(field_id):
    field = ResumeField.query.get_or_404(field_id)

    field.field_type = request.form.get('field_type', 'text')
    field.order = int(request.form.get('order', 0))
    field.is_visible = 'is_visible' in request.form
    field.label = request.form.get("label", "")
    field.value = request.form.get("value", "")
    field.description = request.form.get("description", "")

    db.session.commit()

    with force_locale(get_locale()):
        flash(_("Field updated successfully"), "success")

    return redirect(url_for('admin.view_paragraph_fields', paragraph_id=field.resume_paragraph_id))


@admin_bp.route('/field/delete/<int:field_id>', methods=['POST'])
def delete_field(field_id):
    field = ResumeField.query.get_or_404(field_id)
    paragraph_id = field.resume_paragraph_id

    db.session.delete(field)
    db.session.commit()

    with force_locale(get_locale()):
        flash(_("Field deleted"), "danger")

    return redirect(url_for('admin.view_paragraph_fields', paragraph_id=paragraph_id))


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
