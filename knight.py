import random
from chromosome import Chromosome

BOARD_SIZE = 8

# direction -> (dx, dy). x = column, y = row, (0, 0) = top-left square.
MOVES = {
    1: (1, -2),    # up-right
    2: (2, -1),    # right-up
    3: (2, 1),     # right-down
    4: (1, 2),     # down-right
    5: (-1, 2),    # down-left
    6: (-2, 1),    # left-down
    7: (-2, -1),   # left-up
    8: (-1, -2),   # up-left
}


class Knight:
    def __init__(self, chromosome=None):
        """Create a knight. If no chromosome is given, generate a new one."""
        if chromosome is None:
            chromosome = Chromosome()
        self.chromosome = chromosome
        self.position = (0, 0)         # actuel position 
        self.fitness = 0               # number of valid squares visited
        self.path = [self.position]    # list of visited squares

    def move_forward(self, direction):
        """Apply a move: update the position and add it to the path."""
        dx, dy = MOVES[direction]
        x, y = self.position
        self.position = (x + dx, y + dy)
        self.path.append(self.position)

    def move_backward(self, direction):
        """Cancel a move: go back to the previous position."""
        self.path.pop()
        self.position = self.path[-1]

    def is_last_move_valid(self):
        """The last move is valid if the knight is on the board
        and on a square that was not visited before."""
        x, y = self.position
        on_board = 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE
        not_visited = self.position not in self.path[:-1]
        return on_board and not_visited     # return true is last move in board size + not vited before

    def check_moves(self):
        """Check every move of the chromosome and correct the illegal ones."""
        # Start again from the beginning
        self.position = (0, 0)
        self.path = [self.position]

        # Cycle direction chosen once: +1 (forward) or -1 (backward)
        step = random.choice([1, -1])

        for i in range(len(self.chromosome.genes)):
            direction = self.chromosome.genes[i]
            self.move_forward(direction)

            if not self.is_last_move_valid():
                self.move_backward(direction)        # cancel the illegal move

                # Try the 7 other moves by cycling in the chosen direction
                new_direction = direction
                found = False
                for _ in range(7):
                    new_direction = (new_direction - 1 + step) % 8 + 1
                    self.move_forward(new_direction)
                    if self.is_last_move_valid():
                        found = True
                        break
                    self.move_backward(new_direction)

                if found:
                    self.chromosome.genes[i] = new_direction
                else:
                    # No valid move: keep the last move tried
                    self.move_forward(new_direction)
                    self.chromosome.genes[i] = new_direction

    def evaluate_fitness(self):
        """Count the valid squares of the path until an invalid one.
        Maximum value = 64."""
        self.fitness = 0
        visited = []
        for (x, y) in self.path:
            on_board = 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE
            if not on_board or (x, y) in visited:
                break
            visited.append((x, y))
            self.fitness += 1