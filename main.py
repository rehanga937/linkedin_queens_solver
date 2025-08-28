from classes import Cell, Board


# cell_1 = Cell(0, 0, "FF0000")
# cell_2 = Cell(2, 1, "0000FF")

# board = Board(
#     length=4, 
#     height=5, 
#     cells=[cell_1, cell_2]
# )
# board.to_excel("haha.xlsx")

t = Board.from_json("t.json")
t.to_excel("t.xlsx")