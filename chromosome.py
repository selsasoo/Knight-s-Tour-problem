import random

NUM_GENES = 63   # 64 squares - 1 (the knight already starts on a square)
NUM_MOVES = 8    # 8 possible knight moves, numbered 1 to 8


class Chromosome:
    def __init__(self, genes=None):
        """Create a chromosome. If no genes are given, generate random ones."""
        if genes is None:
            self.genes = [random.randint(1, NUM_MOVES) for _ in range(NUM_GENES)]
        else:
            self.genes = list(genes)

    def crossover(self, partner):
        """Single-point crossover: returns two new offspring (Chromosomes)."""
        point = random.randint(1, NUM_GENES - 1)
        genes1 = self.genes[:point] + partner.genes[point:]
        genes2 = partner.genes[:point] + self.genes[point:]
        return Chromosome(genes1), Chromosome(genes2)

    def mutation(self, rate=0.02):
        """Each gene has a small probability to become a random move."""
        for i in range(NUM_GENES):
            if random.random() < rate:
                self.genes[i] = random.randint(1, NUM_MOVES)