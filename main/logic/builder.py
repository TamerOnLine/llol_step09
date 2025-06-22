import json
from ..models.models import Setting

def get_css_setting(key, default=""):
    """
    Retrieve and format CSS settings from the database.

    Args:
        key (str): The configuration key for the CSS setting.
        default (str): Default CSS string if the setting is not found or invalid.

    Returns:
        str: Formatted CSS string (e.g., "font-size: 14px; color: #000")
    """
    setting = Setting.query.filter_by(key=key).first()
    if setting:
        try:
            css_dict = json.loads(setting.value.replace("'", '"'))
            return "; ".join(f"{k}: {v}" for k, v in css_dict.items())
        except Exception:
            return default
    return default
