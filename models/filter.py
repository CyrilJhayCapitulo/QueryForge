class Filter:

    VALID_OPERATORS = [
        "=",
        "!=",
        ">",
        "<",
        ">=",
        "<=",
        "Contains",
        "Starts With",
        "Ends With",
        "IN",
        "NOT IN",
        "IS NULL",
        "IS NOT NULL"
    ]

    def __init__(
        self,
        column,
        operator,
        value=None,
        logical_operator="AND"
    ):
        self.column = column
        self.operator = operator
        self.value = value
        self.logical_operator = logical_operator

    # ======================================================
    # Validation
    # ======================================================

    def is_valid(self):

        if not self.column:
            return False

        if self.operator not in self.VALID_OPERATORS:
            return False

        if self.operator not in [
            "IS NULL",
            "IS NOT NULL"
        ] and self.value in [None, ""]:
            return False

        return True

    # ======================================================
    # SQL Generation
    # ======================================================

    def to_sql(self):

        if not self.is_valid():
            return ""

        column = self.column
        value = self.value

        if self.operator == "=":
            return f"{column} = '{value}'"

        elif self.operator == "!=":
            return f"{column} != '{value}'"

        elif self.operator == ">":
            return f"{column} > '{value}'"

        elif self.operator == "<":
            return f"{column} < '{value}'"

        elif self.operator == ">=":
            return f"{column} >= '{value}'"

        elif self.operator == "<=":
            return f"{column} <= '{value}'"

        elif self.operator == "Contains":
            return f"{column} LIKE '%{value}%'"

        elif self.operator == "Starts With":
            return f"{column} LIKE '{value}%'"

        elif self.operator == "Ends With":
            return f"{column} LIKE '%{value}'"

        elif self.operator == "IN":

            items = [
                f"'{item.strip()}'"
                for item in str(value).split(",")
            ]

            return (
                f"{column} IN "
                f"({', '.join(items)})"
            )

        elif self.operator == "NOT IN":

            items = [
                f"'{item.strip()}'"
                for item in str(value).split(",")
            ]

            return (
                f"{column} NOT IN "
                f"({', '.join(items)})"
            )

        elif self.operator == "IS NULL":
            return f"{column} IS NULL"

        elif self.operator == "IS NOT NULL":
            return f"{column} IS NOT NULL"

        return ""

    # ======================================================
    # Serialization
    # ======================================================

    def to_dict(self):

        return {
            "column": self.column,
            "operator": self.operator,
            "value": self.value,
            "logical_operator": self.logical_operator
        }

    @classmethod
    def from_dict(cls, data):

        return cls(
            column=data.get("column"),
            operator=data.get("operator"),
            value=data.get("value"),
            logical_operator=data.get(
                "logical_operator",
                "AND"
            )
        )

    # ======================================================
    # String Representation
    # ======================================================

    def __str__(self):

        return self.to_sql()

    def __repr__(self):

        return self.__str__()