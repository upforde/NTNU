import numpy
import pandas

#----------------- Perceptron class ------------------
class Perceptron:
    weights = [0, 0]
    threshold = 0
    bias = 0
    alpha = 0.01

    def activate(self, inputs):
        Sum = self.bias + numpy.dot(self.weights, inputs)
        return 0 if self.threshold > Sum else 1

    def train(self, data):
        for i in range(100):    
            for row in data:
                result = self.activate(row[0:len(row)-1])
                self.bias += self.alpha * (row[len(row)-1] - result)
                 
                for i in row[0:len(row)-1]:
                    for w in range(0, len(self.weights)):
                        self.weights[w] += self.alpha * (row[len(row)-1] - result) * i

    def test(self, data):
        correct = 0
        for row in data:
            if self.activate(row[0:len(row)-1]) == row[len(row)-1]:
                correct += 1
        
        print(str(correct) + "/" + str(len(data)) + " correct")

    def print(self):
        print("Weights: " + str(self.weights))
        print("Bias: " + str(self.bias))

#------------------- Training data -------------------
AND = ((0, 0, 0),
       (0, 1, 0),
       (1, 0, 0),
       (1, 1, 1))

OR = ((0, 0, 0),
      (0, 1, 1),
      (1, 0, 1),
      (1, 1, 1))

XOR = ((0, 0, 0),
       (0, 1, 1),
       (1, 0, 1),
       (1, 1, 0))

data = pandas.read_csv('data.csv')
iris = []

for index, row in data.iterrows():
    iris.append(row.to_list())


#--------------------- Execution ---------------------
print("AND gate")
perceptron_AND = Perceptron()
perceptron_AND.train(AND)
perceptron_AND.print()
perceptron_AND.test(AND)
print()

print("OR gate")
perceptron_OR = Perceptron()
perceptron_OR.train(OR)
perceptron_OR.print()
perceptron_OR.test(OR)
print()

