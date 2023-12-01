import views
import os

from werkzeug.exceptions import HTTPException
from flask import Flask, jsonify
from flask_cors import CORS

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
    cors = CORS(app, resource={r"/*":{"origins":"*"}})
    app.config["CORS_HEADERS"] = "Content-Type"
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    app.run(debug=True)
