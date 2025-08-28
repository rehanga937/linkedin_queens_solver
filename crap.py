import tkinter as tk
from tkinter import colorchooser, simpledialog, filedialog, messagebox
import json

grid_buttons = []  # Keep references to buttons

def pick_color(button):
    color = colorchooser.askcolor()[1]  # Open color picker
    if color:
        button.config(bg=color)

def create_grid(rows=None, cols=None, colors=None):
    """Create a grid. If colors are provided, fill buttons with them."""
    global grid_buttons
    for widget in grid_frame.winfo_children():
        widget.destroy()  # Clear previous grid
    grid_buttons = []

    if rows is None or cols is None:
        rows = simpledialog.askinteger("Input", "Number of rows:", minvalue=1, maxvalue=20)
        cols = simpledialog.askinteger("Input", "Number of columns:", minvalue=1, maxvalue=20)

    for r in range(rows):
        row_buttons = []
        for c in range(cols):
            btn = tk.Button(grid_frame, width=4, height=2)
            btn.config(command=lambda b=btn: pick_color(b))
            btn.grid(row=r, column=c, padx=1, pady=1)
            # Set color if loading from file
            if colors:
                btn.config(bg=colors[r][c])
            row_buttons.append(btn)
        grid_buttons.append(row_buttons)

def save_grid():
    if not grid_buttons:
        messagebox.showerror("Error", "No grid to save!")
        return

    rows = len(grid_buttons)
    cols = len(grid_buttons[0])
    grid_data = [[btn.cget('bg') for btn in row] for row in grid_buttons]

    file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                             filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'w') as f:
            json.dump({"rows": rows, "cols": cols, "colors": grid_data}, f)
        messagebox.showinfo("Saved", f"Grid saved to {file_path}")

def load_grid():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if not file_path:
        return
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        create_grid(rows=data["rows"], cols=data["cols"], colors=data["colors"])
        messagebox.showinfo("Loaded", f"Grid loaded from {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load grid:\n{e}")

# Main window
root = tk.Tk()
root.title("Grid Color Picker")

tk.Button(root, text="Create Grid", command=create_grid).pack(pady=5)
tk.Button(root, text="Save Grid", command=save_grid).pack(pady=5)
tk.Button(root, text="Load Grid", command=load_grid).pack(pady=5)

grid_frame = tk.Frame(root)
grid_frame.pack(pady=10)

root.mainloop()
