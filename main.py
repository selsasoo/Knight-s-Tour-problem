import tkinter as tk
from population import Population

CELL = 70        # size of a square in pixels
DELAY = 300      # milliseconds between two moves (smaller = faster)


def show_solution(knight, generation):
    """Display the solution and animate the knight move by move.
    Squares are numbered in visiting order."""
    window = tk.Tk()
    window.title(f"Knight's Tour - generation {generation}")

    canvas = tk.Canvas(window, width=8 * CELL, height=8 * CELL)
    canvas.pack()

    label = tk.Label(window, text="", font=("Arial", 12))
    label.pack()

    def draw_board():
        """Draw the empty chessboard."""
        canvas.delete("all")
        for row in range(8):
            for col in range(8):
                color = "#eeeed2" if (row + col) % 2 == 0 else "#769656"
                canvas.create_rectangle(col * CELL, row * CELL,
                                        (col + 1) * CELL, (row + 1) * CELL,
                                        fill=color, outline="")

    def center(square):
        x, y = square
        return x * CELL + CELL // 2, y * CELL + CELL // 2

    def play(step=0):
        """Show move number `step`, then call itself for the next one."""
        if step == 0:
            draw_board()
            canvas.create_text(*center(knight.path[0]), text="1",
                               font=("Arial", 16), tags="number")
            canvas.create_text(*center(knight.path[0]), text="♞",
                               font=("Arial", 36), fill="black", tags="knight")
            label.config(text=f"Move 1 / {len(knight.path)}")
        else:
            square = knight.path[step]
            # Write the move number on the square we just reached
            canvas.create_text(*center(square), text=str(step + 1),
                               font=("Arial", 16), tags="number")
            # Move the knight to the new square
            canvas.delete("knight")
            canvas.create_text(*center(square), text="♞",
                               font=("Arial", 36), fill="black", tags="knight")
            label.config(text=f"Move {step + 1} / {len(knight.path)}")

        if step + 1 < len(knight.path):
            window.after(DELAY, play, step + 1)

    tk.Button(window, text="Replay", command=play).pack(pady=5)

    play()
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

        # Generate the new population
        population.create_new_generation()

    # Display the solution (animated)
    show_solution(bestSolution, population.generation)


if __name__ == "__main__":
    main()