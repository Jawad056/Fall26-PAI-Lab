from flask import Flask, render_template, request

app = Flask(__name__)

def chatbot_response(user_input):
    user_input = user_input.lower()

    if "admission" in user_input:
        return "Admissions are open from June to August."
    elif "fee" in user_input:
        return "The fee structure depends on your program."
    elif "program" in user_input:
        return "We offer BS AI, CS, and Data Science programs."
    elif "deadline" in user_input:
        return "The last date for admission is 31 August."
    else:
        return "Sorry, I can only answer admission-related questions."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    user_text = request.form["msg"]
    return chatbot_response(user_text)

if __name__ == "__main__":
    app.run(debug=True)