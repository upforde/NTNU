# Use Python 3.8 or newer (https://www.python.org/downloads/)
import unittest
# Remember to install numpy (https://numpy.org/install/)!
import numpy as np
import pickle
import os

from random import uniform


class Neuron:
    
    def __init__(self, value = 1):
        
        # Links to and from this neuron
        self.links_to = []
        self.links_from = []
        
        # Acitvation value, aka o_k, and inp which is the input value
        self.a = value
        self.inp = value
        
        # Delta
        self.delta = 0
           
            

# Layer hold the neurons
class Layer:
    
    def __init__(self):
        self.units = []
        
    def add(self, neuron):
        self.units.append(neuron)


class Link:
    
    def __init__(self, fn, tn):
    
        # Random weight initialisation
        self.weight = uniform(-0.5, 0.5)
        
        # The link is between these two nodes
        self.fn = fn
        self.tn = tn
        
    

class NeuralNetwork:
    """Implement/make changes to places in the code that contains #TODO."""

    def __init__(self, input_dim: int, hidden_layer: bool) -> None:
        """
        Initialize the feed-forward neural network with the given arguments.
        :param input_dim: Number of features in the dataset.
        :param hidden_layer: Whether or not to include a hidden layer.
        :return: None.
        """

        # --- PLEASE READ --
        # Use the parameters below to train your feed-forward neural network.

        # Number of hidden units if hidden_layer = True.
        self.hidden_units = 25

        # This parameter is called the step size, also known as the learning rate (lr).
        # See 18.6.1 in AIMA 3rd edition (page 719).
        # This is the value of α on Line 25 in Figure 18.24.
        self.lr = 1e-3

        # Line 6 in Figure 18.24 says "repeat".
        # This is the number of times we are going to repeat. This is often known as epochs.
        self.epochs = 256

        # We are going to store the data here.
        # Since you are only asked to implement training for the feed-forward neural network,
        # only self.x_train and self.y_train need to be used. You will need to use them to implement train().
        # The self.x_test and self.y_test is used by the unit tests. Do not change anything in it.
        self.x_train, self.y_train = None, None
        self.x_test, self.y_test = None, None


        self.hidden_layer = hidden_layer

        # Creating the Neural Network, layer by layer
        # A list of Layer objects
        self.layers = []
        
        # 1. Input layer
        self.layers.append( Layer() ) 
        for i in range(input_dim): self.layers[0].add(Neuron())
        
        # 2. Hidden layer
        if self.hidden_layer: 
            self.layers.append( Layer() ) 
            for i in range(self.hidden_units): self.layers[1].add(Neuron())

        # 3. Output layer
        self.layers.append( Layer() ) 
        self.layers[-1].add(Neuron())


        # 4. Link the layers
        if self.hidden_layer:
            
            # Connect the input layer and the hidden layer
            for neuron1 in self.layers[0].units:
                for neuron2 in self.layers[1].units:
                    link = Link(neuron1, neuron2)
                    neuron1.links_to.append(link)
                    neuron2.links_from.append(link)
                    
            # Connect the hidden layer and the output layer
            for neuron1 in self.layers[1].units:
                for neuron2 in self.layers[2].units:
                    link = Link(neuron1, neuron2)
                    neuron1.links_to.append(link)
                    neuron2.links_from.append(link)
                
        else:
            # If there is no hidden layer, then just connect input and output layers
            for neuron1 in self.layers[0].units:
                for neuron2 in self.layers[1].units:
                    link = Link(neuron1, neuron2)
                    neuron1.links_to.append(link)
                    neuron2.links_from.append(link)

        # 5. Add biases to neurons and link them
        if self.hidden_layer:
            for neuron in self.layers[1].units:
                bias = Neuron()
                link = Link(bias, neuron)
                bias.links_to.append(link)
                neuron.links_from.append(link)
            
            # Add bias to the output neuron
            bias = Neuron()
            link = Link(bias, self.layers[2].units[0])
            bias.links_to.append(link)
            self.layers[2].units[0].links_from.append(link)
        
        else:
            # Just add bias to the output neuron
            bias = Neuron()
            link = Link(bias, self.layers[1].units[0])
            bias.links_to.append(link)
            self.layers[1].units[0].links_from.append(link)


    def load_data(self, file_path: str = os.path.join(os.getcwd(), 'data_breast_cancer.p')) -> None:
        """
        Do not change anything in this method.

        Load data for training and testing the model.
        :param file_path: Path to the file 'data_breast_cancer.p' downloaded from Blackboard. If no arguments is given,
        the method assumes that the file is in the current working directory.

        The data have the following format.
                   (row, column)
        x: shape = (number of examples, number of features)
        y: shape = (number of examples)
        """
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
            self.x_train, self.y_train = data['x_train'], data['y_train']
            self.x_test, self.y_test = data['x_test'], data['y_test']


    def train(self) -> None:
        """Run the backpropagation algorithm to train this neural network"""
        
        for x, y in zip(self.x_train, self.y_train):
            
            # Set the values to the input layer 
            for i in range(len(x)):
                self.layers[0].units[i].a = x[i] 
            
            # Start training 
            for e in range(self.epochs):
                
                # Calculate all the values in the network 
                self.forward_propagate()      
                
                # Output node delta
                self.layers[-1].units[0].delta = self.layers[-1].units[0].a * (1 - self.layers[-1].units[0].a ) * (y - self.layers[-1].units[0].a)
                
                # Deltas in the hidden layer
                if self.hidden_layer:
                    for neuron in self.layers[1].units:
                        for link in neuron.links_to: 
                            neuron.delta += link.weight * link.tn.delta
                        neuron.delta *= neuron.a * (1 - neuron.a )
                        
                # Update link weights
                for layer in self.layers[1:]:
                    for neuron in layer.units:
                        for link in neuron.links_from:
                            link.weight += self.lr*link.fn.a*link.tn.delta
                            

    def predict(self, x: np.ndarray) -> float:
        
        # Set the values to the input layer neurons
        for i in range(len(x)):
            self.layers[0].units[i].a = x[i] 
        
        # Calculate values in the network by forward propagation
        self.forward_propagate()
                
        # Calculate the value of the output neuron by backwards iteration
        return self.layers[-1].units[0].a
        
    
    # Forward propagates the values across the network
    def forward_propagate(self):    
        
        # Calculate values in the network
        for layer in self.layers[1:]:
            for neuron in layer.units:

                # Calculate inp and a
                neuron.inp = 0
                for link in neuron.links_from: neuron.inp += link.weight * link.fn.a  
                
                neuron.a = 1 /( 1 + np.exp(-neuron.inp))       


class TestAssignment5(unittest.TestCase):
    """
    Do not change anything in this test class.

    --- PLEASE READ ---
    Run the unit tests to test the correctness of your implementation.
    This unit test is provided for you to check whether this delivery adheres to the assignment instructions
    and whether the implementation is likely correct or not.
    If the unit tests fail, then the assignment is not correctly implemented.
    """

    def setUp(self) -> None:
        self.threshold = 0.8
        self.nn_class = NeuralNetwork
        self.n_features = 30

    def get_accuracy(self) -> float:
        """Calculate classification accuracy on the test dataset."""
        self.network.load_data()
        self.network.train()

        n = len(self.network.y_test)
        correct = 0
        for i in range(n):
            # Predict by running forward pass through the neural network
            pred = self.network.predict(self.network.x_test[i])
            # Sanity check of the prediction
            assert 0 <= pred <= 1, 'The prediction needs to be in [0, 1] range.'
            # Check if right class is predicted
            correct += self.network.y_test[i] == round(float(pred))
        return round(correct / n, 3)

    def test_perceptron(self) -> None:
        """Run this method to see if Part 1 is implemented correctly."""

        self.network = self.nn_class(self.n_features, False)
        accuracy = self.get_accuracy()
        self.assertTrue(accuracy > self.threshold,
                        'This implementation is most likely wrong since '
                        f'the accuracy ({accuracy}) is less than {self.threshold}.')

    def test_one_hidden(self) -> None:
        """Run this method to see if Part 2 is implemented correctly."""

        self.network = self.nn_class(self.n_features, True)
        accuracy = self.get_accuracy()
        self.assertTrue(accuracy > self.threshold,
                        'This implementation is most likely wrong since '
                        f'the accuracy ({accuracy}) is less than {self.threshold}.')


if __name__ == '__main__':
    unittest.main()