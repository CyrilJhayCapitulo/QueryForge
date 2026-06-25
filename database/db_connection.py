import sqlite3
from tkinter import filedialog


class DBConnection:

    def __init__(self):

        self.connection = None
        self.database_path = None

    # ======================================================
    # Browse SQLite Database
    # ======================================================

    def browse_database(self):

        file_path = filedialog.askopenfilename(
            title="Select SQLite Database",
            filetypes=[
                ("SQLite Database", "*.db *.sqlite *.sqlite3"),
                ("All Files", "*.*")
            ]
        )

        if file_path:
            self.database_path = file_path

        return file_path

    # ======================================================
    # Connect
    # ======================================================

    def connect(self, database_path=None):

        try:

            if database_path:
                self.database_path = database_path

            if not self.database_path:
                raise Exception("No database selected.")

            self.connection = sqlite3.connect(
                self.database_path
            )

            return True, "Connected successfully."

        except Exception as ex:

            return False, str(ex)

    # ======================================================
    # Disconnect
    # ======================================================

    def disconnect(self):

        try:

            if self.connection:
                self.connection.close()
                self.connection = None

            return True

        except Exception:

            return False

    # ======================================================
    # Get Cursor
    # ======================================================

    def get_cursor(self):

        if not self.connection:
            raise Exception(
                "Database is not connected."
            )

        return self.connection.cursor()

    # ======================================================
    # Execute Query
    # ======================================================

    def execute_query(self, sql):

        if not self.connection:
            raise Exception(
                "Database is not connected."
            )

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
    # Execute Non Query
    # ======================================================

    def execute_non_query(self, sql):

        if not self.connection:
            raise Exception(
                "Database is not connected."
            )

        cursor = self.connection.cursor()

        cursor.execute(sql)

        self.connection.commit()

    # ======================================================
    # Commit
    # ======================================================

    def commit(self):

        if self.connection:
            self.connection.commit()

    # ======================================================
    # Rollback
    # ======================================================

    def rollback(self):

        if self.connection:
            self.connection.rollback()

    # ======================================================
    # Is Connected
    # ======================================================

    def is_connected(self):

        return self.connection is not None

    # ======================================================
    # Get Database Path
    # ======================================================

    def get_database_path(self):

        return self.database_path