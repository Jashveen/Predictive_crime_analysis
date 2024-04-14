import sqlite3
import csv

# Connect to the SQLite database
conn = sqlite3.connect(r"C:\Users\Jash Progs\Datathon\Code\existing_database.db")
cursor = conn.cursor()

# Open the CSV file and read column names
with open(r"C:\Users\Jash Progs\Datathon\dataset\officialdataset\pcadata\FIR_Details_Data.csv", 'r', newline='', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile)
    column_names = csvreader.fieldnames

    # Create the fir_entry table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fir_entry ({})
    '''.format(', '.join([f'"{column_name}" TEXT' for column_name in column_names])))

    # Insert data into the database
    for row in csvreader:
        # Prepare the SQL query
        query = 'INSERT INTO fir_entry ({}) VALUES ({})'.format(
            ', '.join([f'"{column_name}"' for column_name in column_names]),
            ', '.join(['?'] * len(column_names))
        )

        # Extract values from the dictionary and insert into the database
        cursor.execute(query, list(row.values()))

# Commit changes and close the connection
conn.commit()
conn.close()
