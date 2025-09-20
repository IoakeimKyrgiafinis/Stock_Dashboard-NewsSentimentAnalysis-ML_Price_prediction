import os
from flask import Flask


def create_app():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    app = Flask(
        __name__,
        template_folder=os.path.join(project_root, "templates"),
        static_folder=os.path.join(project_root, "static")
    )

    from mywebapp.routes.dashboard_routes import dashboard_routes_bp
    from mywebapp.routes.home_routes import home_routes_bp
    from mywebapp.services.news import news_bp

    app.register_blueprint(dashboard_routes_bp)
    app.register_blueprint(home_routes_bp)
    app.register_blueprint(news_bp)
    return app

