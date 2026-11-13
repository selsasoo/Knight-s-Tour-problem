import random
from knight import Knight


class Population:
    def __init__(self, population_size):
        """Create the initial population of random knights."""
        self.population_size = population_size
        self.generation = 1
        self.knights = [Knight() for _ in range(population_size)]

    def check_population(self):
        """Check (and correct) the moves of every knight."""
        for knight in self.knights:
            knight.check_moves()

    def evaluate(self):
        """Evaluate every knight. Return the best fitness and the best knight."""
        best_knight = self.knights[0]
        for knight in self.knights:
            knight.evaluate_fitness()
            if knight.fitness > best_knight.fitness:
                best_knight = knight
        return best_knight.fitness, best_knight

    def tournament_selection(self, size=3):
        """Pick `size` random knights and return the two best ones."""
        sample = random.sample(self.knights, size)
        sample.sort(key=lambda k: k.fitness, reverse=True)
        return sample[0], sample[1]

    def create_new_generation(self):
        """Build a new population of the same size."""
        new_knights = []
        while len(new_knights) < self.population_size:
            parent1, parent2 = self.tournament_selection(3)

            # Crossover -> two offspring
            child1, child2 = parent1.chromosome.crossover(parent2.chromosome)

            # Mutation on each offspring
            child1.mutation()
            child2.mutation()

            new_knights.append(Knight(child1))
            new_knights.append(Knight(child2))

        self.knights = new_knights[:self.population_size]
        self.generation += 1