############################################################
# Section 1: Sudoku Solver
############################################################

def sudoku_cells():
    ls = []
    for row in range(9):
        for col in range(9):
            ls.append((row, col))
    return ls

def sudoku_arcs():
    ls = []
    for (row, col) in sudoku_cells():
        # Add cells in same row
        for j in range(9):
            if j != col:
                ls.append(((row, col), (row, j)))
        # Add cells in same col
        for i in range(9):
            if i != row:
                ls.append(((row, col), (i, col)))
        quad_row = int(row / 3) # upper left corner of quadrant cells belongs in
        quad_col = int(col / 3)
        for r in range(3):
            for c in range(3):
                target_cell = (quad_row * 3 + r, quad_col * 3 + c)
                if not (target_cell[0] == row and target_cell[1] == col):
                    if ((row, col), (target_cell[0], target_cell[1])) not in ls:
                        ls.append(((row, col), (target_cell[0], target_cell[1])))
        # Add cells in same square, add if not already in
    return ls


def read_board(path):
    mapping = {}
    f = open(path, "r")
    lines = f.readlines()
    for row in range(9):
        for col in range(9):
            if (lines[row][col] == "*"):
                mapping[(row, col)] = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
            else:
                mapping[(row, col)] = set([int(lines[row][col])])
    f.close()
    #print(mapping)
    return mapping


class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()


    def __init__(self, board):
        self.board = board

    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        # only remove when cell2 is a single val, and cell1 has multiple
        if (len(self.board[cell1]) > 1 and len(self.board[cell2]) == 1):
            cell1_vals = list(self.board[cell1])
            cell2_vals = list(self.board[cell2])
            if cell2_vals[0] in cell1_vals:
                cell1_vals.remove(cell2_vals[0])
                self.board[cell1] = set(cell1_vals)
                return True
        return False


    def find_neighbors(self, cell):
        ls = []
        row, col = cell
        # Add cells in same row
        for j in range(9):
            if j != col:
                ls.append((row, j))
        # Add cells in same col
        for i in range(9):
            if i != row:
                ls.append((i, col))
        quad_row = int(row / 3)  # upper left corner of quadrant cells belongs in
        quad_col = int(col / 3)
        for r in range(3):
            for c in range(3):
                target_cell = (quad_row * 3 + r, quad_col * 3 + c)
                if not (target_cell == cell) and target_cell not in ls:
                        ls.append(target_cell)
        # Add cells in same square, add if not already in
        return ls


    def infer_ac3(self):
        queue = Sudoku.ARCS.copy()
        while len(queue) != 0:
            arc = queue.pop(0)
            if self.remove_inconsistent_values(arc[0], arc[1]) and len(self.get_values(arc[0])) == 1:
                # only check neighbors if changed cell has 1 val left
                for neighbor in self.find_neighbors(arc[0]):
                    queue.append((neighbor, arc[0]))


    def check_lone_values(self, cell):
        vals = self.get_values(cell)
        # Check if there's a value that only exist in this single cell (among the same row, col, OR quadrant)
        if len(vals) > 1:
            for v in vals:
                # Check row
                no_dup = True
                for j in range(9):
                    if j != cell[1]:
                        no_dup = no_dup and v not in self.get_values((cell[0], j))
                if no_dup:
                    self.board[cell] = set([v])
                    return True
                # Check Col
                no_dup = True
                for i in range(9):
                    if i != cell[0]:
                        no_dup = no_dup and v not in self.get_values((i, cell[1]))
                if no_dup:
                    self.board[cell] = set([v])
                    return True
                # Check quadrant
                # Add cells in same col
                quad_row = int(cell[0] / 3)  # upper left corner of quadrant cells belongs in
                quad_col = int(cell[1] / 3)
                no_dup = True
                for r in range(3):
                    for c in range(3):
                        target_cell = (quad_row * 3 + r, quad_col * 3 + c)
                        if not (target_cell == cell):
                            no_dup = no_dup and v not in self.get_values(target_cell)
                if no_dup:
                    self.board[cell] = set([v])
                    return True
        return False


    def infer_improved(self):
        board_old = self.board.copy()
        while (True):
            for cell in Sudoku.CELLS:
                self.check_lone_values(cell)
            self.infer_ac3()
            if board_old == self.board: # Board did not change, then done
                print(self.board)
                return
            board_old = self.board.copy()


    def is_solved(self):
        for cell in Sudoku.CELLS:
            if len(self.get_values(cell)) > 1 or len(self.get_values(cell)) < 1:
                return False
            else:
                for neighbor in self.find_neighbors(cell):
                    v = list(self.get_values(cell))[0]
                    if len(self.get_values(neighbor)) == 1:
                        v_neighbor = list(self.get_values(neighbor))[0]
                        if v == v_neighbor:
                            return False
        return True

    def infer_with_guessing(self):
        self.infer_improved()
        for cell in Sudoku.CELLS:
            if len(self.get_values(cell)) > 1:
                for v in self.get_values(cell):
                    old_b = self.board.copy()
                    self.board[cell] = set([v])
                    self.infer_with_guessing()

                    if self.is_solved():
                        break
                    else:
                        self.board = old_b
                return
