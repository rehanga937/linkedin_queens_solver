from copy import deepcopy

from src.queens_board import Board, CellStatus


class SolvingLogic:

    @staticmethod
    def mark_queens_where_certain(board: Board):
        _ = board.mark_queens_where_certain()

    @staticmethod
    def axiom_1_should_not_block_color_sets(board: Board, n = 1):
        blank_cells = board.get_blank_cells()
        for cell in blank_cells:
            if board.would_cell_block_color_set_n(cell, n): 
                cell.status = CellStatus.CROSS
                if n > 1: break

    @staticmethod
    def axiom_2_color_common_holdings(board: Board):
        for axis in ['row', 'col']:
            colorset_axis_holdings: dict[str, frozenset[int]] = board.colorset_axis_holdings(axis)
            change_made = False
            changes_made_on = set()

            # for each color, see what other color sets have the same or a subset of holdings
            for color, my_holdings  in colorset_axis_holdings.items():
                for done_holding in changes_made_on:
                    if my_holdings.issubset(done_holding): continue
                common_colors = [color]
                for other_color, others_holdings in colorset_axis_holdings.items():
                    if other_color == color: continue
                    if len(others_holdings) == 0: continue # important, otherwise it would be considered a subset
                    if others_holdings.issubset(my_holdings): common_colors.append(other_color)
                if len(common_colors) == len(my_holdings):
                    # the narrowing-down-logic condition is met
                    # we can now cross off all other colors within these n columns/rows
                    for idx1 in my_holdings:
                        for idx2 in range(0, board.height):
                            if axis == 'col': cell = board.cell_grid[idx2][idx1]
                            else: cell = board.cell_grid[idx1][idx2]
                            if cell.color not in common_colors and cell.status == CellStatus.BLANK: 
                                cell.status = CellStatus.CROSS
                                change_made = True
                                changes_made_on.add(frozenset(my_holdings))

    @staticmethod
    def auto_solve(board: Board):
        # Basically a copy of the old main.py
        # TODO: Could refactor a bit using the other functions in this class

        TIMES_TO_THINK_AHEAD_MAX = 20
        TIMES_TO_THINK_AHEAD_MIN = 2
        times_to_think_ahead = TIMES_TO_THINK_AHEAD_MIN
        turn = 0

        while True:
            old_board = deepcopy(board)

            was_queens_marked = board.mark_queens_where_certain()
            if was_queens_marked:
                print(f"Turn {turn}: Queens Marked")
                turn += 1

            if board.is_game_over():
                print("All queens found!")
                break

            board_after_queens_marked = deepcopy(board)


            # Narrowing-down logic

            ## cross off cells that if were queens, would block other color sets
            blank_cells = board.get_blank_cells()
            for cell in blank_cells:
                if board.would_cell_block_color_set(cell): cell.status = CellStatus.CROSS

            if Board.has_board_changed(board_after_queens_marked, board):
                print(f"Turn {turn}: Crossed off cells that would block color sets")
                turn += 1


            ## if n columns/rows contain the entirety of n colorsets, the cells of all other colors within those n columns/rows can be crossed
            for axis in ['row', 'col']:
                colorset_axis_holdings: dict[str, frozenset[int]] = board.colorset_axis_holdings(axis)
                change_made = False
                changes_made_on = set()

                # for each color, see what other color sets have the same or a subset of holdings
                for color, my_holdings  in colorset_axis_holdings.items():
                    for done_holding in changes_made_on:
                        if my_holdings.issubset(done_holding): continue
                    common_colors = [color]
                    for other_color, others_holdings in colorset_axis_holdings.items():
                        if other_color == color: continue
                        if len(others_holdings) == 0: continue # important, otherwise it would be considered a subset
                        if others_holdings.issubset(my_holdings): common_colors.append(other_color)
                    if len(common_colors) == len(my_holdings):
                        # the narrowing-down-logic condition is met
                        # we can now cross off all other colors within these n columns/rows
                        for idx1 in my_holdings:
                            for idx2 in range(0, board.height):
                                if axis == 'col': cell = board.cell_grid[idx2][idx1]
                                else: cell = board.cell_grid[idx1][idx2]
                                if cell.color not in common_colors and cell.status == CellStatus.BLANK: 
                                    cell.status = CellStatus.CROSS
                                    change_made = True
                                    changes_made_on.add(frozenset(my_holdings))

                if change_made:
                    if axis == 'row': string = 'rows'
                    else: string = 'columns'
                    print(f"Turn {turn}: Axis color common used on {string} {changes_made_on}")
                    turn += 1

            if not Board.has_board_changed(old_board, board): # if no change has happened, we will do the 1st narrowing-down logic axiom 2 times into the future
                board_changed = False
                blank_cells = board.get_blank_cells()
                for cell in blank_cells:
                    if board.would_cell_block_color_set_n(cell, 2): 
                        cell.status = CellStatus.CROSS
                        board_changed = True
                        break # only do one change at a time to avoid crossing off independent thinking ahead results
                if board_changed:
                    print(f"Turn {turn}: Crossed off cells that would block color sets, thinking ahead {times_to_think_ahead} times.")
                    turn += 1


            if not Board.has_board_changed(old_board, board): # if still no change has happened
                times_to_think_ahead += 1
                if times_to_think_ahead > TIMES_TO_THINK_AHEAD_MAX:
                    print(f"We are stuck, even tried thinking {TIMES_TO_THINK_AHEAD_MAX} moves ahead.")
                    break
            else:
                times_to_think_ahead = TIMES_TO_THINK_AHEAD_MIN # reset this value
