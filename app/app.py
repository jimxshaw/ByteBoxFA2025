import psycopg2
from flask import Flask

app = Flask(__name__)

def test_db_connection():
  try:
    conn = psycopg2.connect(
      host="db", # Must match the service name in docker-compose.yml.
      database="bytebox",
      user="postgres",
      password="postgres"
    )

    return "Succsessfully connected to PostgreSQL!"
  except Exception as ex:
    return f"Failed to connect: {ex}"
  

@app.route("/")
def home():
  return test_db_connection()

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
