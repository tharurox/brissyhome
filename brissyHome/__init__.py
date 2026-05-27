from flask import Flask, render_template
from flask_mysqldb import MySQL
import os

mysql = MySQL()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "IFN582ASSIGNMENT3"

    app.config["MYSQL_HOST"] = "localhost"
    app.config["MYSQL_USER"] = "root"
    app.config["MYSQL_PASSWORD"] = "root"
    app.config["MYSQL_DB"] = "brissyhome"
    app.config["MYSQL_CURSORCLASS"] = "DictCursor"

    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "img")

    mysql.init_app(app)

    # IMPORTANT: import views only after mysql is created and app is configured
    from .views import bp
    app.register_blueprint(bp)

    @app.errorhandler(404)
    def not_found(error):
        return render_template(
            "error.html",
            error_code=404,
            error_title="Page Not Found",
            error_message="The page you requested could not be found.",
        ), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template(
            "error.html",
            error_code=500,
            error_title="Server Error",
            error_message="Something went wrong on the server.",
        ), 500

    return app