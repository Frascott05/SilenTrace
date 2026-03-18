import os
from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)