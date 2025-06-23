from .resume_templates import template01_routes

def register_resume_templates_routes(app):
    app.register_blueprint(template01_routes.template01_bp)
