from main import create_app
from main.extensions import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # التحقق من وجود العمود أولًا
        inspector = db.inspect(db.engine)
        columns = [col["name"] for col in inspector.get_columns("resume_paragraph")]
        if "location" not in columns:
            print("➕ إضافة العمود location ...")
            db.session.execute(text("ALTER TABLE resume_paragraph ADD COLUMN location VARCHAR(50) DEFAULT 'main';"))
            db.session.commit()
            print("✅ تم إضافة العمود location بنجاح.")
        else:
            print("ℹ️ العمود location موجود بالفعل.")

        # تحديث القيم NULL إلى "main"
        print("🔄 تحديث القيم التي لا تحتوي location...")
        db.session.execute(text("UPDATE resume_paragraph SET location = 'main' WHERE location IS NULL;"))
        db.session.commit()
        print("✅ تم تحديث الصفوف التي كانت تحتوي على NULL.")
    except Exception as e:
        print("❌ حدث خطأ:", e)
