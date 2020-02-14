import os

SECRET_KEY = os.environ.get("SECRET_KEY", default="dev")
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")
