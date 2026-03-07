from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>Random Joke App</h1>
    <p>Go to <a href="/joke">/joke</a> to get a random joke.</p>
    """

@app.route('/joke')
def get_joke():
    url = "https://official-joke-api.appspot.com/random_joke"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return f"""
        <h2>Random Joke</h2>
        <p><b>Question:</b> {data['setup']}</p>
        <p><b>Answer:</b> {data['punchline']}</p>
        """

    except requests.exceptions.RequestException as e:
        return f"<h3>Error: {str(e)}</h3>"

if __name__ == '__main__':
    app.run(debug=True)