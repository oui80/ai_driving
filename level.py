import random

def lerp(start, end, factor):
    return start * (1 - factor) + end * factor

class NeuralNetwork:
    def __init__(self,neuronCounts):
        self.levels = []
        for i in range(len(neuronCounts)-1):
            self.levels.append(
                Level(
                    neuronCounts[i],
                    neuronCounts[i+1] 
                ))
    
    def feed_forward(self,givenInputs,network):
        outputs = Level.feed_forward(givenInputs,network.levels[0])

        for i in range(1,len(network.levels)):
            outputs = Level.feed_forward(outputs,network.levels[i])
        
        return outputs
    
    
    
    def mutate(network,amount):
        for level in network.levels:        
            for i in range(len(level.biases)):
                level.biases[i] = lerp(
                    level.biases[i],
                    random.uniform(-1, 1),
                    amount
                )
            for i in range(len(level.inputs)):  
                    for j in range(len(level.outputs)):
                        level.weights[i][j] = lerp(
                            level.weights[i][j],
                            random.uniform(-1, 1),
                            amount
                        )


    def mutate2(network, amount, mutation_rate=0.1):
        for level in network.levels:        
            for i in range(len(level.biases)):
                if random.random() < mutation_rate:
                    level.biases[i] += random.uniform(-amount, amount)

            for i in range(len(level.inputs)):  
                for j in range(len(level.outputs)):
                    if random.random() < mutation_rate:
                        level.weights[i][j] += random.uniform(-amount, amount)


class Level:
    def __init__(self,inputCount,outputCount):
        self.inputCount = inputCount
        self.outputCount = outputCount

        self.inputs = [None]*inputCount
        self.outputs = [None]*outputCount
        self.biases = [0]*outputCount

        self.weights = []

        for i in self.inputs:
            self.weights.append([0]*outputCount)

        Level.randomize(self)
        
    def randomize(self):
        for i in range(len(self.inputs)):
            for j in range(len(self.outputs)):
                self.weights[i][j] = random.uniform(-1, 1)
        
        for i in range(len(self.biases)):
            self.biases[i] = random.uniform(-1, 1)

    def feed_forward(givenInputs,level):
        for i in range(len(level.inputs)):
            level.inputs[i] = givenInputs[i]

        for i in range(len(level.outputs)):
            sum = 0
            for j in range(len(level.inputs)):
                sum += level.inputs[j] * level.weights[j][i]
            if sum > level.biases[i]:
                level.outputs[i] = 1
            else:
                level.outputs[i] = 0
        
        return level.outputs
    

        