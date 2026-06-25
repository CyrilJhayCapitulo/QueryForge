import customtkinter as ctk


class Toolbar(ctk.CTkFrame):

    def __init__(
        self,
        master,
        connect_callback=None,
        run_callback=None,
        export_callback=None,
        save_callback=None,
        **kwargs
    ):
        super().__init__(master, **kwargs)

        self.connect_callback = connect_callback
        self.run_callback = run_callback
        self.export_callback = export_callback
        self.save_callback = save_callback

        self.grid_columnconfigure(99, weight=1)

        # --------------------------------------------------
        # Connect Database
        # --------------------------------------------------

        self.btn_connect = ctk.CTkButton(
            self,
            text="Connect DB",
            width=130,
            command=self.on_connect
        )

        self.btn_connect.grid(
            row=0,
            column=0,
            padx=(10, 5),
            pady=10
        )

        # --------------------------------------------------
        # Run Query
        # --------------------------------------------------

        self.btn_run = ctk.CTkButton(
            self,
            text="Run Query",
            width=130,
            command=self.on_run
        )

        self.btn_run.grid(
            row=0,
            column=1,
            padx=5,
            pady=10
        )

        # --------------------------------------------------
        # Export Results
        # --------------------------------------------------

        self.btn_export = ctk.CTkButton(
            self,
            text="Export Excel",
            width=130,
            command=self.on_export
        )

        self.btn_export.grid(
            row=0,
            column=2,
            padx=5,
            pady=10
        )

        # --------------------------------------------------
        # Save Project
        # --------------------------------------------------

        self.btn_save = ctk.CTkButton(
            self,
            text="Save Project",
            width=130,
            command=self.on_save
        )

        self.btn_save.grid(
            row=0,
            column=3,
            padx=5,
            pady=10
        )

        # --------------------------------------------------
        # Status Label
        # --------------------------------------------------

        self.lbl_status = ctk.CTkLabel(
            self,
            text="Ready",
            anchor="e"
        )

        self.lbl_status.grid(
            row=0,
            column=99,
            sticky="e",
            padx=15
        )

    # ======================================================
    # Button Handlers
    # ======================================================

    def on_connect(self):
        if self.connect_callback:
            self.connect_callback()

    def on_run(self):
        if self.run_callback:
            self.run_callback()

    def on_export(self):
        if self.export_callback:
            self.export_callback()

    def on_save(self):
        if self.save_callback:
            self.save_callback()

    # ======================================================
    # Utility Methods
    # ======================================================

    def set_status(self, message):
        self.lbl_status.configure(text=message)

    def enable_all(self):

        self.btn_connect.configure(state="normal")
        self.btn_run.configure(state="normal")
        self.btn_export.configure(state="normal")
        self.btn_save.configure(state="normal")

    def disable_all(self):

        self.btn_connect.configure(state="disabled")
        self.btn_run.configure(state="disabled")
        self.btn_export.configure(state="disabled")
        self.btn_save.configure(state="disabled")

    def enable_query_actions(self):

        self.btn_run.configure(state="normal")
        self.btn_export.configure(state="normal")
        self.btn_save.configure(state="normal")

    def disable_query_actions(self):

        self.btn_run.configure(state="disabled")
        self.btn_export.configure(state="disabled")
        self.btn_save.configure(state="disabled")