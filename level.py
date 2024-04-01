import random

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
    

        