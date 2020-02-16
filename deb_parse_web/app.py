import os
import json


from flask import (
    Flask,
    abort,
    render_template,
    send_file,
    flash,
    request,
    redirect,
    url_for,
)
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = set(["txt"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app(test_config=None):

    from .parse import parse_from, read, is_installed  # type: ignore

    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("_404.html"), 404

    @app.route("/", methods=["GET", "POST"])
    def form():
        if request.method == "POST":
            file = request.files.get("file")

            if file is None or file.filename == "":
                flash("No file provided.", "warning")
                return redirect(request.url)

            if allowed_file(file.filename):
                filepath = os.path.join(
                    app.config["UPLOAD_FOLDER"], secure_filename(file.filename)
                )

                file.save(filepath)
                recovery_id = parse_from(filepath)

                if recovery_id:
                    flash(f"Success. Your recovery id is: {recovery_id}", "success")
                    return redirect(url_for("packages", recovery_id=recovery_id))
                else:
                    flash("File doesn't match Debian Control File syntax", "danger")
                    return redirect(request.url)
            else:
                flash("Only .txt file extensions allowed.", "warning")
                return redirect(request.url)

        return render_template("_form.html")

    @app.route("/<recovery_id>/packages")
    def packages(recovery_id):
        json_path = os.path.join(
            "deb_parse_web", "datastore", recovery_id, "pkgs_clean.json"
        )
        with open(json_path) as jf:
            pkgs = json.load(jf)
        return render_template("_packages.html", pkgs=pkgs, recovery_id=recovery_id)

    @app.route("/<recovery_id>/packages/<pkg_name>")
    def package(recovery_id, pkg_name):
        json_path = os.path.join(
            "deb_parse_web", "datastore", recovery_id, "pkgs_clean.json"
        )
        with open(json_path) as jf:
            pkgs = json.load(jf)
        pkg = read(pkgs, pkg_name)

        if pkg:
            return render_template(
                "_package.html",
                pkg=pkg,
                recovery_id=recovery_id,
                is_installed=is_installed,
            )
        else:
            abort(404)

    @app.route("/<recovery_id>/api/packages/<json_type>")
    def api_packages(recovery_id, json_type):
        json_types = ["raw", "list", "clean"]
        if json_type not in json_types:
            flash(f"Only {json_types} are available.", "danger")
            abort(404)

        json_path = os.path.join("datastore", recovery_id, f"pkgs_{json_type}.json")
        return send_file(json_path)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
