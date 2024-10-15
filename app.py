from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pyodbc
import traceback

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

server = '192.168.1.4'
database = 'MirzaSewtech'
username = 'SuperAdmin'
password = 'SuperAdmin'

connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if 'User' not in request.form or 'Password' not in request.form:
        flash('Missing username or password', 'error')
        return redirect(url_for('index'))

    username = request.form['User'].strip()
    password = request.form['Password'].strip()

    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        sql_query = "SELECT COUNT(*) FROM Login WHERE [User] = ? AND [Password] = ?"
        cursor.execute(sql_query, (username, password))
        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        if count > 0:
            return redirect(url_for('welcome'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('index'))
    except pyodbc.Error as e:
        traceback.print_exc()
        flash(f'Error connecting to database: {e}', 'error')
        return redirect(url_for('index'))

@app.route('/welcome')
def welcome():
    return render_template('Welcome.html')

@app.route('/dashboard-data')
def dashboard_data():
    category = request.args.get('category')
    company = request.args.get('company')

    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        query = """
            SELECT Quantity, Variety, Submitted, Category, Crop, Company, Lot
            FROM Data
        """
        params = []

        if category:
            query += " WHERE Category = ?"
            params.append(category)
        
        if company:
            if params:
                query += " AND Company = ?"
            else:
                query += " WHERE Company = ?"
            params.append(company)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        data_list = []
        for row in rows:
            data_dict = {
                'Quantity': row.Quantity,
                'Variety': row.Variety,
                'Submitted': row.Submitted,
                'Category': row.Category,
                'Crop': row.Crop,
                'Company': row.Company,
                'Lot': row.Lot,
            }
            data_list.append(data_dict)

        cursor.close()
        conn.close()

        return jsonify(data_list)
   
    except pyodbc.Error as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
@app.route('/search-printed')
def search_printed():
    lot_number = request.args.get('query')

    if not lot_number:
        return "No lot number provided", 400

    table_name = 'test'  # Assuming table name is 'test'
    column_name = 'LotNumber'  # Assuming column name is 'LotNumber'

    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Use parameterized query to prevent SQL injection
        sql_query = f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} = ?"
        cursor.execute(sql_query, (lot_number,))
        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        if count > 0:
            result = "Printed"
        else:
            result = "Not Printed"

        return  result
    
    except pyodbc.Error as e:
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/search-delivered')
def search_delivered():
    lot_number = request.args.get('query')

    if not lot_number:
         return "No lot number provided", 400

    table_name = 'Delivered'  # Assuming table name is 'Delivered'
    column_name = 'LotNumber'  # Assuming column name is 'LotNumber'

    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Use parameterized query to prevent SQL injection
        sql_query = f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} = ?"
        cursor.execute(sql_query, (lot_number,))
        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        if count > 0:
            result = "Delivered"
        else:
            result = "Not Delivered"

        return  result
    
    except pyodbc.Error as e:
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/companies')
def companies():
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute("SELECT DISTINCT Company FROM Data")
        rows = cursor.fetchall()

        companies = [row.Company for row in rows]

        cursor.close()
        conn.close()

        return jsonify(companies)

    except pyodbc.Error as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
