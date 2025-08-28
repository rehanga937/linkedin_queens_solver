from classes import Cell, Board


# cell_1 = Cell(0, 0, "FF0000")
# cell_2 = Cell(2, 1, "0000FF")

# board = Board(
#     length=4, 
#     height=5, 
#     cells=[cell_1, cell_2]
# )
# board.to_excel("haha.xlsx")

# t = Board.from_json("t.json")
# t.to_excel("t.xlsx")

x = Board.from_json("x.json")
# x._Board__mark_queen(x.get_cell_at(4,0))
x.mark_queens_where_certain()
x.to_excel("x.xlsx")

board_3 = Board.from_json("3.json")
board_3.mark_queens_where_certain()
# board_3.mark_queens_where_certain()
board_3.to_excel("3.xlsx")