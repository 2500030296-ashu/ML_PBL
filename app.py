import os
import io
import base64
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from flask import Flask, render_template, request, session, redirect
from werkzeug.utils import secure_filename

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Required for session
app.secret_key = app.config.get("SECRET_KEY", "mysecretkey")

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        if "dataset" not in request.files:
            return render_template(
                "upload.html",
                error="Please select a file."
            )

        file = request.files["dataset"]

        if file.filename == "":
            return render_template(
                "upload.html",
                error="Please select a file."
            )

        extension = file.filename.rsplit(".", 1)[1].lower()

        if extension not in app.config["ALLOWED_EXTENSIONS"]:
            return render_template(
                "upload.html",
                error="Only CSV and Excel files are allowed."
            )

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(filepath)

        # Save filename in session
        session["dataset"] = filename

        # Read Dataset
        if extension == "csv":
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)

        rows = df.shape[0]
        columns = df.shape[1]

        column_names = df.columns.tolist()

        head_data = df.head(10).values.tolist()
        tail_data = df.tail(10).values.tolist()

        missing_values = df.isnull().sum().to_dict()

        buffer = io.StringIO()
        df.info(buf=buffer)
        info = buffer.getvalue()

        description = df.describe(include="all").to_html(
            classes="table table-bordered",
            border=1
        )

        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        categorical_cols = df.select_dtypes(exclude=np.number).columns.tolist()

        return render_template(
            "summary.html",
            filename=filename,
            rows=rows,
            columns=columns,
            column_names=column_names,
            head_data=head_data,
            tail_data=tail_data,
            missing_values=missing_values,
            info=info,
            description=description,
            numeric_cols=numeric_cols,
            categorical_cols=categorical_cols
        )

    return render_template("upload.html")


@app.route("/visualization")
def visualization():

    filename = session.get("dataset")

    if filename is None:
        return redirect("/upload")

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    df = pd.read_csv(filepath)

    # BAR GRAPH
    plt.figure(figsize=(8,5))
    df["branch"].value_counts().plot(kind="bar")
    plt.title("Students by Branch")
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format="png")
    plt.close()
    img.seek(0)

    bar_graph = base64.b64encode(img.getvalue()).decode()

    # HISTOGRAM
    plt.figure(figsize=(8,5))
    plt.hist(df["age"], bins=10, edgecolor="black")
    plt.title("Age Distribution")
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format="png")
    plt.close()
    img.seek(0)

    hist_graph = base64.b64encode(img.getvalue()).decode()

    return render_template(
        "visualization.html",
        bar_graph=bar_graph,
        hist_graph=hist_graph
    )


if __name__ == "__main__":
    app.run(debug=True)