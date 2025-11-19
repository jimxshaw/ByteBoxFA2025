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
# Read.
@app.route("/customers")
def list_customers():
  conn = get_db_connection()
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM customer")
  
  customers = cursor.fetchall()

  cursor.close()
  conn.close()
  return render_template("customer_list.html", customers=customers)

# Create.
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

# Update.
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
    
    # A python tuple with one item must have a trailing comma.
    cursor.execute("SELECT * FROM customer WHERE id = %s", (id,))
    customer = cursor.fetchone()

    cursor.close()
    conn.close()
    return render_template("customer_edit.html", customer=customer)

# Delete.
@app.route("/customers/<int:id>/delete", methods=["POST"])
def delete_customer(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # A python tuple with one item must have a trailing comma.
    cursor.execute("DELETE FROM customer WHERE id = %s", (id,))
    
    conn.commit()
    
    cursor.close()
    conn.close()
    return redirect(url_for("list_customers"))


######################
# STORAGE UNIT ROUTES
######################
# Read.
@app.route("/storage_units")
def list_storage_units():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM StorageUnit ORDER BY ID;")
    
    units = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template("storage_units/index.html", units=units)

# Create.
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

# Delete.
@app.route("/storage_units/<int:id>/delete", methods=["POST"])
def delete_storage_unit(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # A python tuple with one item must have a trailing comma.
    cursor.execute("DELETE FROM StorageUnit WHERE ID = %s;", (id,))
    
    conn.commit()
    
    cursor.close()
    conn.close()
    return redirect(url_for("list_storage_units"))


############################
# CLIMATE CONTROLLED ROUTES
############################
# Read.
@app.route("/climate_controls")
def list_climate_controls():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM ClimateControl ORDER BY ClimateControlled;")
    
    climate_controls = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template("climate_controls/index.html", climate_controls=climate_controls)

# Update.
@app.route("/climate_controls/<climate_controlled>/edit", methods=["GET", "POST"])
def edit_climate_control(climate_controlled):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == "POST":
        monthly_rate = request.form["monthly_rate"]
        
        cursor.execute(
            "UPDATE ClimateControl SET MonthlyRate = %s WHERE ClimateControlled = %s;",
            (monthly_rate, climate_controlled)
        )
        
        conn.commit()
        
        cursor.close()
        conn.close()
        return redirect(url_for("list_climate_controls"))
    
    # Fetch current values.
    cursor.execute(
        "SELECT * FROM ClimateControl WHERE ClimateControlled = %s;",
        (climate_controlled,)
    )
    
    control = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return render_template("climate_controls/edit.html", control=control)


#########################
# RENTAL CONTRACT ROUTES
#########################
# Read.
@app.route("/rental_contracts")
def list_rental_contracts():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT rc.*, c.Name, su.ID as UnitNumber
        FROM RentalContract rc
        JOIN Customer c ON rc.CustomerID = c.ID
        JOIN StorageUnit su ON rc.Unit_ID = su.ID
        ORDER BY rc.ID;
    """)
    
    contracts = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template("rental_contracts/index.html", contracts=contracts)

# Create.
@app.route("/rental_contracts/new", methods=["GET", "POST"])
def new_rental_contract():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == "POST":
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        monthly_rate = request.form["monthly_rate"]
        customer_id = request.form["customer_id"]
        unit_id = request.form["unit_id"]
        
        cursor.execute("""
            INSERT INTO RentalContract (StartDate, EndDate, MonthlyRate, CustomerID, Unit_ID)
            VALUES (%s, %s, %s, %s, %s);
        """, (start_date, end_date, monthly_rate, customer_id, unit_id))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        return redirect(url_for("list_rental_contracts"))
    
    # Get the customers and units for the form.
    cursor.execute("SELECT ID, Name FROM Customer;")
    
    customers = cursor.fetchall()
    
    cursor.execute("SELECT ID FROM StorageUnit;")
    
    units = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template("rental_contracts/new.html", customers=customers, units=units)

# Update.
@app.route("/rental_contracts/<int:id>/edit", methods=["GET", "POST"])
def edit_rental_contract(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == "POST":
        end_date = request.form["end_date"]
        monthly_rate = request.form["monthly_rate"]
        
        cursor.execute("""
            UPDATE RentalContract SET EndDate = %s, MonthlyRate = %s WHERE ID = %s;
        """, (end_date, monthly_rate, id))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        return redirect(url_for("list_rental_contracts"))
    
    # A python tuple with one item must have a trailing comma.
    cursor.execute("SELECT * FROM RentalContract WHERE ID = %s;", (id,))
    
    contract = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return render_template("rental_contracts/edit.html", contract=contract)

# Delete.
@app.route("/rental_contracts/<int:id>/delete", methods=["POST"])
def delete_rental_contract(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM RentalContract WHERE ID = %s;", (id,))
    
    conn.commit()
    
    cursor.close()
    conn.close()
    return redirect(url_for("list_rental_contracts"))


#################
# PAYMENT ROUTES
#################
# Read.
@app.route("/payments")
def list_payments():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.*, rc.ID as ContractID
        FROM Payment p
        JOIN RentalContract rc ON p.Contract_ID = rc.ID
        ORDER BY p.PaymentDate DESC;
    """)
    
    payments = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template("payments/index.html", payments=payments)

# Create.
@app.route("/payments/new", methods=["GET", "POST"])
def new_payment():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        payment_date = request.form["payment_date"]
        amount = request.form["amount"]
        method = request.form["method"]
        contract_id = request.form["contract_id"]

        cursor.execute("""
            INSERT INTO Payment (PaymentDate, Amount, Method, Contract_ID)
            VALUES (%s, %s, %s, %s);
        """, (payment_date, amount, method, contract_id))

        conn.commit()
        
        cursor.close()
        conn.close()
        return redirect(url_for("list_payments"))

    cursor.execute("SELECT ID FROM RentalContract;")
    
    contracts = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template("payments/new.html", contracts=contracts)   

# Update.
@app.route("/payments/<int:id>/edit", methods=["GET", "POST"])
def edit_payment(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        method = request.form["method"]

        cursor.execute("UPDATE Payment SET Method = %s WHERE ID = %s;", (method, id))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        return redirect(url_for("list_payments"))

    # A python tuple with one item must have a trailing comma.
    cursor.execute("SELECT * FROM Payment WHERE ID = %s;", (id,))
    
    payment = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return render_template("payments/edit.html", payment=payment)

# Delete.
@app.route("/payments/<int:id>/delete", methods=["POST"])
def delete_payment(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # A python tuple with one item must have a trailing comma.
    cursor.execute("DELETE FROM Payment WHERE ID = %s;", (id,))
    
    conn.commit()
    
    cursor.close()
    conn.close()
    return redirect(url_for("list_payments"))


#############
# HOME ROUTE
#############
@app.route("/")
def home():
  return redirect(url_for("list_customers"))

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
