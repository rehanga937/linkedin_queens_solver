import copy

from classes import Cell, Board


board = Board.from_json("test_files/20250828.json")
turn = 0

while True:
    old_board = copy.deepcopy(board)
    board.mark_queens_where_certain()
    board.to_excel("test_files/20250828.xlsx", turn)
    if not Board.has_board_changed(old_board, board): break
    turn += 1
