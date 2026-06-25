import sqlite3


class SchemaLoader:

    def __init__(self, connection):

        self.connection = connection

    # ======================================================
    # Get All Tables
    # ======================================================

    def get_tables(self):

        query = """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """

        cursor = self.connection.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()

        return [row[0] for row in rows]

    # ======================================================
    # Get Columns
    # ======================================================

    def get_columns(self, table_name):

        query = f"PRAGMA table_info('{table_name}')"

        cursor = self.connection.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()

        columns = []

        for row in rows:

            columns.append({
                "cid": row[0],
                "name": row[1],
                "type": row[2],
                "notnull": row[3],
                "default": row[4],
                "pk": row[5]
            })

        return columns

    # ======================================================
    # Get Column Names Only
    # ======================================================

    def get_column_names(self, table_name):

        columns = self.get_columns(table_name)

        return [
            column["name"]
            for column in columns
        ]

    # ======================================================
    # Get Primary Keys
    # ======================================================

    def get_primary_keys(self, table_name):

        columns = self.get_columns(table_name)

        return [
            column["name"]
            for column in columns
            if column["pk"] == 1
        ]

    # ======================================================
    # Get Table Info
    # ======================================================

    def get_table_info(self, table_name):

        columns = self.get_columns(table_name)

        return {
            "table_name": table_name,
            "column_count": len(columns),
            "columns": columns,
            "primary_keys": self.get_primary_keys(
                table_name
            )
        }

    # ======================================================
    # Get Entire Schema
    # ======================================================

    def get_schema(self):

        schema = {}

        tables = self.get_tables()

        for table in tables:

            schema[table] = self.get_table_info(
                table
            )

        return schema

    # ======================================================
    # Detect Relationships
    # ======================================================

    def detect_relationships(self):

        """
        Simple heuristic:

        Customers.CustomerID
        Orders.CustomerID

        Detect possible joins.
        """

        relationships = []

        tables = self.get_tables()

        all_columns = {}

        for table in tables:

            all_columns[table] = self.get_column_names(
                table
            )

        for table1 in tables:

            for table2 in tables:

                if table1 == table2:
                    continue

                for col1 in all_columns[table1]:

                    if col1 in all_columns[table2]:

                        relationships.append({
                            "table1": table1,
                            "column1": col1,
                            "table2": table2,
                            "column2": col1
                        })

        return relationships

    # ======================================================
    # Get Row Count
    # ======================================================

    def get_row_count(self, table_name):

        query = f"""
        SELECT COUNT(*)
        FROM "{table_name}"
        """

        cursor = self.connection.cursor()

        cursor.execute(query)

        row_count = cursor.fetchone()[0]

        return row_count

    # ======================================================
    # Get Table Preview
    # ======================================================

    def get_preview_data(
        self,
        table_name,
        limit=100
    ):

        query = f"""
        SELECT *
        FROM "{table_name}"
        LIMIT {limit}
        """

        cursor = self.connection.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()

        headers = []

        if cursor.description:

            headers = [
                column[0]
                for column in cursor.description
            ]

        return headers, rows