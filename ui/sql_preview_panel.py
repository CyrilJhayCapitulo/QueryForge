import customtkinter as ctk


class SQLPreviewPanel(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --------------------------------------------------
        # Header
        # --------------------------------------------------

        self.header_frame = ctk.CTkFrame(self)

        self.header_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=(10, 5)
        )

        self.header_frame.grid_columnconfigure(0, weight=1)

        self.lbl_title = ctk.CTkLabel(
            self.header_frame,
            text="GENERATED SQL",
            font=("Segoe UI", 16, "bold")
        )

        self.lbl_title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=10,
            pady=5
        )

        self.btn_copy = ctk.CTkButton(
            self.header_frame,
            text="Copy",
            width=80,
            command=self.copy_sql
        )

        self.btn_copy.grid(
            row=0,
            column=1,
            padx=(5, 5),
            pady=5
        )

        self.btn_clear = ctk.CTkButton(
            self.header_frame,
            text="Clear",
            width=80,
            command=self.clear_sql
        )

        self.btn_clear.grid(
            row=0,
            column=2,
            padx=(0, 10),
            pady=5
        )

        # --------------------------------------------------
        # SQL Text Area
        # --------------------------------------------------

        self.sql_textbox = ctk.CTkTextbox(
            self,
            font=("Consolas", 13)
        )

        self.sql_textbox.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 5)
        )

        # --------------------------------------------------
        # Footer
        # --------------------------------------------------

        self.lbl_status = ctk.CTkLabel(
            self,
            text="Ready",
            anchor="w"
        )

        self.lbl_status.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=10,
            pady=(0, 10)
        )

    # ======================================================
    # SQL Methods
    # ======================================================

    def set_sql(self, sql_text):
        """
        Replace existing SQL.
        """

        self.sql_textbox.delete("1.0", "end")
        self.sql_textbox.insert("1.0", sql_text)

        self.set_status("SQL updated")

    def append_sql(self, sql_text):
        """
        Append SQL text.
        """

        self.sql_textbox.insert("end", sql_text)

    def get_sql(self):
        """
        Return current SQL.
        """

        return self.sql_textbox.get(
            "1.0",
            "end-1c"
        )

    def clear_sql(self):
        """
        Clear SQL textbox.
        """

        self.sql_textbox.delete(
            "1.0",
            "end"
        )

        self.set_status("SQL cleared")

    # ======================================================
    # Clipboard
    # ======================================================

    def copy_sql(self):

        sql_text = self.get_sql()

        if not sql_text.strip():
            self.set_status("No SQL to copy")
            return

        self.clipboard_clear()
        self.clipboard_append(sql_text)

        self.set_status("SQL copied to clipboard")

    # ======================================================
    # Status
    # ======================================================

    def set_status(self, message):

        self.lbl_status.configure(
            text=message
        )

    # ======================================================
    # Read Only Mode
    # ======================================================

    def set_readonly(self):

        self.sql_textbox.configure(
            state="disabled"
        )

    def set_editable(self):

        self.sql_textbox.configure(
            state="normal"
        )

    # ======================================================
    # Load Sample SQL
    # ======================================================

    def load_sample(self):

        sample_sql = """
SELECT
    CustomerID,
    Name,
    Email
FROM Customers
WHERE CustomerID > 100
ORDER BY Name ASC;
        """

        self.set_sql(sample_sql.strip())