"""
Initialize the admin Blueprint and register admin route modules.
"""

from flask import Blueprint

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

from . import admin_routes, admin_builder_routes, admin_field, admin_paragraph
