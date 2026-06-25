class Table:

    def __init__(
        self,
        name,
        columns=None,
        primary_keys=None
    ):
        self.name = name
        self.columns = columns or []
        self.primary_keys = primary_keys or []

    # ======================================================
    # Column Methods
    # ======================================================

    def add_column(self, column):

        self.columns.append(column)

    def remove_column(self, column_name):

        self.columns = [
            column
            for column in self.columns
            if column.name != column_name
        ]

    def get_column(self, column_name):

        for column in self.columns:

            if column.name == column_name:
                return column

        return None

    # ======================================================
    # Primary Key Methods
    # ======================================================

    def add_primary_key(self, column_name):

        if column_name not in self.primary_keys:
            self.primary_keys.append(column_name)

    # ======================================================
    # Information
    # ======================================================

    @property
    def column_count(self):

        return len(self.columns)

    # ======================================================
    # Serialization
    # ======================================================

    def to_dict(self):

        return {
            "name": self.name,
            "columns": [
                column.to_dict()
                for column in self.columns
            ],
            "primary_keys": self.primary_keys
        }

    # ======================================================
    # String Representation
    # ======================================================

    def __str__(self):

        return f"Table({self.name})"

    def __repr__(self):

        return self.__str__()