from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import jwt
import datetime
import psycopg2
import bcrypt
import os
import secrets

#hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
# Save hashed_pw to DB, not the raw password

app = Flask(__name__)
CORS(app)
SECRET_KEY = secrets.token_hex(32)

load_dotenv()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    try:
        print("DB_HOST:", os.getenv("DB_HOST"))
        print("DB_USER:", os.getenv("DB_USER"))
        print("DB_NAME:", os.getenv("DB_NAME"))
        print("DB_PORT:", os.getenv("DB_PORT"))

        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dbname=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT")
        )

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            token = jwt.encode({
                "email": email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, SECRET_KEY, algorithm="HS256")
            return jsonify({"success": True, "token": token})
        else:
            return jsonify({"success": False, "message": "Invalid credentials"}), 401

    except Exception as e:
        print("DB error:", e)
        return jsonify({"success": False, "message": "Database connection error"}), 500



if __name__ == '__main__':
    app.run(debug=True)
