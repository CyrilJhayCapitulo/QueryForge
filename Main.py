import traceback
import customtkinter as ctk
from tkinter import messagebox

from ui.main_window import MainWindow


APP_NAME = "QueryForge"
APP_VERSION = "1.0.0"


def configure_application():
    """
    Configure global application settings.
    """

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")


def start_application():
    """
    Create and launch the main window.
    """

    app = MainWindow()

    app.mainloop()


def main():

    try:

        configure_application()

        start_application()

    except Exception as ex:

        error_message = (
            f"Application Error\n\n"
            f"{type(ex).__name__}: {str(ex)}\n\n"
            f"{traceback.format_exc()}"
        )

        messagebox.showerror(
            f"{APP_NAME} Error",
            error_message
        )


if __name__ == "__main__":
    main()