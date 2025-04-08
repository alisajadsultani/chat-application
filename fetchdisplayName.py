from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import jwt
import datetime
import psycopg2
import bcrypt
import os
import secrets

@app.route('/api/display-name', methods=['POST'])
def get_display_name():
    data = request.json
    email = data.get("email")

    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dbname=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()
        cursor.execute("SELECT display_name FROM Users WHERE email = %s", (email,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return jsonify({"success": True, "display_name": result[0]})
        else:
            return jsonify({"success": False, "message": "User not found"}), 404

    except Exception as e:
        print("Error fetching display name:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
