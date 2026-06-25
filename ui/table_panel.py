import customtkinter as ctk


class TablePanel(ctk.CTkFrame):

    def __init__(self, master, table_select_callback=None, **kwargs):
        super().__init__(master, **kwargs)

        self.table_select_callback = table_select_callback
        self.column_checkboxes = {}
        self.table_buttons = {}

        # --------------------------------------------------
        # Layout
        # --------------------------------------------------

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # --------------------------------------------------
        # Title
        # --------------------------------------------------

        self.lbl_title = ctk.CTkLabel(
            self,
            text="DATABASE EXPLORER",
            font=("Segoe UI", 16, "bold")
        )

        self.lbl_title.grid(
            row=0,
            column=0,
            padx=10,
            pady=(10, 5),
            sticky="w"
        )

        # --------------------------------------------------
        # Tables Label
        # --------------------------------------------------

        self.lbl_tables = ctk.CTkLabel(
            self,
            text="Tables",
            font=("Segoe UI", 13)
        )

        self.lbl_tables.grid(
            row=1,
            column=0,
            padx=10,
            pady=(5, 0),
            sticky="w"
        )

        # --------------------------------------------------
        # Tables Frame
        # --------------------------------------------------

        self.tables_frame = ctk.CTkScrollableFrame(
            self,
            height=220
        )

        self.tables_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 10)
        )

        # --------------------------------------------------
        # Columns Label
        # --------------------------------------------------

        self.lbl_columns = ctk.CTkLabel(
            self,
            text="Columns",
            font=("Segoe UI", 13)
        )

        self.lbl_columns.grid(
            row=3,
            column=0,
            padx=10,
            pady=(0, 0),
            sticky="w"
        )

        # --------------------------------------------------
        # Columns Frame
        # --------------------------------------------------

        self.columns_frame = ctk.CTkScrollableFrame(
            self
        )

        self.columns_frame.grid(
            row=4,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(5, 10)
        )

    # ======================================================
    # Tables
    # ======================================================

    def load_tables(self, tables):

        for widget in self.tables_frame.winfo_children():
            widget.destroy()

        self.table_buttons.clear()

        for table in tables:

            btn = ctk.CTkButton(
                self.tables_frame,
                text=table,
                anchor="w",
                command=lambda t=table: self.on_table_click(t)
            )

            btn.pack(
                fill="x",
                padx=2,
                pady=2
            )

            self.table_buttons[table] = btn

    def on_table_click(self, table_name):

        self.highlight_table(table_name)

        if self.table_select_callback:
            self.table_select_callback(table_name)

    def highlight_table(self, selected_table):

        for table_name, button in self.table_buttons.items():

            if table_name == selected_table:

                button.configure(
                    fg_color=("gray70", "gray30")
                )

            else:

                button.configure(
                    fg_color="transparent"
                )
    # ======================================================
    # Columns
    # ======================================================

    def load_columns(self, columns):

        for widget in self.columns_frame.winfo_children():
            widget.destroy()

        self.column_checkboxes.clear()

        for column in columns:

            checkbox = ctk.CTkCheckBox(
                self.columns_frame,
                text=column
            )

            checkbox.pack(
                anchor="w",
                padx=5,
                pady=2
            )

            self.column_checkboxes[column] = checkbox

    def get_selected_columns(self):

        selected_columns = []

        for column_name, checkbox in self.column_checkboxes.items():

            if checkbox.get() == 1:
                selected_columns.append(column_name)

        return selected_columns

    def select_all_columns(self):

        for checkbox in self.column_checkboxes.values():
            checkbox.select()

    def clear_column_selection(self):

        for checkbox in self.column_checkboxes.values():
            checkbox.deselect()

    # ======================================================
    # Clear
    # ======================================================

    def clear_columns(self):

        for widget in self.columns_frame.winfo_children():
            widget.destroy()

        self.column_checkboxes.clear()

    def clear_tables(self):

        for widget in self.tables_frame.winfo_children():
            widget.destroy()

        self.table_buttons.clear()

    def clear(self):

        self.clear_tables()
        self.clear_columns()