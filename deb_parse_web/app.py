import os
from flask import Flask, render_template, flash, request, escape, redirect, url_for
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = set(["txt"])
UPLOAD_FOLDER = "deb_parse_web/uploads"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    @app.route("/", methods=["GET", "POST"])
    def form():
        if request.method == "POST":
            file = request.files.get("file")

            if file is None or file.filename == "":
                text = request.form.get("text-content")

                if text is None or text == "":
                    flash("No file or text provided for processing", "warning")
                    return redirect(request.url)
                else:
                    escape(text)
                    flash("Plain text input is being processed.", "success")
                    return redirect(url_for("packages"))

            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                flash("File successfully uploaded", "success")
                return redirect(url_for("packages"))
            else:
                flash("Only .txt file extensions allowed.", "danger")
                return redirect(request.url)

        return render_template("_form.html")

    @app.route("/packages")
    def packages():
        return render_template("_packages.html")

    return app


# Elastic BeanStalk works with "application"
application = create_app()

if __name__ == "__main__":
    application.run(debug=True)
