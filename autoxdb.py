import sqlite3
from tabulate import tabulate  # Install with `pip install tabulate`

# Database setup
def initialize_db():
    conn = sqlite3.connect("autocross.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS autocross_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_name TEXT NOT NULL,
            car TEXT NOT NULL,
            class TEXT NOT NULL,
            run_number INTEGER NOT NULL,
            time REAL NOT NULL,
            penalties REAL DEFAULT 0,
            total_time REAL AS (time + penalties) STORED
        )
    """)
    conn.commit()
    conn.close()

# Insert new autocross result
def add_result():
    driver_name = input("Enter driver's name: ")
    car = input("Enter car (make and model): ")
    class_name = input("Enter class: ")
    run_number = int(input("Enter run number: "))
    time = float(input("Enter time (in seconds): "))
    penalties = float(input("Enter penalties (in seconds, default 0): ") or 0)
    
    conn = sqlite3.connect("autocross.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO autocross_results (driver_name, car, class, run_number, time, penalties)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (driver_name, car, class_name, run_number, time, penalties))
    conn.commit()
    conn.close()
    print("Result added successfully!")

# Query results
def query_results():
    conn = sqlite3.connect("autocross.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM autocross_results ORDER BY total_time ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Update result
def update_result():
    result_id = int(input("Enter the result ID to update: "))
    print("Leave fields blank to skip updating them.")
    time = input("Enter new time (in seconds): ")
    penalties = input("Enter new penalties (in seconds): ")
    
    conn = sqlite3.connect("autocross.db")
    cursor = conn.cursor()
    if time:
        cursor.execute("UPDATE autocross_results SET time = ? WHERE id = ?", (float(time), result_id))
    if penalties:
        cursor.execute("UPDATE autocross_results SET penalties = ? WHERE id = ?", (float(penalties), result_id))
    conn.commit()
    conn.close()
    print("Result updated successfully!")

# Delete a result
def delete_result():
    result_id = int(input("Enter the result ID to delete: "))
    conn = sqlite3.connect("autocross.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM autocross_results WHERE id = ?", (result_id,))
    conn.commit()
    conn.close()
    print("Result deleted successfully!")

# Display results
def display_results():
    results = query_results()
    if results:
        print(tabulate(results, headers=["ID", "Driver Name", "Car", "Class", "Run #", "Time", "Penalties", "Total Time"], tablefmt="grid"))
    else:
        print("No results found.")

# Main menu
def main():
    initialize_db()
    while True:
        print("\n--- Autocross Results Management ---")
        print("1. Add a new result")
        print("2. View all results")
        print("3. Update a result")
        print("4. Delete a result")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_result()
        elif choice == "2":
            display_results()
        elif choice == "3":
            update_result()
        elif choice == "4":
            delete_result()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
