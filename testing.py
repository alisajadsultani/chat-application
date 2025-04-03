import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="User_information",
        user="postgres",
        password="BossDaddy@123",
        port=3999
    )
    print("✅ Connected to DB")
except Exception as e:
    print("❌ Error:", e)
