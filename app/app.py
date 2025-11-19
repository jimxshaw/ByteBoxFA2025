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

@app.route("/customers/new", methods=["GET", "POST"])
def add_customer():
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        phone = request.form["phone"]
        email = request.form["email"]
        address = request.form["address"]

        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO customer (firstname, lastname, phone, email, address)
            VALUES (%s, %s, %s, %s, %s)
        """, (firstname, lastname, phone, email, address))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        return redirect(url_for("list_customers"))
    return render_template("customer_create.html")

@app.route("/customers/<int:id>/edit", methods=["GET", "POST"])
def edit_customer(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        phone = request.form["phone"]
        email = request.form["email"]
        address = request.form["address"]
        
        cursor.execute("""
            UPDATE customer
            SET firstname = %s, lastname = %s, phone = %s, email = %s, address = %s
            WHERE id = %s
        """, (firstname, lastname, phone, email, address, id))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        return redirect(url_for("list_customers"))
    
    cursor.execute("SELECT * FROM customer WHERE id = %s", (id,))
    customer = cursor.fetchone()

    cursor.close()
    conn.close()
    return render_template("customer_edit.html", customer=customer)

@app.route("/customers/<int:id>/delete", methods=["POST"])
def delete_customer(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM customer WHERE id = %s", (id,))
    
    conn.commit()
    
    cursor.close()
    conn.close()
    return redirect(url_for("list_customers"))

@app.route("/")
def home():
  return redirect(url_for("list_customer"))

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
