class SQLGenerator:

    @staticmethod
    def generate(builder):

        if not builder.is_valid():
            raise ValueError(
                "QueryBuilder is not valid."
            )

        sql_parts = []

        # --------------------------------------------------
        # SELECT
        # --------------------------------------------------

        columns = builder.get_columns()

        if columns:
            select_clause = (
                "SELECT "
                + ", ".join(columns)
            )
        else:
            select_clause = "SELECT *"

        sql_parts.append(
            select_clause
        )

        # --------------------------------------------------
        # FROM
        # --------------------------------------------------

        sql_parts.append(
            f"FROM {builder.get_table()}"
        )

        # --------------------------------------------------
        # WHERE
        # --------------------------------------------------

        where_clause = (
            builder.build_where_clause()
        )

        if where_clause:
            sql_parts.append(
                where_clause
            )

        # --------------------------------------------------
        # ORDER BY
        # --------------------------------------------------

        order_clause = (
            builder.build_order_clause()
        )

        if order_clause:
            sql_parts.append(
                order_clause
            )

        # --------------------------------------------------
        # LIMIT
        # --------------------------------------------------

        limit_clause = (
            builder.build_limit_clause()
        )

        if limit_clause:
            sql_parts.append(
                limit_clause
            )

        # --------------------------------------------------
        # Final SQL
        # --------------------------------------------------

        return (
            "\n".join(sql_parts)
            + ";"
        )

    # ======================================================
    # Pretty Format
    # ======================================================

    @staticmethod
    def format_sql(sql):

        keywords = [
            "SELECT",
            "FROM",
            "WHERE",
            "ORDER BY",
            "GROUP BY",
            "HAVING",
            "LIMIT",
            "INNER JOIN",
            "LEFT JOIN",
            "RIGHT JOIN",
            "FULL JOIN"
        ]

        formatted = sql

        for keyword in keywords:

            formatted = formatted.replace(
                keyword,
                f"\n{keyword}"
            )

        return formatted.strip()

    # ======================================================
    # Generate SELECT *
    # ======================================================

    @staticmethod
    def generate_select_all(
        table_name
    ):

        return (
            f"SELECT *\n"
            f"FROM {table_name};"
        )

    # ======================================================
    # Generate Preview Query
    # ======================================================

    @staticmethod
    def generate_preview(
        builder,
        limit=100
    ):

        sql = SQLGenerator.generate(
            builder
        )

        sql = sql.rstrip(";")

        if "LIMIT" not in sql.upper():

            sql += (
                f"\nLIMIT {limit}"
            )

        return sql + ";"

    # ======================================================
    # Generate Count Query
    # ======================================================

    @staticmethod
    def generate_count(
        builder
    ):

        if not builder.is_valid():

            raise ValueError(
                "QueryBuilder is not valid."
            )

        sql_parts = []

        sql_parts.append(
            "SELECT COUNT(*)"
        )

        sql_parts.append(
            f"FROM {builder.get_table()}"
        )

        where_clause = (
            builder.build_where_clause()
        )

        if where_clause:

            sql_parts.append(
                where_clause
            )

        return (
            "\n".join(sql_parts)
            + ";"
        )