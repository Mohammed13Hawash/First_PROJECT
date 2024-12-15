from flask import Flask, render_template, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

# إعداد قاعدة البيانات وإنشاء جدول المستخدمين إذا لم يكن موجودًا
def init_db():
    with sqlite3.connect("users.db") as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)
init_db()

# صفحة تسجيل الدخول والتسجيل (Frontend)
@app.route("/")
def index():
    return render_template("index.html")

# API لتسجيل حساب جديد
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    hashed_password = generate_password_hash(password)  # تشفير كلمة المرور
    try:
        with sqlite3.connect("users.db") as conn:
            conn.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
            conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400

# API لتسجيل الدخول
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    with sqlite3.connect("users.db") as conn:
        cursor = conn.execute("SELECT password FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row and check_password_hash(row[0], password):  # التحقق من كلمة المرور
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401

if __name__ == "__main__":
    app.run(debug=True)
