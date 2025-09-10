import tkinter as tk
from tkinter import ttk, colorchooser

from src.queens_board import Board, Cell, CellStatus
from src.solving_logic import SolvingLogic


class GUI:

    __gui_cells: list[tk.Label] = []
    """Holds references to the gui cells. Keep this in grid order (like reading a book from left to right, top to bottom)

    (So that cells can be accessed easily via this convention: gui_cell = self.__gui_cells[x + self.__grid_size * y])
    """

    __chosen_color = "white" # initial color
    __grid_size: int = 0
    __board: Board

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
        self.__grid_size_input = ttk.Entry(grid_configs)
        self.__grid_size_input.grid(row=0, column=1)

        ### third row of grid config frame (color picker)
        color_picker_label = ttk.Label(grid_configs, text="Pick Color")
        color_picker_label.grid(row=2, column=0, sticky="e")

        self.__color_picker_button = tk.Button(
            grid_configs, 
            command=self.__pick_color,
            height=2,
            width=4,
            bg=self.__chosen_color # set the initial color
        )
        self.__color_picker_button.grid(row=2, column=1, sticky="w")

        ## (queens cell grid)
        self.__cell_grid = ttk.Frame(mainframe)
        self.__cell_grid.grid(row=1, padx=10, pady=10)

        ### second row of grid config frame (create grid button)
        create_grid_button = ttk.Button(grid_configs, command=self.__create_grid, text="Create Grid / Reset")
        create_grid_button.grid(row=1)

        ## solving controls frame
        solving_controls = ttk.Frame(mainframe)
        solving_controls.grid(row=2, padx=10, pady=10)

        ### solving controls frame first row
        mark_queens_button = ttk.Button(solving_controls, text="Mark Queens", command=self.__mark_queens)
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

        # padding
        for child in grid_configs.winfo_children():
            child.grid_configure(padx=5, pady=2)
        for child in solving_controls.winfo_children():
            child.grid_configure(padx=5, pady=2)


    def __pick_color(self):
        """This will change the self.__chosen_color variable and update the color picker button.
        """
        self.__chosen_color = colorchooser.askcolor(initialcolor=self.__chosen_color)[1] # [1] to choose the hex code. For example the entire returned tuple might look like this: ((255, 0, 0), '#ff0000')
        self.__color_picker_button.config(bg=self.__chosen_color) # update the color of the button 





    def __change_cell_color(self, event: tk.Event):
        """Change a cell color to the current self.__chosen_color

        Args:
            event (tk.Event): This tk.Event should correspond to a gui cell.
        """
        cell: tk.Label = event.widget
        cell.config(bg=self.__chosen_color)

    def __create_grid(self):
        """Function to create a cell grid (the queens board) in the GUI with whatever grid size the user has entered
        """

        # reset cells
        for cell in self.__gui_cells: cell.destroy()
        self.__gui_cells = []

        # validation
        try: 
            max_index = int(self.__grid_size_input.get())
            if max_index < 1 or max_index > 20: return
        except ValueError: return

        self.__grid_size = max_index
        for row_number in range(0, max_index):
            for col_number in range(0, max_index):
                cell = tk.Label(
                    self.__cell_grid, 
                    fg="black", bg="white", # i guess fg affects the border color
                    # text="t", 
                    borderwidth=2, relief="solid", # solid border
                    # padx=2, pady=2, # this refers to the interior padding
                    height=2, width=4 # it seems to make a square, height should be half the width
                )
                cell.grid(
                    row=row_number, column=col_number, 
                    padx=2, pady=2 # this refers to the external padding. i.e. the spacing between individual cells
                )
                cell.bind("<Button-3>", func=self.__change_cell_color) # on right-click, change cell color
                self.__gui_cells.append(cell)

    
    def __update_gui_to_board(self):
        # first create Cells
        cells: list[Cell] = []
        for gui_cell in self.__gui_cells:
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
        self.__board = Board(self.__grid_size, self.__grid_size, cells)
        

    def __update_board_to_gui(self):
        for y, row in enumerate(self.__board.cell_grid):
            for x, cell in enumerate(row):
                gui_cell = self.__gui_cells[x + self.__grid_size * y]
                gui_cell.config(text=cell.status.value, bg=cell.color)

    def __mark_queens(self):
        """For the button command.
        """
        self.__update_gui_to_board()
        SolvingLogic.mark_queens_where_certain(self.__board)
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
        SolvingLogic.axiom_1_should_not_block_color_sets(self.__board, times_to_think_ahead)
        self.__update_board_to_gui()

    def axiom_2(self):
        """For the button command.
        """
        self.__update_gui_to_board()
        SolvingLogic.axiom_2_color_common_holdings(self.__board)
        self.__update_board_to_gui()

    def auto_solve(self):
        """For the button command.
        """
        self.__update_gui_to_board()
        SolvingLogic.auto_solve(self.__board)
        self.__update_board_to_gui()