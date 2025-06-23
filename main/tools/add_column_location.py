from flask import Blueprint, render_template, request, redirect, url_for, flash
from main.extensions import db
from main.models import ResumeField, ResumeParagraph

bp = Blueprint('admin', __name__, url_prefix='/admin')  # أو استيراده كما في الخيار السابق

@bp.route('/field/add/<int:paragraph_id>', methods=['GET', 'POST'])
def add_field(paragraph_id):
    paragraph = ResumeParagraph.query.get_or_404(paragraph_id)

    if request.method == 'POST':
        try:
            field = ResumeField(
                resume_paragraph_id=paragraph_id,
                field_type=request.form.get('field_type', 'text'),
                order=int(request.form.get('order', 1)),
                is_visible=True,
                label_translations={
                    "en": request.form.get('label_en', ''),
                    "ar": request.form.get('label_ar', '')
                },
                value_translations={
                    "en": request.form.get('value_en', ''),
                    "ar": request.form.get('value_ar', '')
                }
            )
            db.session.add(field)
            db.session.commit()
            flash("تمت إضافة الحقل بنجاح ✅", "success")
            return redirect(url_for('admin.edit_paragraph', paragraph_id=paragraph_id))

        except Exception as e:
            db.session.rollback()
            flash(f"حدث خطأ أثناء الإضافة: {str(e)}", "danger")

    return render_template('admin/add_field.html', paragraph=paragraph)
