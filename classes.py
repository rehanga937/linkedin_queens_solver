from enum import Enum
import json

from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import PatternFill


class CellStatus(Enum):
    """BLANK, CROSS or QUEEN. Value is a string representing a suitable character.
    """
    BLANK = " "
    CROSS = "x"
    QUEEN = chr(0x2655) # ♕


class Cell:
    """A single cell of the Queens board
    """

    color: str
    """expected to be a 6-digit color value hex: e.g. 'FF0010'"""
    x: int
    """x-coordinate (0-indexing) \n\n x-coord is from left to right. y-coord is from top to bottom. Origin is at the top-left of the board."""
    y: int
    """y-coordinate (0-indexing) \n\n x-coord is from left to right. y-coord is from top to bottom. Origin is at the top-left of the board."""
    status: CellStatus

    def __init__(self, x: int, y: int, color: str):
        """x-coord is from left to right. y-coord is from top to bottom. Origin is at the top-left of the board.

        Args:
            color (str): 6-digit hex code. e.g. 'FF0010'
        """
        self.color = color; 
        self.x = x; self.y = y
        self.status = CellStatus.BLANK


class ColorSet:
    """A group of cells on the Queens board with the same color
    """

    color: str
    """expected to be a 6-digit color value hex: e.g. 'FF0010'"""
    held_rows: set[int]
    """The row numbers held by the ColorSet. 0-indexed. e.g. if the color set spans the first 3 rows, this set would have 0,1,2"""
    held_cols: set[int]
    """The column numbers held by the ColorSet. 0-indexed. e.g. if the color set spans the first 3 columns, this set would have 0,1,2"""
    cells: list[Cell]
    complete: bool

    def __init__(self, cells: list[Cell], color: str):
        """_summary_

        Args:
            color (str): expected to be a 6-digit color value hex: e.g. 'FF0010'
        """

        self.color = color
        self.complete = False
        self.held_cols = set(); self.held_rows = set()

        self.cells = []
        for cell in cells:
            if cell.color == self.color: 
                self.cells.append(cell)
                self.held_cols.add(cell.x)
                self.held_rows.add(cell.y)
            


class Board:
    """The Queens board.
    
    x-coord is from left to right. y-coord is from top to bottom. Origin is at the top-left of the board.
    """

    length: int
    """i.e. how many columns the board has
    """
    height: int
    """i.e. how many rows the board has
    """
    color_sets: list[ColorSet]

    cell_grid: list[list[Cell]]
    """Convention such that we can access a cell via y,x.  i.e. self.cell_grid[y][x].\n 
    So the self.cell_grid would be a list of rows.
    """

    def __init__(self, length: int, height: int, cells: list[Cell]):
        self.length = length
        self.height = height
        self.color_sets = []

        # initialize cell grid, so we can add the cells to it later in any order
        self.cell_grid = []
        for _ in range(0, height):
            row = [None] * length
            self.cell_grid.append(row)

        # add the cells to the grid
        for cell in cells:
            self.cell_grid[cell.y][cell.x] = cell

        # create the color sets
        color_sets_dict: dict[str, list[Cell]] = {}
        for cell in cells:
            if cell.color not in color_sets_dict.keys():
                color_sets_dict[cell.color] = [cell]
            else:
                color_sets_dict[cell.color].append(cell)

        for color in color_sets_dict.keys():
            color_set = ColorSet(
                cells=color_sets_dict[color],
                color=color
            )
            self.color_sets.append(color_set)
    
    @classmethod
    def from_json(cls, filepath: str):
        """Initialize the board from the json representing the board.
        """
        with open(filepath, "rt") as f:
            data = json.load(f)

        # the json has the cell color values as a list of rows.
        # Each row displays the values from left to right
        # The rows are listed in the order top to bottom.
        
        cells: list[Cell] = []

        cell_data: list[list[str]] = data["colors"]
        for i, row in enumerate(cell_data):
            for j, color in enumerate(row):
                cells.append(Cell(j, i, color[1:])) # remove the leading '#' from the otherwise 6-digit color hex code

        return cls(
            length = int(data["cols"]),
            height = int(data["rows"]),
            cells = cells
        )



    def to_excel(self, filepath: str):
        """Save the board (in its current state) to an excel file for visualization.
        """

        wb = Workbook()
        ws = wb.active

        # set column and row lengths (note: openpyxl uses 1-indexing. It also takes columns as left to right and rows as top to bottom.)
        for i in range(1, self.height + 1):
            ws.row_dimensions[i].height = 20
        for i in range(1, self.length + 1):
            ws.column_dimensions[get_column_letter(i)].width = 4

        for row in self.cell_grid:
            for cell in row:
                excel_cell = ws.cell(row=cell.y + 1, column=cell.x + 1, value=cell.status.value) # openpyxl will use 1-indexing
                excel_cell.fill = PatternFill(start_color=cell.color, fill_type="solid")

        wb.save(filepath)



    




