import subprocess
import os
import pickle


PUZZLE_START_DIRECTORY_PATH = "tests/puzzle_starts"
TRUTH_DIRECTORY_PATH = "tests/truth"

RED = "\033[31m"
RESET = "\033[0m"
GREEN = "\033[32m"

files = os.listdir(PUZZLE_START_DIRECTORY_PATH)
puzzles = []
for file in files:
    puzzles.append(os.path.splitext(file)[0])

all_tests_passed = True

for puzzle in puzzles:
    subprocess.run(["python3", "main.py",f"{PUZZLE_START_DIRECTORY_PATH}/{puzzle}", 'test']) # run main.py on each puzzle in the directory
    try: os.remove(f"{PUZZLE_START_DIRECTORY_PATH}/{puzzle}.xlsx") # remove the generated excel file, we don't need it
    except FileNotFoundError:
        print(f"{RED}Puzzle {puzzle} excel not generated!{RESET}")
        all_tests_passed = False
        continue

    # load the generated pickle file
    try:
        with open(f"{PUZZLE_START_DIRECTORY_PATH}/{puzzle}.pkl", "rb") as f:
            generated_statuses = pickle.load(f)
    except FileNotFoundError:
        print(f"{RED}Puzzle {puzzle} pickle not found!{RESET}")
        all_tests_passed = False
        continue

    # load the truth pickle file
    with open(f"{TRUTH_DIRECTORY_PATH}/{puzzle}.pkl", "rb") as f:
        truth_statuses = pickle.load(f)

    if truth_statuses != generated_statuses:
        all_tests_passed = False
        print(f"{RED}Puzzle {puzzle} failed!{RESET}")

    # clean-up
    os.remove(f"{PUZZLE_START_DIRECTORY_PATH}/{puzzle}.pkl")
    print("\n\n")

if all_tests_passed: print(f"{GREEN}All tests passed.{RESET}")