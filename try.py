import pandas as pd
import pyodbc

# Read the CSV file
csv_file_path = r"C:\Users\Malaika\parsed_data.csv"
data = pd.read_csv(csv_file_path)

# Extract the required columns from the CSV file
columns_to_insert = [
    'numberOfBags',  # To be inserted into the 1st column of the DB table
    'varietyName',   # To be inserted into the 2nd column of the DB table
    'submitted',     # To be inserted into the 3rd column of the DB table
    'category',      # To be inserted into the 4th column of the DB table
    'cropName',      # To be inserted into the 5th column of the DB table
    'companyName',   # To be inserted into the 6th column of the DB table
    'printed',       # To be inserted into the 7th column of the DB table
    'seedLotNumber'  # To be inserted into the 8th column of the DB table
]

# Create a connection to the database
conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=192.168.1.4;"
    r"DATABASE=MirzaSewtech;"
    r"UID=SuperAdmin;"
    r"PWD=SuperAdmin;"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Define the insert query
insert_query = """
INSERT INTO Data(Quantity, Variety, Submitted, Category, Crop, Company, Printed, Lot)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

# Insert the data into the database table
for index, row in data.iterrows():
    values_to_insert = [
        row['numberOfBags'],
        row['varietyName'],
        row['submitted'],
        row['category'],
        row['cropName'],
        row['companyName'],
        row['printed'],
        row['seedLotNumber']
    ]
    cursor.execute(insert_query, values_to_insert)

# Commit the transaction and close the connection
conn.commit()
cursor.close()
conn.close()
