from pathlib import Path

from flask import Flask

import db

app = Flask(__name__)

app.config["DATABASE"] = str(
    Path(app.instance_path) / "registro.sqlite"
)

Path(app.instance_path).mkdir(parents=True, exist_ok=True)

db.init_app(app)


@app.get("/")
def index():
    return "<h1>REgistro</h1><p>Application setup is working.</p>"