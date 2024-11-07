from flask import Flask, render_template, jsonify, session

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")



if __name__ == "__main__":
    start_game()