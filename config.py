import os


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    ALLOWED_EXTENSIONS = {
        "csv",
        "xls",
        "xlsx",
    }

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "ml_preprocessing_studio_2026"
    )