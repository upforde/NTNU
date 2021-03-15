from sys import argv
from numpy.core.numeric import NaN
import pandas as pd
import numpy as np
import random

class Tree():
    '''
    The tree datastructure. Since this is not a binary tree, meaning that a node can have more or less than two 
    branches, the datastructure to contain the branches is an arraylist.
    '''
    def __init__(self, label):
        self.label = label
        self.branches = []
    
    def add_branch(self, action, subtree):
        '''
        Adds a branch to the tree.
        '''
        self.branches.append([action, subtree])

    def print_tree(self):
        '''
        Recursively traverses the tree depth-first. Prints out the attribute, action taken and value that it leads to.
        The attribute is the first, followed by a semi-colon, then the variable of the attribute in quotation marks.
        If a value follows, then that is the value of the leaf node. If no value follows, that means that there is 
        a new subtree in stead of the value. Since this is recursive, the tree is outputted in the terminal as if it
        grows upwards.
        '''
        for branch in self.branches:
            if isinstance(branch[1], Tree): branch[1].print_tree()
            if isinstance(branch[1], Tree): print(f"{self.label}: \"{branch[0]}\"")
            else: print(f"{self.label} ; \"{branch[0]}\": {branch[1]}")

def decision_tree_learning(examples, attributes, parent_examples = pd.DataFrame()):
    '''
    The decision tree learning algorithm, as depicted in pseudocode in the AIMA book.
    '''
    if examples.empty: return plurality_value(parent_examples)
    elif examples['Survived'].unique().size == 1: return examples['Survived'].unique()[0]
    elif not attributes: return plurality_value(examples)
    else: 
        attribute = max_importance(attributes, examples)
        tree = Tree(attribute)
        for value in examples[attribute].unique():
            eks = examples.loc[(examples[attribute]==value)]
            new_attributes = attributes.copy()
            new_attributes.remove(attribute)
            subtree = decision_tree_learning(eks, new_attributes, examples)
            tree.add_branch(value, subtree)
        return tree

def plurality_value(examples):
    '''
    Returns the value that is most common in the examples, splitting ties randomly
    '''
    values = [0, 0]
    for example in examples['Survived']:
        values[example] += 1
    if values[0] == values[1]: return random.randint(0, 1)
    elif values[0] < values[1]: return 0
    else: return 1

def max_importance(attributes, examples):
    '''
    Finds the attribute with highest information gain
    '''
    info_gain = 0
    most_info_gain_attribute = ""
    # Going through each attribute
    for attribute in attributes:
        # Calculating the information gain of the attribute
        info_gain_new = importance(attribute, examples)
        # If it is higher than the previous attribute, then replace it with the new one
        if info_gain < info_gain_new:
            info_gain = info_gain_new
            most_info_gain_attribute = attribute 
    # Sometimes some attributes can have information gain of 0, meaning no attributes will be selected. In that case
    # select a random attribute from the ones that are left. This should not affect the accuracy in any way, 
    # as if the information gain is the same for 2 attributes, then one gains as much information from splitting on
    # the one attribute as the other.
    if most_info_gain_attribute == "": most_info_gain_attribute = attributes[random.randint(0, len(attributes)-1)]
    return most_info_gain_attribute

def importance(a, examples):
    '''
    Calculates the information gain of an attribute given examples
    '''
    return entropy(a, examples) - remainder(a, examples)

def entropy(a, examples):
    '''
    Calculates the total entropy of the given attribute in the provided examples
    '''
    entropy = 0
    # Going through each variable in the given attribute a
    for var in examples[a].unique():
        # Calculating the entropy for that variable of the attribute
        k_entropy, _ = calc_entropy(var, a, examples)
        # Calculating the total entropy
        entropy += k_entropy
    return entropy
            
def remainder(a, examples):
    '''
    Calculating the remainder, which is the weighted sum of entropy of each variable in a given attribute
    '''
    remainder = 0
    total = examples['Survived'].size
    # Going through each variable in the given attribute a
    for var in examples[a].unique():
        # Calculating the entropy for this variable of the attribute
        k_entropy, sum_val = calc_entropy(var, a, examples)
        # Calculating the weighted sum of entropies
        remainder += (sum_val/total) * k_entropy
    return remainder

def calc_entropy(var, a, examples):
    '''
    Calculates the entropy of a given variable of a given attribute in the provided examples.
    '''
    values = [0, 0]
    # Goes through all where the attribute is of the variable value
    for _, row in examples.loc[(examples[a]==var)].iterrows():
        values[row['Survived']] += 1
    # Getting the amount of examples where the attribute is of the variable value
    sum_val = values[0]+values[1]
    # Defining 0log2(0) = 0
    prob = values[1]/sum_val if sum_val != 0 else 0
    if prob == 0 or prob == 1: k_entropy = 0
    # Calculating the entropy given the variable of a given attribute in the provided examples
    else: k_entropy = -prob * np.math.log2(prob) - (1-prob) * np.math.log2(1-prob) 
    # Returning both the calculated entropy and the amount of examples
    return k_entropy, sum_val

def test_tree(tree, example):
    '''
    Tests the tree with the provided example.
    '''
    root = tree
    # Loops until a value is found
    while(True):
        found = False
        # Checks every branch for values that match the attribute value of the example
        for branch in root.branches:
            # If a value is found
            if branch[0]==example[root.label]:
                found = True
                # If the value of the branch is a subtree, then the root is replaced with the subtree
                # so that the subtree's branches can be checked next
                if isinstance(branch[1], Tree): root = branch[1]
                # If the value is not a tree, then it is a leaf node, and the value is returned
                else: return branch[1]
        # If all branches have been checked but no value has been found
        if(not found):
            # A random branch is selected. There might be a smarter way to do this, 
            # such as selecting the most likely or the most similar branch, comparing 
            # to a different label that is most similar to the current label, etc.
            branch = root.branches[random.randint(0, len(root.branches)-1)]
            # If the value of the branch is a subtree, then the root is replaced with the subtree
            # so that the subtree's branches can be checked next
            if isinstance(branch[1], Tree) : root = branch[1]
            # If the value is not a tree, then it is a leaf node, and the value is returned
            else: return branch[1]

# Hard coding in values that are continuous, as I'm too lazy to figure out wehter that's the case programmatically in the algorithm
continuous = ['Age', 'SibSp', 'Parch', 'Fare']

# Choosing the attributes to grow the tree with
if len(argv) == 2:
    if   argv[1] == "0": attributes = ['Pclass', 'Sex', 'Embarked']
    elif argv[1] == "1": attributes = ['Pclass', 'Name', 'Sex', 'Embarked']
    elif argv[1] == "2": attributes = ['Pclass', 'Sex', 'Cabin', 'Embarked']
    elif argv[1] == "3": attributes = ['Pclass', 'Name', 'Sex', 'Cabin', 'Embarked']
else: attributes = ['Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']
print(attributes)

# Running the training algorithm, growing the tree
train_df = pd.read_csv("./titanic/train.csv")
tree = decision_tree_learning(train_df, attributes)
tree.print_tree()

# Testing the tree with the test data
test_df = pd.read_csv("./titanic/test.csv")
accuracy = 0
i = 0
for index, row in test_df.iterrows():
    guess = test_tree(tree, row)
    if guess == row['Survived']: 
        accuracy += 1
    i = index
print(f"Accuracy: {accuracy/i}")