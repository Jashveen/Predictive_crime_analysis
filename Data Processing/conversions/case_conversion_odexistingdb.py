import sqlite3

def change_column_casing(database_path, table_name):
    # Connect to the database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Get the existing column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns_info = cursor.fetchall()

    # Generate SQL statements to rename columns with different casings
    sql_statements = []
    for column_info in columns_info:
        old_column_name = column_info[1]
        new_column_name = old_column_name.lower()  # Change casing to lowercase
        if new_column_name != old_column_name:
            sql_statement = f"ALTER TABLE {table_name} RENAME COLUMN '{old_column_name}' TO '{new_column_name}';"
            sql_statements.append(sql_statement)

    # Execute SQL statements
    for sql_statement in sql_statements:
        cursor.execute(sql_statement)

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Example usage
database_path = r"C:\Users\Jash Progs\Datathon\Code\existing_database.db"
table_name = "fir_entry"
change_column_casing(database_path, table_name)
