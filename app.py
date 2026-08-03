from flask import Flask, render_template, request, redirect, url_for, session
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":

        if "dataset" not in request.files:
            return render_template("upload.html", error="Please upload a dataset.")

        file = request.files["dataset"]

        if file.filename == "":
            return render_template("upload.html", error="No file selected.")

        filename = secure_filename(file.filename)

        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        return redirect(url_for("summary"))

    return render_template("upload.html")


@app.route("/summary")
def summary():
    return render_template("summary.html")


if __name__ == "__main__":
    app.run(debug=True)