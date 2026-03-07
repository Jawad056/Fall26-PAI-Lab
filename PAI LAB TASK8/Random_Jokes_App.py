from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/joke')
def get_joke():
    url = "https://official-joke-api.appspot.com/random_joke"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return jsonify({
            "setup": data["setup"],
            "punchline": data["punchline"]
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Failed to fetch joke",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)