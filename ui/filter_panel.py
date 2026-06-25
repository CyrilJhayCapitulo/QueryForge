import customtkinter as ctk


class FilterPanel(ctk.CTkFrame):

    OPERATORS = [
        "=",
        "!=",
        ">",
        "<",
        ">=",
        "<=",
        "Contains",
        "Starts With",
        "Ends With"
    ]

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.filters = []
        self.available_columns = []

        self.grid_columnconfigure(0, weight=1)

        # ==================================================
        # Header
        # ==================================================

        self.header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.header_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=(8, 4)
        )

        self.header_frame.grid_columnconfigure(
            3,
            weight=1
        )

        self.lbl_title = ctk.CTkLabel(
            self.header_frame,
            text="FILTERS",
            font=("Segoe UI", 16, "bold")
        )

        self.lbl_title.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.btn_add = ctk.CTkButton(
            self.header_frame,
            text="Add Filter",
            width=120,
            command=self.add_filter_row
        )

        self.btn_add.grid(
            row=0,
            column=1,
            padx=(20, 5)
        )

        self.btn_clear = ctk.CTkButton(
            self.header_frame,
            text="Clear",
            width=120,
            command=self.clear_filters
        )

        self.btn_clear.grid(
            row=0,
            column=2,
            padx=5
        )

        # ==================================================
        # Filters Area
        # ==================================================

        self.filters_frame = ctk.CTkScrollableFrame(
            self,
            height=75
        )

        self.filters_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=10,
            pady=(0, 5)
        )

    # ======================================================
    # Add Filter
    # ======================================================

    def add_filter_row(self):

        row_frame = ctk.CTkFrame(
            self.filters_frame
        )

        row_frame.pack(
            fill="x",
            padx=2,
            pady=2
        )

        column_values = (
            self.available_columns
            if self.available_columns
            else ["Select Column"]
        )

        column_combo = ctk.CTkComboBox(
            row_frame,
            values=column_values,
            width=180
        )

        if self.available_columns:
            column_combo.set(
                self.available_columns[0]
            )
        else:
            column_combo.set(
                "Select Column"
            )

        column_combo.pack(
            side="left",
            padx=5,
            pady=3
        )

        operator_combo = ctk.CTkComboBox(
            row_frame,
            values=self.OPERATORS,
            width=100
        )

        operator_combo.set("=")

        operator_combo.pack(
            side="left",
            padx=5,
            pady=3
        )

        value_entry = ctk.CTkEntry(
            row_frame,
            placeholder_text="Value"
        )

        value_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5,
            pady=3
        )

        filter_data = {}

        remove_btn = ctk.CTkButton(
            row_frame,
            text="✕",
            width=35,
            command=lambda:
                self.remove_filter_row(
                    row_frame,
                    filter_data
                )
        )

        remove_btn.pack(
            side="right",
            padx=5,
            pady=3
        )

        filter_data.update({
            "frame": row_frame,
            "column": column_combo,
            "operator": operator_combo,
            "value": value_entry
        })

        self.filters.append(
            filter_data
        )

    # ======================================================
    # Remove Filter
    # ======================================================

    def remove_filter_row(
        self,
        frame,
        filter_data
    ):

        frame.destroy()

        if filter_data in self.filters:
            self.filters.remove(
                filter_data
            )

    # ======================================================
    # Set Columns
    # ======================================================

    def set_columns(self, columns):

        self.available_columns = columns

        for filter_row in self.filters:

            filter_row["column"].configure(
                values=columns
            )

            if columns:
                filter_row["column"].set(
                    columns[0]
                )

    # ======================================================
    # Get Filters
    # ======================================================

    def get_filters(self):

        results = []

        for filter_row in self.filters:

            column = (
                filter_row["column"].get()
            )

            operator = (
                filter_row["operator"].get()
            )

            value = (
                filter_row["value"].get()
            )

            if (
                column
                and column != "Select Column"
                and value
            ):

                results.append({
                    "column": column,
                    "operator": operator,
                    "value": value
                })

        return results

    # ======================================================
    # Clear Filters
    # ======================================================

    def clear_filters(self):

        for filter_row in self.filters:

            filter_row["frame"].destroy()

        self.filters.clear()

    # ======================================================
    # Build WHERE Clause
    # ======================================================

    def build_where_clause(self):

        filters = self.get_filters()

        if not filters:
            return ""

        clauses = []

        for f in filters:

            col = f["column"]
            op = f["operator"]
            val = f["value"]

            if op == "Contains":

                clauses.append(
                    f"{col} LIKE '%{val}%'"
                )

            elif op == "Starts With":

                clauses.append(
                    f"{col} LIKE '{val}%'"
                )

            elif op == "Ends With":

                clauses.append(
                    f"{col} LIKE '%{val}'"
                )

            else:

                clauses.append(
                    f"{col} {op} '{val}'"
                )

        return (
            "WHERE "
            + " AND ".join(clauses)
        )
