from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

def extract_emails(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        emails = re.findall(EMAIL_REGEX, text)
        unique_emails = list(set(emails))
        return unique_emails
    except Exception as e:
        return [f"Error: {str(e)}"]

@app.route("/", methods=["GET", "POST"])
def index():
    emails = []
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            emails = extract_emails(url)

    return render_template("index.html", emails=emails)

if __name__ == "__main__":
    app.run(debug=True)