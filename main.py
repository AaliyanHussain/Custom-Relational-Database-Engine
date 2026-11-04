import os

from engine import Database, Table
# 1. Initialize the Database Container
db = Database("school_db")

# 2. Create Tables using the database manager
users = db.create_table(
    "users",
    ["id", "name", "age"],
    types={"id": int, "name": str, "age": int},
    primary_key="id"
)    

orders = db.create_table(
    "orders",
    ["order_id", "user_id", "item"],
    types={"order_id": int, "user_id": int, "item": str},
    primary_key="order_id"
)
# 3. Insert Rows
users.insert([1, "Aaliyan", 17])
users.insert([2, "Rehan", 15])
users.insert([3, "Ali", 20])

orders.insert([101, 1, "Graphics Tablet"])
orders.insert([102, 1, "Mechanical Keyboard"])
orders.insert([103, 2, "Python Programming Book"])

# 4. Test Single-Tablet Selection
print("\n--- QUERY RESULTS (Age = 17) ---")
seventeen_years_old = users.select("age", 17)
print(seventeen_years_old)

# 5. Test Relational Join
print("\n--- INNER JOIN RESULTS (Users + Orders) ---")
columns, rows = db.inner_join("users", "orders", "id", "user_id")
print(columns)
for row in rows:
    print(row)

 # Test Advance Filtering with Operators   
print("\n--- ADVANCED FILTER RESULTS (Age >= 17) ---")
older_users = users.select_where("age", ">=", 17)
print(older_users)

# Test Update and Delete
print("\n--- Test Update and Delete ---")
users.update(2, "age", 16)
print("After update (ID 2):", users.select("id", 2))

users.delete(3)
print("Remaining users after deletion:", users.rows)

#Save database to diisk
db.save_to_disk("school.json")

# Test loadiing into a new database instance
new_db = Database("school_db")
new_db.load_from_disk("school.json")

print("\n--- Verifying Loaded Data ---")
print("Loaded users table rows:", new_db.get_table("users").rows)

def run_cli():
    db = Database("school_db")

    #Load your saved data into memory when CLI starts
    if os.path.exists("school.json"):
        db.load_from_disk("school.json")
        

    while True:
        print("\n=== COSTUM DATABASE ENGINE BY AALIYAN HUSSAIN ===")
        print("1. View Tables")
        print("2. View Table Rows")
        print("3. Create Table")
        print("4. Insert Row")
        print("5. Exit")

        choice = input("Choose an option (1, 2, 3, 4, or 5): ").strip()

        if choice == "1":
            print("Current tables in memory:", list(db.tables.keys()))

        elif choice == "2":
            t_name = input("Enter table name to view rows: ").strip() 
            try:
                table = db.get_table(t_name)
            except KeyError as e:
                print("Error:", e)
                continue

            print(f"\n--- {t_name.upper()} ROWS ---")
            print("Columns:", table.columns)
            for row in table.rows:
                print(row)

        elif choice == "3":
            t_name = input("Enter new table name: ").strip()
            cols_input = input("Enter column names (comma-seperated, e.g. id,name,age): ").strip()
            cols = [c.strip() for c in cols_input.split(",")]

            types_dict = {}
            for col in cols:
                t_type = input(f"Enter data type for '{col}' (int/str): ").strip().lower()
                types_dict[col] = int if t_type == "int" else str

            pk = input("Enter primary key column name: ").strip()
            if pk not in cols:
                print(f"Error: Primary key '{pk}' must be one of the table columns: {cols}")
                continue
            db.create_table(t_name, cols, types_dict, pk)
            print(f"Table '{t_name}' created successfully!")

        elif choice == "4":
            t_name = input("Table to insert intro: ").strip()
            try:
                table = db.get_table(t_name)
            except KeyError as e:
                print("Error:", e)
                continue

            row_data = []
            for col in table.columns:
                expected_type = table.types[col]
                while True:
                    val = input(f"Enter value for '{col}' ({table.types[col].__name__}): ").strip()
                    try:
                        if expected_type == int:
                            val = int(val)
                        break
                    except ValueError:
                        print(f"Error: '{val}' is not a valid integer. Try again.")
                row_data.append(val)

            try:
                table.insert(row_data)
                print("Row inserted successfully")
            except Exception as e:
                print("Insert Error:", e)

        elif choice == "5":
            print("Exiting engine.")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    run_cli()