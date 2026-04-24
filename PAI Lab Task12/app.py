from flask import Flask, request, jsonify, render_template
import pandas as pd
import re
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# -------------------------
# LOAD MODEL + FAISS
# -------------------------
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
index = faiss.read_index("admission.index")

# ⚠️ IMPORTANT: recreate dataset inside Flask (same as notebook)
data = {
    "Question": [
        "What are the admission requirements?",
        "When does admission open?",
        "Is entry test required?",
        "How can I apply?",
        "What documents are needed?",
        "Is hostel available?",
        "What is fee structure?",
        "Do you offer scholarships?"
    ],
    "Answer": [
        "Students need FSC/A-level with minimum 60% marks.",
        "Admissions open in August every year.",
        "Yes, entry test is required for most programs.",
        "You can apply online through university portal.",
        "CNIC, photos, and academic certificates are required.",
        "Yes, separate hostels are available for boys and girls.",
        "Fee varies from 30,000 to 120,000 per semester.",
        "Yes, merit and need-based scholarships are available."
    ]
}

df = pd.DataFrame(data)

# -------------------------
# CLEAN TEXT
# -------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

# -------------------------
# SEARCH FUNCTION
# -------------------------
def search(query, k=3):
    query = clean_text(query)
    q_vec = model.encode([query])

    distances, indices = index.search(np.array(q_vec), k)

    results = []
    for i in range(k):
        idx = indices[0][i]
        results.append({
            "question": df["Question"].iloc[idx],
            "answer": df["Answer"].iloc[idx]
        })
    return results

# -------------------------
# ROUTES
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]
    results = search(user_msg)
    return jsonify(results)

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)