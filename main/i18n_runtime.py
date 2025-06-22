from flask import session, request
from flask_babel import gettext
from .extensions import babel

def get_locale():
    """
    Determine the preferred locale for the current user.

    Returns:
        str: Selected language code (e.g., 'de', 'en', 'ar').
    """
    # 1. If language is passed in the URL parameters
    if "lang" in request.args:
        lang = request.args.get("lang")
        if lang in ['de', 'en', 'ar']:
            session['lang'] = lang  # Store language in session
            return lang

    # 2. If a language has already been selected and stored in session
    if "lang" in session:
        return session['lang']

    # 3. Fallback to the best match from browser settings
    return request.accept_languages.best_match(['de', 'en', 'ar'])

def init_i18n(app):
    """
    Initialize internationalization (i18n) for the Flask app.

    Args:
        app (Flask): The Flask application instance.
    """
    babel.locale_selector_func = get_locale

    @app.context_processor
    def inject_get_locale():
        return dict(get_locale=get_locale)

    @app.context_processor
    def inject_translation():
        return dict(_=gettext)
