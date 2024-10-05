import neat
import os

class MyNeat:
    def __init__(self):
        local_dir = os.path.dirname(__file__)
        config_file = os.path.join(local_dir, "NEATconfig-file.txt")
        self.config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

        self.stats = None
        self.population = None
        
    
    def create(self):
        self.population = neat.Population(self.config)

        self.population.add_reporter(neat.StdOutReporter(True))
        self.stats = neat.StatisticsReporter()
        self.population.add_reporter(self.stats)


    def run(self,eval_genomes ,n):
        self.winner = self.population.run(eval_genomes, n)

        return self.winner

    def output(self, inputs):
        return self.genome.output(inputs)