# This script essentially tests the SolvingLogic auto_solve function


import os
import pickle

from src.queens_board import Board
from src.solving_logic import SolvingLogic


PUZZLE_START_DIRECTORY_PATH = "tests/puzzle_starts"
TRUTH_DIRECTORY_PATH = "tests/truth"

RED = "\033[31m"
RESET = "\033[0m"
GREEN = "\033[32m"

files = os.listdir(PUZZLE_START_DIRECTORY_PATH)
puzzles = []
for file in files:
    puzzles.append(file)

all_tests_passed = True

for puzzle in puzzles:
    # create a Board from the json file
    filepath = f"{PUZZLE_START_DIRECTORY_PATH}/{puzzle}"
    print(f"Filepath: {filepath}")
    board = Board.from_json(filepath)

    # Use the SolvingLogic class auto_solve function to solve the board
    SolvingLogic.auto_solve(board)

    generated_status_grid = board.to_status_grid()

    # load the truth pickle file status grid
    puzzle_name_only = os.path.splitext(puzzle)[0]
    with open(f"{TRUTH_DIRECTORY_PATH}/{puzzle_name_only}.pkl", "rb") as f:
        truth_statuses = pickle.load(f)

    if truth_statuses != generated_status_grid:
        all_tests_passed = False
        print(f"{RED}Puzzle {puzzle} failed!{RESET}")

    print("\n\n")

if all_tests_passed: print(f"{GREEN}All tests passed.{RESET}")