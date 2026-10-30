from pathlib import Path
import secrets

from flask import Flask

import auth
import db
import admin_courses
import admin_sections

app = Flask(__name__)

instance_folder = Path(app.instance_path)
instance_folder.mkdir(parents=True, exist_ok=True)

app.config["DATABASE"] = str(instance_folder / "registro.sqlite")

secret_file = instance_folder / "secret_key"
if not secret_file.exists():
    secret_file.write_text(secrets.token_hex(32), encoding="utf-8")

app.config["SECRET_KEY"] = secret_file.read_text(encoding="utf-8").strip()
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

db.init_app(app)
app.register_blueprint(auth.bp)
app.register_blueprint(admin_courses.bp)
app.register_blueprint(admin_sections.bp)