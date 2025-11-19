import psycopg2
from flask import Flask, request, redirect, render_template, url_for

app = Flask(__name__)

def get_db_connection():
  conn = psycopg2.connect(
    host="db", # Must match the service name in docker-compose.yml.
    database="bytebox",
    user="postgres",
    password="postgres"
  )
  return conn

@app.route("/customers")
def list_customers():
  conn = get_db_connection()
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM customer")
  
  customers = cursor.fetchall()

  cursor.close()
  conn.close()
  return render_template("customer_list.html", customers=customers)


@app.route("/")
def home():
  return redirect(url_for("list_customer"))

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
