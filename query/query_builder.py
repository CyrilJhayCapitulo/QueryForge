from models.filter import Filter


class QueryBuilder:

    def __init__(self):

        self.reset()

    # ======================================================
    # Reset
    # ======================================================

    def reset(self):

        self.table_name = None

        self.selected_columns = []

        self.filters = []

        self.order_by = []

        self.limit = None

    # ======================================================
    # Table
    # ======================================================

    def set_table(self, table_name):

        self.table_name = table_name

    def get_table(self):

        return self.table_name

    # ======================================================
    # Columns
    # ======================================================

    def add_column(self, column_name):

        if column_name not in self.selected_columns:
            self.selected_columns.append(column_name)

    def remove_column(self, column_name):

        if column_name in self.selected_columns:
            self.selected_columns.remove(column_name)

    def clear_columns(self):

        self.selected_columns.clear()

    def get_columns(self):

        return self.selected_columns

    # ======================================================
    # Filters
    # ======================================================

    def add_filter(self, filter_obj):

        if isinstance(filter_obj, Filter):
            self.filters.append(filter_obj)

    def remove_filter(self, index):

        if 0 <= index < len(self.filters):
            self.filters.pop(index)

    def clear_filters(self):

        self.filters.clear()

    def get_filters(self):

        return self.filters

    # ======================================================
    # Order By
    # ======================================================

    def add_sort(
        self,
        column_name,
        direction="ASC"
    ):

        direction = direction.upper()

        if direction not in [
            "ASC",
            "DESC"
        ]:
            direction = "ASC"

        self.order_by.append(
            (
                column_name,
                direction
            )
        )

    def clear_sort(self):

        self.order_by.clear()

    def get_sort(self):

        return self.order_by

    # ======================================================
    # Limit
    # ======================================================

    def set_limit(self, limit):

        try:

            self.limit = int(limit)

        except Exception:

            self.limit = None

    def get_limit(self):

        return self.limit

    # ======================================================
    # Validation
    # ======================================================

    def is_valid(self):

        if not self.table_name:
            return False

        return True

    # ======================================================
    # Build WHERE Clause
    # ======================================================

    def build_where_clause(self):

        valid_filters = []

        for filter_obj in self.filters:

            sql = filter_obj.to_sql()

            if sql:
                valid_filters.append(sql)

        if not valid_filters:
            return ""

        return "WHERE " + " AND ".join(
            valid_filters
        )

    # ======================================================
    # Build ORDER BY Clause
    # ======================================================

    def build_order_clause(self):

        if not self.order_by:
            return ""

        clauses = []

        for column, direction in self.order_by:

            clauses.append(
                f"{column} {direction}"
            )

        return "ORDER BY " + ", ".join(
            clauses
        )

    # ======================================================
    # Build LIMIT Clause
    # ======================================================

    def build_limit_clause(self):

        if self.limit is None:
            return ""

        return f"LIMIT {self.limit}"

    # ======================================================
    # Summary
    # ======================================================

    def summary(self):

        return {
            "table": self.table_name,
            "columns": self.selected_columns,
            "filters": len(self.filters),
            "sorts": len(self.order_by),
            "limit": self.limit
        }

    # ======================================================
    # Serialization
    # ======================================================

    def to_dict(self):

        return {
            "table_name": self.table_name,
            "selected_columns": self.selected_columns,
            "filters": [
                filter_obj.to_dict()
                for filter_obj in self.filters
            ],
            "order_by": self.order_by,
            "limit": self.limit
        }

    @classmethod
    def from_dict(cls, data):

        builder = cls()

        builder.table_name = data.get(
            "table_name"
        )

        builder.selected_columns = data.get(
            "selected_columns",
            []
        )

        builder.order_by = data.get(
            "order_by",
            []
        )

        builder.limit = data.get(
            "limit"
        )

        for filter_data in data.get(
            "filters",
            []
        ):

            builder.filters.append(
                Filter.from_dict(
                    filter_data
                )
            )

        return builder