from flask import Flask
from flask import render_template


def create_app(test_config=None):
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("_form.html")

    return app


# Elastic BeanStalk works with "application"
application = create_app()

if __name__ == "__main__":
    application.run(debug=True)
