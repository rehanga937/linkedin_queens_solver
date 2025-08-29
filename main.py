import copy

from classes import Board, CellStatus


FILEPATH = "test_files/20250828"

board = Board.from_json(f"{FILEPATH}.json")
turn = 0

while True:
    old_board = copy.deepcopy(board)

    was_queens_marked = board.mark_queens_where_certain()
    if was_queens_marked:
        print(f"Turn {turn}: Queens Marked")
        board.to_excel(f"{FILEPATH}.xlsx", turn)
        turn += 1

    if board.is_game_over():
        print("All queens found!")
        board.to_excel(f"{FILEPATH}.xlsx", turn)
        break

    

    # narrowing down logic
    ## If a row's (or column's) remaining blank cells are all of the same color, then cross of all the other cells of the same color
    # for row_y, row in enumerate(board.cell_grid):
    #     unique_colors = set()
    #     for cell in row:
    #         if cell.status == CellStatus.BLANK:
    #             unique_colors.add(cell.color)
    #     if len(unique_colors) == 1:
    #         color_set = board.color_sets[unique_colors.pop()]
    #         if color_set.held_rows == {row_y}: continue # skip the turn stuff below
    #         color_set.only_keep_one_axis(row_y, 'row')
    #         print(f"Turn {turn}: Row {row_y} with only same color")
    #         board.to_excel(f"{FILEPATH}.xlsx", turn)
    #         turn += 1
    
    # for col_x in range(0, board.length):
    #     unique_colors = set()
    #     for row_y in range(0, board.height):
    #         cell = board.cell_grid[row_y][col_x]
    #         if cell.status == CellStatus.BLANK:
    #             unique_colors.add(cell.color)
    #     if len(unique_colors) == 1:
    #         color_set = board.color_sets[unique_colors.pop()]
    #         if color_set.held_cols == {col_x}: continue # skip the turn stuff below
    #         color_set.only_keep_one_axis(col_x, 'col')
    #         print(f"Turn {turn}: Column {col_x} with only same color")
    #         board.to_excel(f"{FILEPATH}.xlsx", turn)
    #         turn += 1

    ## cross off cells that if were queens, would block other color sets
    blank_cells = board.get_blank_cells()
    for cell in blank_cells:
        if board.would_cell_block_color_set(cell): cell.status = CellStatus.CROSS

    print(f"Turn {turn}: Crossed off cells that would block color sets")
    board.to_excel(f"{FILEPATH}.xlsx", turn)
    turn += 1

    if not Board.has_board_changed(old_board, board): break
