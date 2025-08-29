import copy

from classes import Board, CellStatus


FILEPATH = "test_files/20250827"

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
        break

    board_after_queens_marked = copy.deepcopy(board)


    # Narrowing-down logic

    ## cross off cells that if were queens, would block other color sets
    blank_cells = board.get_blank_cells()
    for cell in blank_cells:
        if board.would_cell_block_color_set(cell): cell.status = CellStatus.CROSS

    if Board.has_board_changed(board_after_queens_marked, board):
        print(f"Turn {turn}: Crossed off cells that would block color sets")
        board.to_excel(f"{FILEPATH}.xlsx", turn)
        turn += 1


    ## if n columns/rows contain the entirety of n colorsets, the cells of all other colors within those n columns/rows can be crossed
    for axis in ['row', 'col']:
        colorset_axis_holdings: dict[str, frozenset[int]] = board.colorset_axis_holdings(axis)
        change_made = False
        changes_made_on = set()

        unique_sets_to_colors_mapping: dict[frozenset[int], list[str]] = {}

        for color, holdings in colorset_axis_holdings.items():
            if holdings not in unique_sets_to_colors_mapping.keys():
                unique_sets_to_colors_mapping[holdings] = [color]
            else:
                unique_sets_to_colors_mapping[holdings].append(color)

        for holdings, colors in unique_sets_to_colors_mapping.items():
            if len(holdings) != len(colors): continue
            # the narrowing-down-logic condition is met
            # we can now cross off all other colors within these n columns/rows
            for idx1 in holdings:
                for idx2 in range(0, board.height):
                    if axis == 'col': cell = board.cell_grid[idx2][idx1]
                    else: cell = board.cell_grid[idx1][idx2]
                    if cell.color not in colors and cell.status == CellStatus.BLANK: 
                        cell.status = CellStatus.CROSS
                        change_made = True
                        changes_made_on.add(frozenset(holdings))

        if change_made:
            if axis == 'row': string = 'rows'
            else: string = 'columns'
            print(f"Turn {turn}: Axis color common used on {string} {changes_made_on}")
            board.to_excel(f"{FILEPATH}.xlsx", turn)
            turn += 1

    if not Board.has_board_changed(old_board, board): # if no change has happened, we are stuck :(
        print("We are stuck :(")
        break
