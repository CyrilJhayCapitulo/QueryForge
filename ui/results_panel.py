import customtkinter as ctk
from tksheet import Sheet


class ResultsPanel(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --------------------------------------------------
        # Header
        # --------------------------------------------------
        self.lbl_title = ctk.CTkLabel(
            self,
            text="QUERY RESULTS",
            font=("Segoe UI", 16, "bold")
        )

        self.lbl_title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=10,
            pady=(10, 5)
        )

        # --------------------------------------------------
        # Sheet Container
        # --------------------------------------------------
        self.sheet_frame = ctk.CTkFrame(self)

        self.sheet_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 10)
        )

        # --------------------------------------------------
        # TKSheet
        # --------------------------------------------------
        self.sheet = Sheet(
            self.sheet_frame,
            show_x_scrollbar=True,
            show_y_scrollbar=True
        )

        self.sheet.enable_bindings(
            (
                "single_select",
                "row_select",
                "column_select",
                "arrowkeys",
                "right_click_popup_menu",
                "rc_select",
                "copy",
                "select_all",
                "column_width_resize",
                "double_click_column_resize",
                "row_height_resize",
            )
        )

        self.sheet.pack(
            fill="both",
            expand=True
        )

    # ======================================================
    # Display Query Results
    # ======================================================

    def load_data(self, headers, rows):
        """
        headers = list of column names
        rows = list of tuples/lists
        """

        self.sheet.headers(headers)
        self.sheet.set_sheet_data(rows)

    # ======================================================
    # Clear Results
    # ======================================================

    def clear(self):

        self.sheet.headers([])
        self.sheet.set_sheet_data([])

    # ======================================================
    # Get Selected Row
    # ======================================================

    def get_selected_row(self):

        selected = self.sheet.get_currently_selected()

        if not selected:
            return None

        row_index = selected.row

        try:
            return self.sheet.get_row_data(row_index)
        except Exception:
            return None

    # ======================================================
    # Append Row
    # ======================================================

    def append_row(self, row_data):

        current_data = self.sheet.get_sheet_data()

        current_data.append(row_data)

        self.sheet.set_sheet_data(current_data)

    # ======================================================
    # Update Status
    # ======================================================

    def load_dataframe_like(self, headers, rows):

        self.load_data(headers, rows)

        row_count = len(rows)
        col_count = len(headers)

        return f"{row_count} rows returned | {col_count} columns"