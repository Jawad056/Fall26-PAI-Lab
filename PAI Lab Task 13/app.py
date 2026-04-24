from flask import Flask, render_template, request
from resume_parser import analyze_resume
from PyPDF2 import PdfReader
import docx

app = Flask(__name__)

def extract_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        resume_text = ""

        if request.form.get("resume"):
            resume_text = request.form.get("resume")

        file = request.files.get("file")
        if file and file.filename != "":
            if file.filename.endswith(".pdf"):
                resume_text = extract_pdf(file)
            elif file.filename.endswith(".docx"):
                resume_text = extract_docx(file)

        if resume_text:
            result = analyze_resume(resume_text)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)