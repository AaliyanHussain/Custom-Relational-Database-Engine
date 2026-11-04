import json
import os

class Table:
    def __init__(self, name, columns, types=None, primary_key=None):
        self.name = name
        self.columns = columns
        self.types = types if types is not None else {col: str for col in columns}
        self.primary_key = primary_key
        self.rows = []
        self._primary_key_values = set()

    def insert(self, values):
        if len(values) != len(self.columns):
            raise ValueError(f"Error: Table '{self.name}' expects {len(self.columns)} columns, but got {len(values)}.")
        row_dict = {}
        for col, val in zip(self.columns, values):
            expected_type = self.types.get(col)
            if not isinstance(val, expected_type):
                raise TypeError(f"Type error in column '{col}': expected {expected_type.__name__}, got {type(val).__name__}")
            row_dict[col] = val

        if self.primary_key:
            pk_val = row_dict[self.primary_key]
            if pk_val in self._primary_key_values:
                raise ValueError(f"Constraint error: Primary key '{pk_val}' already exists in table '{self.name}'.")
            self._primary_key_values.add(pk_val)
        self.rows.append(values)
        print(f"Inserted row into {self.name}: {values}")

    def select(self, column_name=None, value=None):
        if column_name is None and value is None:
            return self.rows
        if column_name is None or value is None:
            raise ValueError("Error: Both column_name and value must be provided for filtering.")
        if column_name not in self.columns:
            raise ValueError(f"Column '{column_name}' does not exist in table '{self.name}'.")

        col_index = self.columns.index(column_name)
        return [row for row in self.rows if row[col_index] == value]

    def select_where(self, column_name, operator, value):
        if column_name not in self.columns:
            raise ValueError(f"Column '{column_name}' does not exist in table '{self.name}'.")

        col_index = self.columns.index(column_name)
        matched_rows = []

        for row in self.rows:
            cell_value = row[col_index]
            match = False

            if operator == "==":
                match = (cell_value == value)
            elif operator == "!=":
                match = (cell_value != value)
            elif operator == ">":
                match = (cell_value > value)
            elif operator == "<":
                match = (cell_value < value)
            elif operator == ">=":
                match = (cell_value >= value)
            elif operator == "<=":
                match = (cell_value <= value)
            else:
                raise ValueError(f"Unsupported operator '{operator}'. Supported operators are: '==', '!=', '<', '<=', '>', '>='.")
            if match:
                matched_rows.append(row)
        return matched_rows  

    def update(self, primary_key_val, column_name, new_value):
        if not self.primary_key:
            raise ValueError(f"Table '{self.name}' has no primary key defined.")
        if column_name not in self.columns:
            raise ValueError(f"Column '{column_name}' dies not exist in table '{self.name}'.")
        expected_type = self.types.get(column_name)
        if expected_type and not isinstance(new_value, expected_type):
            raise TypeError(f"Type error in column '{column_name}': expected {expected_type.__name__}, got {type(new_value).__name__}")

        pk_index = self.columns.index(self.primary_key)
        col_index = self.columns.index(column_name)

        updated = False
        for row in self.rows:
            if row[pk_index] == primary_key_val:
                row[col_index] = new_value
                updated = True
                break

        if not updated:
            raise KeyError(f"Row with primary key '{primary_key_val}' not found in table '{self.name}'.")
        print(f"Updated table '{self.name}': Primary Key {primary_key_val} -> set {column_name} = {new_value}")

    def delete(self, primary_key_val):
        if not self.primary_key:
            raise ValueError(f"Table '{self.name}' has no primary key defined.")

        pk_index = self.columns.index(self.primary_key)
        row_to_delete = None

        for row in self.rows:
            if row[pk_index] == primary_key_val:
                row_to_delete = row
                break

        if row_to_delete is None:
            raise KeyError(f"Row with primary key '{primary_key_val}' not found in table '{self.name}'.")

        self.rows.remove(row_to_delete) 
        self._primary_key_values.remove(primary_key_val)
        print(f"Deleted row with primary key '{primary_key_val}' from table '{self.name}'.")

class Database:
    def __init__(self, name):
        self.name = name
        self.tables = {}

    def create_table(self, name, columns, types=None, primary_key=None):
        table = Table(name, columns, types, primary_key)
        self.tables[name] = table
        return table

    def get_table(self, name):
        if name not in self.tables:
            raise KeyError(f"Table '{name}' does not exist in database '{self.name}'.")
        return self.tables[name]

    def inner_join(self, table1_name, table2_name, on_col1, on_col2):
        t1 = self.get_table(table1_name)
        t2 = self.get_table(table2_name)

        if on_col1 not in t1.columns or on_col2 not in t2.columns:
             raise ValueError("Join columns do not match table schemas.")

        idx1 = t1.columns.index(on_col1)
        idx2 = t2.columns.index(on_col2)

        joined_results = []
        combined_columns = t1.columns + [c for c in t2.columns if c != on_col2]

        for r1 in t1.rows:
            for r2 in t2.rows:
                if r1[idx1] == r2[idx2]:
    # Merge rows, excluding the join column from the second table
                    merged_row = r1 + [val for i, val in enumerate(r2) if i != idx2]
                    joined_results.append(merged_row)

        return combined_columns, joined_results      

    def save_to_disk(self, filename="database.json"):
        data = {}
        for table_name, table in self.tables.items(): 
        #convert type of objects to their string name
            seralized_types = {col: t.__name__ for col, t in table.types.items()}

            data[table_name] = {
                "name": table.name,
                "columns": table.columns,
                "types": seralized_types,
                "primary_key": table.primary_key,
                "rows": table.rows,
                "primary_key_values": list(table.primary_key_values)
            }

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Database successfully saved to '{filename}'.")   

    def load_from_disk(self, filename="database.json"):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File '{filename}'.")

        type_map = {"int": int, "str": str, "float": float, "bool": bool}
        with open(filename, "r") as f:
            data = json.load(f)

        self.tables = {}
        for table_name, t_data in data.items():
            #Converts string names back to actual type objects
            deserialized_types = {col: type_map[t_name] for col, t_name in t_data["types"].items()}

            table = Table(
                name=t_data["name"],
                columns=t_data["columns"],
                types=deserialized_types,
                primary_key=t_data["primary_key"]
            )
            table.rows = t_data["rows"]
            table.primary_key_values = set(t_data["primary_key_values"])

            self.tables[table_name] = table
        print(f"Database successfully loaded from '{filename}'.")    
        