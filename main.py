import copy

from classes import Board, CellStatus


board = Board.from_json("test_files/20250828.json")
turn = 0

while True:
    old_board = copy.deepcopy(board)

    was_queens_marked = board.mark_queens_where_certain()
    if was_queens_marked:
        board.to_excel("test_files/20250828.xlsx", turn)

    if board.is_game_over():
        print("All queens found!")
        board.to_excel("test_files/20250828.xlsx", turn)
        break

    turn += 1

    # narrowing down logic
    ## cross off cells that if were queens, would block other color sets
    blank_cells = board.get_blank_cells()
    for cell in blank_cells:
        if board.would_cell_block_color_set(cell): cell.status = CellStatus.CROSS

    board.to_excel("test_files/20250828.xlsx", turn)
    turn += 1



    if not Board.has_board_changed(old_board, board): break
