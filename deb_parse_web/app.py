from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "Hello from Flask!"

    return app


# Elastic BeanStalk works with "application"
application = create_app()

if __name__ == "__main__":
    application.run(debug=True)
