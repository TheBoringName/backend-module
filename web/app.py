
import views
from werkzeug.exceptions import HTTPException

from flask import Flask, jsonify


def register_error_handlers(app):
    @app.errorhandler(code_or_exception=HTTPException)
    def handle_error(error):
        return jsonify(error.description), error.code


def register_blueprints(app):
    app.register_blueprint(blueprint=views.bp)


def create_app():
    app = Flask(import_name=__name__)
    register_error_handlers(app=app)
    register_blueprints(app=app)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
