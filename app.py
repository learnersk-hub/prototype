from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/api/register/teacher", methods=["POST"])
def register_teacher():
    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"message": "All fields are required!"}), 400

    if Teacher.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered!"}), 409

    hashed_password = generate_password_hash(password)
    new_teacher = Teacher(name=name, email=email, password=hashed_password)
    db.session.add(new_teacher)
    db.session.commit()

    return jsonify({"message": "Registration successful!"}), 201

# Serve register.html directly
@app.route("/")
def serve_register():
    return send_from_directory(os.getcwd(), "register.html")

if __name__ == "_main_":
    app.run(debug=True)