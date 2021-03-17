from sys import argv
from numpy.core.numeric import NaN
from numpy.lib.arraysetops import isin
import pandas as pd
import numpy as np
import random

from pandas.io.parsers import read_csv

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
        for value in get_values(attribute, examples):
            eks = get_examples(value, attribute, examples)
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
    elif values[0] < values[1]: return 1
    else: return 0

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
    p = len(examples[examples['Survived'] == 1])
    n = len(examples[examples['Survived'] == 0])

    return calc_entropy(p, n) - remainder(a, examples)
            
def remainder(a, examples):
    '''
    Calculating the remainder, which is the weighted sum of entropy of each variable in a given attribute
    '''
    remainder = 0
    p = examples[examples['Survived'] == 1]
    n = examples[examples['Survived'] == 0]

    # For each value in an attribute
    for value in examples[a].unique():
        pos = p[p[a] == value]
        neg = n[n[a] == value]
        # Calculating the weighted sum of the entropy of each value
        remainder += (len(pos) + len(neg)) / (len(p) + len(n)) * calc_entropy(len(pos), len(neg))
    # Returning the remainder
    return remainder

def calc_entropy(p, n):
    # Checking that the probability will not be 0 or 1
    if p == 0 or p+n == 0 or p+n == p: return 0
    else: 
        # Getting the probability
        prob = p / (p+n)
        # Calculating the entropy
        return - (prob * np.math.log2(prob) + (1 - prob) * np.math.log2(1 - prob))

def get_values(attribute, examples):
    if attribute == 'Cabin': return get_cabin_values(examples)
    elif attribute not in continuous: return examples[attribute].unique()
    else: return get_continuous_values(attribute, examples)

def get_cabin_values(examples):
    unique = []
    for value in examples['Cabin'].values:
        if not isinstance(value, float):
            char = ''.join([i for i in value if not i.isdigit()])
            if char[0] not in unique: unique.append(char[0])
    return unique

def get_continuous_values(attribute, examples):
    potential_splits = []
    sorted = examples.sort_values(by=attribute)
    prev_row = sorted.iloc[0]
    for _, row in sorted.iterrows():
        if str(row[attribute]) != "nan":
            if row['Survived'] != prev_row['Survived']:
                val = (prev_row[attribute]+row[attribute])/2
                if val not in potential_splits: potential_splits.append(val)
            prev_row = row
    split = find_split(potential_splits, attribute, examples)
    values = [f"<{split}", f">={split}"]
    return values

def find_split(potential_splits, attribute, examples):
    split = 0
    highest_info_gain = 0
    for potential_split in potential_splits:
        under = examples[examples[attribute]<potential_split]
        p_under = len(under[under['Survived']==1])
        n_under = len(under[under['Survived']==0])
        over = examples[examples[attribute]>=potential_split]
        p_over = len(over[over['Survived']==1])
        n_over = len(over[over['Survived']==0])

        entropy_under = calc_entropy(p_under, n_under)
        entropy_over = calc_entropy(p_over, n_over)
        entropy = entropy_under + entropy_over
        remainder_under = (p_under + n_under)/(len(under) + len(over)) * entropy_under
        remainder_over = (p_over + n_over)/(len(under) + len(over)) * entropy_over

        info_gain = entropy - (remainder_under + remainder_over)

        if info_gain > highest_info_gain: 
            highest_info_gain = info_gain
            split = potential_split

    return split

def get_examples(value, attribute, examples):
    if attribute == 'Cabin': return examples[(examples[attribute].str.contains(value, na=False))]
    elif attribute not in continuous: return examples.loc[(examples[attribute]==value)]
    else: return get_continuous_examples(value, attribute, examples)

def get_continuous_examples(value, attribute, examples):
    if value[0] == "<":
        return examples[examples[attribute]<float(value[1:])]
    else:
        return examples[examples[attribute]>=float(value[2:])]
    return

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
    elif argv[1] == "-1": attributes = ['Cabin']
else: attributes = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Cabin', 'Embarked']
print(attributes)

# atr = ['Alt','Bar','Fri','Hun','Pat','Rain','Res','Type']
# test = pd.read_csv("Restaurants.csv")
# tree = decision_tree_learning(test, atr)
# tree.print_tree()

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
    i += 1
print(f"Accuracy: {accuracy/i}")