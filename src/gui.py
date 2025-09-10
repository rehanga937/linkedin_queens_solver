import tkinter as tk
from tkinter import ttk, colorchooser

from src.queens_board import Board, Cell, CellStatus
from src.solving_logic import SolvingLogic


class GUI:

    __gui_cells: list[tk.Label] = []
    __chosen_color = "white" # initial color
    __grid_size: int = 0
    __board: Board

    def __init__(self, root: tk.Tk):
        
        root.title("LinkedIn Queens Solver")

        # mainframe
        mainframe = ttk.Frame(root) # TODO: add padding
        mainframe.grid(row=0, column=0)

        # first row (grid size input)
        grid_size_input_label = ttk.Label(mainframe, text="Grid Size")
        grid_size_input_label.grid(row=0, column=0)
        self.__grid_size_input = ttk.Entry(mainframe)
        self.__grid_size_input.grid(row=0, column=1)

        # third row (color picker)
        color_picker_label = ttk.Label(mainframe, text="Pick Color")
        color_picker_label.grid(row=2, column=0)

        self.__color_picker_button = tk.Button(
            mainframe, 
            command=self.__pick_color,
            height=2,
            width=4,
            bg=self.__chosen_color # set the initial color
        )

        self.__color_picker_button.grid(row=2, column=1)

        # fourth row (queens cell grid)
        self.__cell_grid = ttk.Frame(mainframe)
        self.__cell_grid.grid(row=3, columnspan=2)

        # second row (create grid button)
        create_grid_button = ttk.Button(mainframe, command=self.__create_grid, text="Create Grid")
        create_grid_button.grid(row=1)

        # fifth row (solver buttons)
        mark_queens_button = ttk.Button(mainframe, text="Mark Queens", command=self.__mark_queens)
        mark_queens_button.grid(row=4, column=0)


    def __pick_color(self):
        self.__chosen_color = colorchooser.askcolor(initialcolor=self.__chosen_color)[1] # [1] to choose the hex code. For example the entire returned tuple might look like this: ((255, 0, 0), '#ff0000')
        self.__color_picker_button.config(bg=self.__chosen_color) # update the color of the button 





    def __change_cell_color(self, event: tk.Event):
        cell: tk.Label = event.widget
        cell.config(bg=self.__chosen_color)

    def __create_grid(self):

        # reset cells
        for cell in self.__gui_cells: cell.destroy()
        self.__gui_cells = []
        # TODO: if not int validation

        max_index = int(self.__grid_size_input.get())
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
        # TODO: Assume self._gui_cells is sorted
        for y, row in enumerate(self.__board.cell_grid):
            for x, cell in enumerate(row):
                gui_cell = self.__gui_cells[x + self.__grid_size * y]
                # if cell.status == CellStatus.BLANK: continue
                gui_cell.config(text=cell.status.value, bg=cell.color)

    def __mark_queens(self):
        self.__update_gui_to_board()
        SolvingLogic.mark_queens_where_certain(self.__board)
        self.__update_board_to_gui()
