import customtkinter as ctk
from tkinter import messagebox

from ui.toolbar import Toolbar
from ui.table_panel import TablePanel
from ui.filter_panel import FilterPanel
from ui.sql_preview_panel import SQLPreviewPanel
from ui.results_panel import ResultsPanel

from database.db_connection import DBConnection
from database.schema_loader import SchemaLoader
from database.query_executor import QueryExecutor

from query.query_builder import QueryBuilder
from query.sql_generator import SQLGenerator

from exports.excel_export import ExcelExporter


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ==================================================
        # Window
        # ==================================================

        self.title("QueryForge")
        self.geometry("1600x900")
        self.minsize(1200, 700)

        # ==================================================
        # Backend Objects
        # ==================================================

        self.db = DBConnection()

        self.schema_loader = None
        self.query_executor = None

        self.query_builder = QueryBuilder()

        self.excel_exporter = ExcelExporter()

        self.current_table = None

        # ==================================================
        # Layout
        # ==================================================

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=2)

        # ==================================================
        # Header
        # ==================================================

        self.header = ctk.CTkFrame(self)

        self.header.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=10
        )

        self.header.grid_columnconfigure(0, weight=1)

        self.lbl_title = ctk.CTkLabel(
            self.header,
            text="⚒ QueryForge",
            font=("Segoe UI", 24, "bold")
        )

        self.lbl_title.grid(
            row=0,
            column=0,
            padx=15,
            pady=10,
            sticky="w"
        )

        # ==================================================
        # Left Panel
        # ==================================================

        self.table_panel = TablePanel(
            self,
            table_select_callback=self.on_table_selected
        )

        self.table_panel.grid(
            row=1,
            column=0,
            rowspan=2,
            sticky="nsew",
            padx=(10, 5),
            pady=(0, 10)
        )

        # ==================================================
        # Right Panel
        # ==================================================

        self.content_frame = ctk.CTkFrame(self)

        self.content_frame.grid(
            row=1,
            column=1,
            rowspan=2,
            sticky="nsew",
            padx=(5, 10),
            pady=(0, 10)
        )

        self.content_frame.grid_columnconfigure(0, weight=1)

        # Toolbar
        self.content_frame.grid_rowconfigure(0, weight=0)

        # Filters
        self.content_frame.grid_rowconfigure(1, weight=0)

        # SQL Preview
        self.content_frame.grid_rowconfigure(2, weight=1)

        # Results
        self.content_frame.grid_rowconfigure(3, weight=8)
        # ==================================================
        # Toolbar
        # ==================================================

        self.toolbar = Toolbar(
            self.content_frame,
            connect_callback=self.connect_database,
            run_callback=self.run_query,
            export_callback=self.export_results,
            save_callback=self.save_project
        )

        self.toolbar.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=10
        )

        # ==================================================
        # Filter Panel
        # ==================================================

        self.filter_panel = FilterPanel(
            self.content_frame
        )

        self.filter_panel.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=10,
            pady=5
        )

        self.filter_panel.configure(height=100)

        # ==================================================
        # SQL Preview
        # ==================================================

        self.sql_preview_panel = SQLPreviewPanel(
            self.content_frame
        )

        self.sql_preview_panel.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=10,
            pady=5
        )

        # ==================================================
        # Results Panel
        # ==================================================

        self.results_panel = ResultsPanel(
            self.content_frame
        )

        self.results_panel.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=10,
            pady=5
        )

    # ======================================================
    # Connect Database
    # ======================================================

    def connect_database(self):

        try:

            db_path = self.db.browse_database()

            if not db_path:
                return

            success, message = self.db.connect()

            if not success:
                raise Exception(message)

            self.schema_loader = SchemaLoader(
                self.db.connection
            )

            self.query_executor = QueryExecutor(
                self.db.connection
            )

            tables = self.schema_loader.get_tables()

            self.table_panel.load_tables(
                tables
            )

            self.toolbar.set_status(
                "Database Connected"
            )

        except Exception as ex:

            messagebox.showerror(
                "Connection Error",
                str(ex)
            )

    # ======================================================
    # Table Selected
    # ======================================================

    def on_table_selected(self, table_name):

        try:

            print("=" * 50)
            print("TABLE SELECTED:", table_name)

            self.current_table = table_name

            columns = self.schema_loader.get_column_names(
                table_name
            )

            print("COLUMNS FOUND:", columns)

            self.table_panel.load_columns(
                columns
            )

            print("COLUMNS LOADED")

            self.filter_panel.set_columns(
                columns
            )

            self.generate_sql()

        except Exception as ex:

            print("ERROR:", ex)

            messagebox.showerror(
                "Table Error",
                str(ex)
            )

    # ======================================================
    # Generate SQL
    # ======================================================

    def generate_sql(self):

        if not self.current_table:
            return

        selected_columns = (
            self.table_panel.get_selected_columns()
        )

        # ------------------------------------------
        # SELECT
        # ------------------------------------------

        if selected_columns:

            select_clause = (
                "SELECT "
                + ", ".join(selected_columns)
            )

        else:

            select_clause = "SELECT *"

        # ------------------------------------------
        # FROM
        # ------------------------------------------

        sql = (
            f"{select_clause}\n"
            f"FROM {self.current_table}"
        )

        # ------------------------------------------
        # WHERE
        # ------------------------------------------

        where_clause = (
            self.filter_panel.build_where_clause()
        )

        if where_clause:

            sql += "\n" + where_clause

        sql += ";"

        self.sql_preview_panel.set_sql(sql)

    # ======================================================
    # Run Query
    # ======================================================

    def run_query(self):

        try:

            self.generate_sql()

            sql = self.sql_preview_panel.get_sql()

            if not sql.strip():

                self.generate_sql()

                sql = self.sql_preview_panel.get_sql()

            result = (
                self.query_executor.execute_safe(
                    sql
                )
            )

            if not result["success"]:

                raise Exception(
                    result["error"]
                )

            self.results_panel.load_data(
                result["headers"],
                result["rows"]
            )

            self.toolbar.set_status(
                f"{len(result['rows'])} rows returned"
            )

        except Exception as ex:

            messagebox.showerror(
                "Query Error",
                str(ex)
            )

    # ======================================================
    # Export Results
    # ======================================================

    def export_results(self):

        try:

            headers = self.results_panel.sheet.headers()

            rows = self.results_panel.sheet.get_sheet_data()

            self.excel_exporter.export_with_dialog(
                headers,
                rows
            )

        except Exception as ex:

            messagebox.showerror(
                "Export Error",
                str(ex)
            )

    # ======================================================
    # Save Project
    # ======================================================

    def save_project(self):

        messagebox.showinfo(
            "QueryForge",
            "Save Project feature coming soon."
        )
