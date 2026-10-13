import os
from pathlib import Path
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from services.resume_parser import extract_text
from services.matcher import analyze_resume, INTERNSHIPS

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-before-production")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = os.environ.get("UPLOAD_FOLDER", "uploads")
ALLOWED_EXTENSIONS = {"pdf", "txt", "docx"}

Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html", internships=INTERNSHIPS[:3])

@app.route("/analyze", methods=["POST"])
def analyze():
    uploaded = request.files.get("resume")
    target_role = request.form.get("target_role", "Any")
    if not uploaded or not uploaded.filename:
        flash("Choose a resume file before continuing.", "error")
        return redirect(url_for("index"))
    if not allowed_file(uploaded.filename):
        flash("Please upload a PDF, DOCX, or TXT file.", "error")
        return redirect(url_for("index"))
    filename = secure_filename(uploaded.filename)
    # Process in memory; the uploaded file is not retained on disk.
    try:
        resume_text = extract_text(uploaded, filename)
    except Exception as exc:
        app.logger.exception("Resume parsing failed")
        flash("We couldn't read that file. Try a text-based PDF, DOCX, or TXT file.", "error")
        return redirect(url_for("index"))
    if len(resume_text.strip()) < 30:
        flash("Very little text was found. Try a text-based PDF or DOCX resume.", "error")
        return redirect(url_for("index"))
    results = analyze_resume(resume_text, target_role)
    return render_template("results.html", results=results, filename=filename)

@app.route("/health")
def health():
    return {"status": "ok"}

@app.errorhandler(413)
def too_large(_error):
    flash("File too large. Maximum upload size is 5 MB.", "error")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
