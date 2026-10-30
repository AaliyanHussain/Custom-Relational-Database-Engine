from engine import Table

users_table = Table("users", ["id", "name", "age"])

users_table.insert([1, "Aaliyan", 17])
users_table.insert([2, "Rehan", 15])

print("\n--- DATABASE STATE ---")
print(f"Table: {users_table.name}")
print(f"Columns: {users_table.columns}")
print(f"Rows: {users_table.rows}")