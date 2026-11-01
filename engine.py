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
