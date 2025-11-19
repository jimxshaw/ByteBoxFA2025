import psycopg2
from flask import Flask, request, redirect, render_template, url_for

app = Flask(__name__)

################
# DB CONNECTION
################
def get_db_connection():
  conn = psycopg2.connect(
    host="db", # Must match the service name in docker-compose.yml.
    database="bytebox",
    user="postgres",
    password="postgres"
  )
  return conn

##################
# CUSTOMER ROUTES
##################
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

######################
# STORAGE UNIT ROUTES
######################
@app.route("/storage_units")
def list_storage_units():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM StorageUnit ORDER BY ID;")
    
    units = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template("storage_units/index.html", units=units)

@app.route("/storage_units/new", methods=["GET", "POST"])
def create_storage_unit():
    if request.method == "POST":
        floor = request.form["floor"]
        climate_controlled = request.form.get("climate_controlled", "false").lower() == "true"
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO StorageUnit (Floor, ClimateControlled) VALUES (%s, %s);",
            (floor, climate_controlled),
        )
        
        conn.commit()
        
        cursor.close()
        conn.close()
        return redirect(url_for("list_storage_units"))
    return render_template("storage_units/create.html")

@app.route("/storage_units/<int:id>/delete", methods=["POST"])
def delete_storage_unit(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM StorageUnit WHERE ID = %s;", (id,))
    
    conn.commit()
    
    cursor.close()
    conn.close()
    return redirect(url_for("list_storage_units"))


#############
# HOME ROUTE
#############
@app.route("/")
def home():
  return redirect(url_for("list_customer"))

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
