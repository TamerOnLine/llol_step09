from flask import Flask
from main.extensions import db

from main.models.resume_section import ResumeSection
from main.models.resume_paragraph import ResumeParagraph
from main.models.resume_field import ResumeField
from main.models.resume_setting import Setting
from main.models.Section import Section
from main.models.LanguageOption import LanguageOption
from main.models.NavigationLink import NavigationLink

from .routes.admin import admin_bp
from .routes.main_routes import main_bp
from .routes.resume_templates import template_blueprints
from .extensions import babel
from .i18n_runtime import init_i18n, get_locale


import os
import logging

def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("main.config.settings.Config")
    app.config['LANGUAGES'] = ['de', 'en', 'ar']
    translations_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'translations'))
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = translations_path
    app.debug = True

    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    babel.init_app(app)
    babel.locale_selector_func = get_locale
    init_i18n(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    for bp in template_blueprints:
        app.register_blueprint(bp)

    with app.app_context():
        db_path = os.path.join(app.instance_path, 'lebenslauf.db')
        if not os.path.exists(db_path):
            db.create_all()
            insert_initial_sections()
            insert_initial_navigation()
            insert_initial_languages()
            insert_initial_settings()

    @app.before_request
    def log_locale_info():
        logging.debug("Requested locale: %s", get_locale())
        logging.debug("Babel directory: %s", app.config.get('BABEL_TRANSLATION_DIRECTORIES'))

    @app.context_processor
    def inject_globals():
        nav_links = NavigationLink.query.order_by(NavigationLink.order).all()
        langs = LanguageOption.query.order_by(LanguageOption.order).all()
        settings_list = Setting.query.all()
        settings_dict = {s.key: s.value for s in settings_list}
        return dict(nav_links=nav_links, langs=langs, settings=settings_list, settings_dict=settings_dict)

    return app

def insert_initial_sections():
    """
    Insert default resume sections into the database.
    """
    default_sections = [
        "Summary", "Career Objective", "Experience", "Qualifications",
        "Skills", "Languages", "Projects", "Links", "Interests"
    ]
    for idx, title in enumerate(default_sections, start=1):
        section = Section(order=idx, title=title, content="")
        db.session.add(section)
    db.session.commit()


def insert_initial_navigation():
    """
    Insert default navigation links into the database.
    """
    if NavigationLink.query.count() == 0:
        nav_items = [
            {"label": "Home", "icon": "", "endpoint": "main.index", "order": 0},
            {"label": "Sections", "icon": "", "endpoint": "admin.manage_sections", "order": 1},
            {"label": "Settings", "icon": "", "endpoint": "admin.manage_settings", "order": 2},
            {"label": "Builder", "icon": "", "endpoint": "admin.resume_builder", "order": 3}
        ]
        for item in nav_items:
            link = NavigationLink(**item)
            db.session.add(link)
        db.session.commit()


def insert_initial_languages():
    """
    Insert supported languages into the database.
    """
    if LanguageOption.query.count() == 0:
        langs = [
            {"code": "ar", "name": "Arabic", "order": 1},
            {"code": "en", "name": "English", "order": 2},
            {"code": "de", "name": "German", "order": 3}
        ]
        for lang in langs:
            db.session.add(LanguageOption(**lang))
        db.session.commit()


def insert_initial_settings():
    """
    Insert default styling and theme settings into the database.
    """
    if not Setting.query.filter_by(key="section_title_css").first():
        db.session.add(Setting(key="section_title_css", value='{"font-size": "20px", "color": "#000", "font-weight": "normal"}'))
    if not Setting.query.filter_by(key="paragraph_css").first():
        db.session.add(Setting(key="paragraph_css", value='{"font-size": "14px", "color": "#333"}'))
    if not Setting.query.filter_by(key="body_font").first():
        db.session.add(Setting(key="body_font", value="font-family: Arial, sans-serif;"))
    if not Setting.query.filter_by(key="theme_mode").first():
        db.session.add(Setting(key="theme_mode", value="light"))
    db.session.commit()
