import sys
import json

import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox

from src.queens_board import Board, Cell, CellStatus
from src.solving_logic import SolvingLogic
from src.copy_std import STDOutHandler, STDErrHandler


class GUI:

    gui_cells: list[tk.Label] = []
    """Holds references to the gui cells. Keep this in grid order (like reading a book from left to right, top to bottom)

    (So that cells can be accessed easily via this convention: gui_cell = self.__gui_cells[x + self.__grid_size * y])
    """

    chosen_color = "white" # initial color
    """Variable to hold the currently chosen color from the color picker.
    """

    grid_size: int = 0
    board: Board

    def __init__(self, root: tk.Tk):

        # Widget structure
        # It is intended for the mainframe to have 4 horizontal sections
        # Top section is for the grid config controls
        # Next section is the cell grid - i.e. the queens board
        # 3rd section has the solving buttons
        # 4th section holds a print terminal
        
        root.title("LinkedIn Queens Solver")

        # so if the window is resized by the user, somehow this makes everything stay in the middle. Still not familiar with how this works.
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        # mainframe
        mainframe = ttk.Frame(root)
        mainframe.grid(
            row=0, column=0,
            # sticky=tk.EW # no clue how this works
        )

        ## grid configuration frame
        grid_configs = ttk.Frame(mainframe)
        grid_configs.grid(row=0, padx=10, pady=10) # this padding seems to be the interior padding for the entire grid_configs frame

        ### first row of grid config frame (grid size input)
        grid_size_input_label = ttk.Label(grid_configs, text="Grid Size")
        grid_size_input_label.grid(row=0, column=0)
        self.grid_size_input = ttk.Entry(grid_configs)
        self.grid_size_input.grid(row=0, column=1)

        ### third row of grid config frame (color picker)
        color_picker_label = ttk.Label(grid_configs, text="Pick Color")
        color_picker_label.grid(row=2, column=0, sticky="e")

        self.color_picker_button = tk.Button(
            grid_configs, 
            command=self.pick_color,
            height=2,
            width=4,
            bg=self.chosen_color # set the initial color
        )
        self.color_picker_button.grid(row=2, column=1, sticky="w")

        ## (queens cell grid)
        self.cell_grid = ttk.Frame(mainframe)
        self.cell_grid.grid(row=1, padx=10, pady=10)

        ### second row of grid config frame (grid command buttons)
        create_grid_button = ttk.Button(grid_configs, command=self.create_new_grid, text="Create Grid / Reset")
        create_grid_button.grid(row=1, column=0)
        save_grid_button = ttk.Button(grid_configs, command=self.save_grid_2_json_file, text="Save Grid")
        save_grid_button.grid(row=1, column=1)
        load_grid_button = ttk.Button(grid_configs, command=self.load_new_grid, text="Load Grid")
        load_grid_button.grid(row=1, column=2)

        ## solving controls frame
        solving_controls = ttk.Frame(mainframe)
        solving_controls.grid(row=2, padx=10, pady=10)

        ### solving controls frame first row
        mark_queens_button = ttk.Button(solving_controls, text="Mark Queens", command=self.mark_queens)
        axiom1_button = ttk.Button(solving_controls, text="Axiom 1", command=self.axiom_1)
        axiom2_button = ttk.Button(solving_controls, text="Axiom 2", command=self.axiom_2)
        auto_solve_button = ttk.Button(solving_controls, text="Auto Solve", command=self.auto_solve)
        mark_queens_button.grid(row=0, column=0)
        axiom1_button.grid(row=0,column=1)
        axiom2_button.grid(row=0,column=2)
        auto_solve_button.grid(row=0,column=3) 

        ### solving controls frame 2nd row
        times_to_think_ahead_label = tk.Label(solving_controls, text="Axiom 1 - no. of moves to think ahead")
        times_to_think_ahead_label.grid(row=1, column=0, columnspan=2)
        self.think_ahead = ttk.Entry(solving_controls)
        self.think_ahead.grid(row=1, column=2)
        self.think_ahead.insert(tk.END, '1') # default value

        ## terminal
        terminal = tk.Text(mainframe, wrap="word", bg="black", fg="white", insertbackground="white", height=12)
        terminal.grid(row=3, padx=10, pady=10)
        # text.pack(expand=True, fill="both")
        sys.stdout = STDOutHandler(terminal) # tell sys.stdout that our STDOutHandler object is the new stdout
        sys.stderr = STDErrHandler(terminal) # tell sys.stderr that our STDErrHandler object is the new stderr

        # padding
        for child in grid_configs.winfo_children():
            child.grid_configure(padx=5, pady=2)
        for child in solving_controls.winfo_children():
            child.grid_configure(padx=5, pady=2)


    def pick_color(self):
        """This will change the self.__chosen_color variable and update the color picker button.
        """
        self.chosen_color = colorchooser.askcolor(initialcolor=self.chosen_color)[1] # [1] to choose the hex code. For example the entire returned tuple might look like this: ((255, 0, 0), '#ff0000')
        self.color_picker_button.config(bg=self.chosen_color) # update the color of the button 





    def change_cell_color(self, event: tk.Event):
        """Change a cell color to the current self.chosen_color

        Args:
            event (tk.Event): This tk.Event should correspond to a gui cell.
        """
        cell: tk.Label = event.widget
        cell.config(bg=self.chosen_color)

    def create_new_grid(self):
        """Function to create a cell grid (the queens board) in the GUI with whatever grid size the user has entered
        """
        # validation
        try: 
            new_grid_size = int(self.grid_size_input.get())
            if new_grid_size < 1 or new_grid_size > 20: return
        except ValueError: return

        self.grid_size = new_grid_size
        
        self.__create_new_grid(new_grid_size)

    def __create_new_grid(self, grid_size: int, colors: list[list[str]] = None):
        """Creates a new grid in the GUI.

        Args:
            grid_size (int): _description_
            colors (list[list[str]], optional): Colors of the cells. List of list - book reading order - i.e. left to right, top to bottom. 
                Defaults to None. If none, all cells will be initialized with white. Colors are tkinter compatible string values: e.g.: "blue", "#FF0000", etc.
        """
        # reset cells
        for cell in self.gui_cells: cell.destroy()
        self.gui_cells = []

        for row_number in range(0, grid_size):
            for col_number in range(0, grid_size):
                color = "white"
                if colors: color = colors[row_number][col_number]
                cell = tk.Label(
                    self.cell_grid, 
                    fg="black", bg=color, # i guess fg affects the border color
                    # text="t", 
                    borderwidth=2, relief="solid", # solid border
                    # padx=2, pady=2, # this refers to the interior padding
                    height=2, width=4 # it seems to make a square, height should be half the width
                )
                cell.grid(
                    row=row_number, column=col_number, 
                    padx=2, pady=2 # this refers to the external padding. i.e. the spacing between individual cells
                )
                cell.bind("<Button-3>", func=self.change_cell_color) # on right-click, change cell color
                self.gui_cells.append(cell)

    def load_new_grid(self):
        """Load a grid from a json file.

        Asks user for location of json file. Reads the json file and creates a new grid with the size and colors provided in the json file.
        """
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path: return

        with open(file_path, "rt") as f:
            grid_json_dict = json.load(f)

        rows = grid_json_dict['rows']
        cols = grid_json_dict['cols']
        if rows != cols:
            messagebox.showinfo("Invalid grid size", "Grid is not a square!")
            return
        grid_size = rows
        if grid_size < 1 or grid_size > 20: 
            messagebox.showinfo("Invalid grid size", "Grid size must be between 1 and 20")
            return
        
        colors = grid_json_dict['colors']
        # validate colors size
        if len(colors) != grid_size:
            messagebox.showinfo("Invalid JSON", "Colors array does not match grid size")
            return
        for row in colors:
            if len(row) != grid_size:
                messagebox.showinfo("Invalid JSON", "Colors array does not match grid size")
                return
        
        self.grid_size = grid_size
        self.__create_new_grid(grid_size, colors)


    def grid_colors_2_json_dict(self) -> dict:
        """Saves the information about the grid to a dictionary. Considers only the blank board - i.e. crosses and queens locations are not saved.
        """
        grid_size = self.grid_size
        
        colors: list[list[str]] = []
        for y in range(0, grid_size):
            colors_in_this_row: list[str] = []
            for x in range(0, grid_size):
                gui_cell = self.gui_cells[x + self.grid_size * y]
                color_str = gui_cell.cget("bg")
                colors_in_this_row.append(color_str)
            colors.append(colors_in_this_row)

        output = {
            "rows": grid_size,
            "cols": grid_size,
            "colors": colors
        }
        return output


    def save_grid_2_json_file(self):
        """Function to save the grid (colors only - i.e. a blank board with the colors) to a json file.

        Uses a filedialog.
        Example json:
        ```
        {
            "rows": 2,
            "cols": 2,
            "colors": [
                [
                    "blue",
                    "#ff0000"
                ],
                [
                    "#ff0000",
                    "white"
                ]
            ]
        }
        ```
        """
        # get the dict representation that can be saved to a json
        dict_repr = self.grid_colors_2_json_dict()

        # ask the user for the filepath
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                             filetypes=[("JSON files", "*.json")])
        if not file_path: return

        # save the dict to a json at the filepath
        with open(file_path, "wt") as f:
            json.dump(dict_repr, f, indent=4)
        messagebox.showinfo("Saved", f"Grid saved to {file_path}")

    
    def __update_gui_to_board(self):
        # first create Cells
        cells: list[Cell] = []
        for gui_cell in self.gui_cells:
            grid_information = gui_cell.grid_info()
            column_index = grid_information['column']
            row_index = grid_information['row']
            color_str = gui_cell.cget("bg")
            text = gui_cell.cget("text")
            if text == None: text = ""
            cell_status = CellStatus.get_status_for(text)
            cell = Cell(x=column_index, y=row_index, color=color_str, status=cell_status)
            cells.append(cell)

        # then create Board
        self.board = Board(self.grid_size, self.grid_size, cells)
        

    def __update_board_to_gui(self):
        for y, row in enumerate(self.board.cell_grid):
            for x, cell in enumerate(row):
                gui_cell = self.gui_cells[x + self.grid_size * y]
                gui_cell.config(text=cell.status.value, bg=cell.color)

    def mark_queens(self):
        """For the button command.
        """
        self.__update_gui_to_board()
        SolvingLogic.mark_queens_where_certain(self.board)
        self.__update_board_to_gui()

    def axiom_1(self):
        """For the button command.
        """
        self.__update_gui_to_board()
        try: 
            times_to_think_ahead = int(self.think_ahead.get())
            if times_to_think_ahead < 1 or times_to_think_ahead > 20: 
                times_to_think_ahead = 1
                self.think_ahead.insert(tk.END, '1') # default value
        except ValueError: 
            times_to_think_ahead = 1
            self.think_ahead.insert(tk.END, '1') # default value
        SolvingLogic.axiom_1_should_not_block_color_sets(self.board, times_to_think_ahead)
        self.__update_board_to_gui()

    def axiom_2(self):
        """For the button command.
        """
        self.__update_gui_to_board()
        SolvingLogic.axiom_2_color_common_holdings(self.board)
        self.__update_board_to_gui()

    def auto_solve(self):
        """For the button command.
        """
        self.__update_gui_to_board()
        SolvingLogic.auto_solve(self.board)
        self.__update_board_to_gui()