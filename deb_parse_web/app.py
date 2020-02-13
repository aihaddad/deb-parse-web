import os
from flask import Flask, render_template, send_file, flash, request, escape, redirect, url_for
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = set(["txt"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app(test_config=None):

    from parse import parse_from    # type: ignore

    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


    @app.route("/", methods=["GET", "POST"])
    def form():
        if request.method == "POST":
            file = request.files.get("file")

            if file is None or file.filename == "":
                flash("No file provided.", "warning")
                return redirect(request.url)

            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

                file.save(filepath)
                recovery_id = parse_from(filepath)

                if recovery_id:
                    flash(f"File successfully uploaded. Your recovery id is: {recovery_id}", "success")
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
        return send_file(f"datastore/{recovery_id}/pkgs_clean.json")

    return app


# Elastic BeanStalk works with "application"
application = create_app()

if __name__ == "__main__":
    application.run(debug=True)
