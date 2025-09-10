import sys
from typing import TextIO

import tkinter as tk


class STDOutHandler:
    """Class to handle stdout.

    This copies the stdout to the provided tk.Text widget.
    """

    text_widget: tk.Text
    """Reference to a tkinter text widget
    """

    actual_stdout: TextIO
    """Reference to the real stdout
    """

    def __init__(self, text_widget: tk.Text):
        self.text_widget = text_widget
        self.actual_stdout = sys.stdout

    # Method to stick to protocol
    def write(self, string: str):
        # Print to real terminal
        self.actual_stdout.write(string)

        # Copy to tkinter text widget
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)

    # Method to stick to protocol
    def flush(self):
        self.actual_stdout.flush()