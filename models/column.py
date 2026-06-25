class Column:

    def __init__(
        self,
        name,
        data_type="TEXT",
        nullable=True,
        primary_key=False,
        default_value=None
    ):
        self.name = name
        self.data_type = data_type
        self.nullable = nullable
        self.primary_key = primary_key
        self.default_value = default_value

    # ======================================================
    # Properties
    # ======================================================

    @property
    def is_numeric(self):

        numeric_types = [
            "INTEGER",
            "INT",
            "REAL",
            "FLOAT",
            "DOUBLE",
            "NUMERIC",
            "DECIMAL"
        ]

        return (
            self.data_type.upper()
            in numeric_types
        )

    @property
    def is_text(self):

        text_types = [
            "TEXT",
            "VARCHAR",
            "CHAR",
            "STRING"
        ]

        return (
            self.data_type.upper()
            in text_types
        )

    @property
    def is_date(self):

        date_types = [
            "DATE",
            "DATETIME",
            "TIMESTAMP"
        ]

        return (
            self.data_type.upper()
            in date_types
        )

    # ======================================================
    # Serialization
    # ======================================================

    def to_dict(self):

        return {
            "name": self.name,
            "data_type": self.data_type,
            "nullable": self.nullable,
            "primary_key": self.primary_key,
            "default_value": self.default_value
        }

    @classmethod
    def from_dict(cls, data):

        return cls(
            name=data.get("name"),
            data_type=data.get(
                "data_type",
                "TEXT"
            ),
            nullable=data.get(
                "nullable",
                True
            ),
            primary_key=data.get(
                "primary_key",
                False
            ),
            default_value=data.get(
                "default_value"
            )
        )

    # ======================================================
    # String Representation
    # ======================================================

    def __str__(self):

        pk = " PK" if self.primary_key else ""

        return (
            f"{self.name} "
            f"({self.data_type}){pk}"
        )

    def __repr__(self):

        return self.__str__()