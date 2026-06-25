class QueryExecutor:

    def __init__(self, connection):

        self.connection = connection

    # ======================================================
    # Execute SELECT Query
    # ======================================================

    def execute(self, sql):

        cursor = self.connection.cursor()

        cursor.execute(sql)

        rows = cursor.fetchall()

        headers = []

        if cursor.description:

            headers = [
                column[0]
                for column in cursor.description
            ]

        return headers, rows

    # ======================================================
    # Execute Non-Select Query
    # ======================================================

    def execute_non_query(self, sql):

        cursor = self.connection.cursor()

        cursor.execute(sql)

        self.connection.commit()

        return cursor.rowcount

    # ======================================================
    # Execute With Parameters
    # ======================================================

    def execute_params(self, sql, params):

        cursor = self.connection.cursor()

        cursor.execute(sql, params)

        rows = cursor.fetchall()

        headers = []

        if cursor.description:

            headers = [
                column[0]
                for column in cursor.description
            ]

        return headers, rows

    # ======================================================
    # Validate SQL
    # ======================================================

    def validate_sql(self, sql):

        sql = sql.strip()

        if not sql:
            return False, "SQL is empty."

        return True, "Valid"

    # ======================================================
    # Get Query Preview
    # ======================================================

    def preview(self, sql, limit=100):

        sql = sql.strip().rstrip(";")

        preview_sql = f"""
        SELECT *
        FROM (
            {sql}
        )
        LIMIT {limit}
        """

        return self.execute(preview_sql)

    # ======================================================
    # Get Row Count
    # ======================================================

    def get_row_count(self, sql):

        sql = sql.strip().rstrip(";")

        count_sql = f"""
        SELECT COUNT(*)
        FROM (
            {sql}
        )
        """

        cursor = self.connection.cursor()

        cursor.execute(count_sql)

        return cursor.fetchone()[0]

    # ======================================================
    # Test Connection
    # ======================================================

    def test_connection(self):

        try:

            cursor = self.connection.cursor()

            cursor.execute(
                "SELECT 1"
            )

            return True

        except Exception:

            return False

    # ======================================================
    # Get First Row
    # ======================================================

    def get_first_row(self, sql):

        headers, rows = self.preview(
            sql,
            limit=1
        )

        if rows:
            return headers, rows[0]

        return headers, None

    # ======================================================
    # Execute Safely
    # ======================================================

    def execute_safe(self, sql):

        try:

            headers, rows = self.execute(sql)

            return {
                "success": True,
                "headers": headers,
                "rows": rows,
                "error": None
            }

        except Exception as ex:

            return {
                "success": False,
                "headers": [],
                "rows": [],
                "error": str(ex)
            }