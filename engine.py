class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns
        self.rows = []

    def insert(self, values):
        if len(values) != len(self.columns):
            raise ValueError(f"Error: Table '{self.name}' expects {len(self.columns)} columns, but got {len(values)}.")
        self.rows.append(values)
        print(f"Inserted row into {self.name}: {values}")