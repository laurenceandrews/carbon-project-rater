from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, I'm a Carbon Project Rater!"

if __name__ == '__main__':
    app.run(debug=True)