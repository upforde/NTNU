from math import nan
import pandas as pd
import numpy as np
import random

class Tree():
    def __init__(self, label):
        self.label = label
        self.branches = []
    
    def add_branch(self, action, subtree):
        self.branches.append([action, subtree])

    def print_tree(self):
        for branch in self.branches:
            if isinstance(branch[1], Tree): branch[1].print_tree()
            if isinstance(branch[1], Tree): print(f"{self.label}: \"{branch[0]}\"")
            else: print(f"{self.label} ; {branch[0]}: {branch[1]}")

def decision_tree_learning(examples, attributes, parent_examples = pd.DataFrame()):
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
    values = [0, 0]
    for example in examples['Survived']:
        values[example] += 1
    
    if values[0] == values[1]: return random.randint(0, 1)
    elif values[0] < values[1]: return 0
    else: return 1

def max_importance(attributes, examples):
    info_gain = -1
    most_info_gain_attribute = ""
    for attribute in attributes:
        info_gain_new = importance(attribute, examples)
        if info_gain < info_gain_new:
            info_gain = info_gain_new
            most_info_gain_attribute = attribute 
    if most_info_gain_attribute == "": most_info_gain_attribute = attributes[random.randint(0, len(attributes)-1)]
    return most_info_gain_attribute

def importance(a, examples):
    return entropy(a, examples) - remainder(a, examples)

def entropy(a, examples):
    entropy = 0
    for var in examples[a].unique():
        k_entropy, _ = calc_entropy(var, a, examples)
        entropy -= k_entropy
    return entropy
            
def remainder(a, examples):
    remainder = 0
    total = examples['Survived'].size
    for var in examples[a].unique():
        k_entropy, sum_val = calc_entropy(var, a, examples)
        remainder += (sum_val/total) * k_entropy
    return remainder

def calc_entropy(var, a, examples):
    values = [0, 0]
    for _, row in examples.loc[(examples[a]==var)].iterrows():
        values[row['Survived']] += 1
    sum_val = values[0]+values[1]
    prob = values[1]/sum_val if sum_val != 0 else 0
    if prob == 0 or prob == 1: k_entropy = 0
    else: k_entropy = prob * np.math.log2(prob) + (1-prob) * np.math.log2(1-prob) 
    return k_entropy, sum_val

def test_tree(tree, example):
    root = tree
    while(True):
        for branch in root.branches:
            if branch[0]==example[root.label]:
                if isinstance(branch[1], Tree):
                    root = branch[1]
                else:
                    return branch[1]
        return 0

train_df = pd.read_csv("./titanic/train.csv")
test_df = pd.read_csv("./titanic/test.csv")

attributes = train_df.keys().tolist()

to_remove = ['Survived', 'Name', 'Age']

for attribute in to_remove:
    attributes.remove(attribute)

tree = decision_tree_learning(train_df, attributes)

tree.print_tree()

accuracy = 0
i = 0
for index, row in train_df.iterrows():
    guess = test_tree(tree, row)
    if guess == row['Survived']: 
        accuracy += 1
    i = index

print(f"Accuracy: {accuracy/i}")