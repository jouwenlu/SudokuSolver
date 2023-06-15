# SudokuSolver
SudokuSolver using the AC-3 algorithm and inference and guessing algorithm to solve 9x9 sudokus.

*Note: This was originally an independent homework assignment from an Artificial Intelligence class. 

### Source Files
sudokuSolver.py
sudokuGUI.py (given by the course to visualize the Sudoku)

### Overview of Work Done
3 Algorithms were implemented to solve easy, medium, and hard difficulty sudokus. 
  1. AC-3 Algorithm
    Iterates through each arc (pairing of two cells on the sudoku), checks for and removes inconsistencies in the domain (list of possible values) of the two cells until there are no inconsistencies left. It should return a complete solution for easy difficulty sudokus. 
  2. Improved AC-3 Algorithm
    Repeated runs the AC-3 algorithm in a loop. After each iteration, it checks if there are any lone values (a value that only exists in a single cell within its row, column, and quadrant), and updates the board accordingly. The loop runs until the solution is found or until no futher inferences can be made. This algorithm should be sufficient in solving medium difficulty solutions. 
  3. Inference Algorithm with Guessing
    Sometimes no further inferences can be made, and a guess needs to be made to solve the sudoku. This algorithm uses the improved AC-3 algorithm, and recursively runs on each possibility when a guess is made, until the sudoku is solved. 
