import tkinter as tk
from population import Population

CELL = 70                # size of a square in pixels
MARGIN = 40              # space around the board for the coordinates
DELAY = 300              # milliseconds between two moves (smaller = faster)
MAX_GENERATIONS = 20000  # safety limit so the program never runs forever

# Colors (same look as Figure 2 of the project)
LIGHT = "#eeeed2"           # unvisited light square
DARK = "#769656"            # unvisited dark square
LIGHT_VISITED = "#d3df8a"   # visited light square
DARK_VISITED = "#9db84f"    # visited dark square
NUMBER_COLOR = "#7a8c45"    # move numbers
LABEL_COLOR = "#6b7a4a"     # coordinates 1..8 around the board


def square_colors(col, row):
    """Top-left square (0, 0) is a dark one, like in Figure 2."""
    if (col + row) % 2 == 0:
        return DARK, DARK_VISITED
    return LIGHT, LIGHT_VISITED


def show_solution(knight, generation):
    """Display the solution and animate the knight move by move.
    Visited squares are colored and numbered in visiting order."""
    # Only the valid part of the path (the whole path if fitness == 64)
    squares = knight.path[:knight.fitness]
    size = 8 * CELL + 2 * MARGIN

    window = tk.Tk()
    window.title("Knight's Tour")
    window.configure(bg=LIGHT)

    canvas = tk.Canvas(window, width=size, height=size,
                       bg=LIGHT, highlightthickness=0)
    canvas.pack()

    label = tk.Label(window, text="", font=("Arial", 12), bg=LIGHT)
    label.pack()

    job = {"id": None}   # pending animation step (so Replay can cancel it)

    def center(square):
        col, row = square
        return (MARGIN + col * CELL + CELL // 2,
                MARGIN + row * CELL + CELL // 2)

    def draw_coordinates():
        for i in range(8):
            pos = MARGIN + i * CELL + CELL // 2
            text = str(i + 1)
            font = ("Arial", 11, "bold")
            canvas.create_text(pos, MARGIN // 2, text=text,
                               font=font, fill=LABEL_COLOR)           # top
            canvas.create_text(pos, size - MARGIN // 2, text=text,
                               font=font, fill=LABEL_COLOR)           # bottom
            canvas.create_text(MARGIN // 2, pos, text=text,
                               font=font, fill=LABEL_COLOR)           # left
            canvas.create_text(size - MARGIN // 2, pos, text=text,
                               font=font, fill=LABEL_COLOR)           # right

    def render(step):
        """Draw the board as it looks after move number `step` (0-based)."""
        canvas.delete("all")
        draw_coordinates()

        order = {sq: i + 1 for i, sq in enumerate(squares[:step + 1])}
        current = squares[step]

        for row in range(8):
            for col in range(8):
                normal, visited = square_colors(col, row)
                color = visited if (col, row) in order else normal
                x0 = MARGIN + col * CELL
                y0 = MARGIN + row * CELL
                canvas.create_rectangle(x0, y0, x0 + CELL, y0 + CELL,
                                        fill=color, outline="")
                # Number of the visit (hidden under the knight)
                if (col, row) in order and (col, row) != current:
                    canvas.create_text(*center((col, row)),
                                       text=str(order[(col, row)]),
                                       font=("Arial", 13, "bold"),
                                       fill=NUMBER_COLOR)

        canvas.create_text(*center(current), text="♞",
                           font=("Arial", 40), fill="black")
        label.config(text=f"Move {step + 1} / {len(squares)}"
                          f"   (found at generation {generation})")

    def play(step=0):
        render(step)
        if step + 1 < len(squares):
            job["id"] = window.after(DELAY, play, step + 1)
        else:
            job["id"] = None

    def replay():
        if job["id"] is not None:
            window.after_cancel(job["id"])   # stop the running animation
        play(0)

    tk.Button(window, text="Replay", command=replay,
              bg=LIGHT_VISITED, relief="flat").pack(pady=5)

    play(0)
    window.mainloop()


def main():
    population_size = 50

    # Create the initial population
    population = Population(population_size)

    while True:
        # Check the validity of the current population
        population.check_population()

        # Evaluate the current generation and get the best knight
        maxFit, bestSolution = population.evaluate()
        print(f"Generation {population.generation} - best fitness: {maxFit}")
        if maxFit == 64:
            break
        if population.generation >= MAX_GENERATIONS:
            print("Maximum number of generations reached, "
                  "showing the best tour found.")
            break

        # Generate the new population
        population.create_new_generation()

    # Display the solution (animated)
    show_solution(bestSolution, population.generation)


if __name__ == "__main__":
    main()