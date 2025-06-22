"""
Initialize the database and populate it with sample data.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from __init__ import create_app
from models.models import db, Section, Setting

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Insert initial data (section titles)
    sections = [
        "Profile", "Career Goal", "Preferred Areas",
        "Work Experience", "Qualifications", "Technical Skills",
        "Languages", "Projects", "Links", "Interests"
    ]

    for title in sections:
        db.session.add(Section(title=title, content=""))

    db.session.add(
        Setting(key="section_title_css", value="{'font-size': '18px', 'color': '#000'}")
    )
    db.session.commit()

    print("Database initialized and populated with sample data.")
