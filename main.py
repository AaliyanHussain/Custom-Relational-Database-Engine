from engine import Database
# 1. Initialize the Database Container
db = Database("school_db")

# 2. Create Tables using the database manager
users = db.create_table(
    "users",
    ["id", "name", "age"],
    types={"id": int, "name": str, "age": int}
    primary_key="id"and
)    

orders = db.create_table(
    "orders",
    ["order_id", "user_id", "item"]
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
print("n\--- INNER JOIN RESULTS (Users + Orders) ---")
columns, rows = db.inner_join("users", "orders", "id", "user_id")
print(columns)
for row in rows:
    print(row)