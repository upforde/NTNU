import os
import string
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from random import random
import torch
from transformers import BertTokenizer, BertForMaskedLM, AdamW
from tqdm import tqdm


PATH = "data/train.txt"
EPOCHS = 3

class MatchesDataset(torch.utils.data.Dataset):
    '''
        Class for presenting data as a dataset implementation
    '''
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}

    def __len__(self):
        return len(self.encodings.input_ids)

def pair_to_string(pair):
    '''
    Takes in the pair dictionary and returns the string version of the pair dictionary in ditto format
    '''
    string = ""

    for key in pair.keys():
        if key == "Match": continue
        string += "COL " + key + " VAL " + pair[key][0]
    
    string += "\t"

    for key in pair.keys():
        if key == "Match": continue
        string += "COL " + key + " VAL " + pair[key][1]
    
    string += "\t" + str(pair["Match"])

    return string

def string_to_pair(string):
    '''
        Takes in a string and returns it as a pair dictionary
    '''
    pair = {}
    # Each item of the pair is split up by a \t
    parts = string.split("\t")
    
    # First item
    first = parts[0].split("COL ")
    for part in first:
        if part == '': continue
        colval = part.split(" VAL ")
        pair[colval[0]] = [colval[1]]

    # Second item
    second = parts[1].split("COL ")
    for part in second:
        if part == '': continue
        colval = part.split(" VAL ")
        pair[colval[0]].append(colval[1])

    # Adding match parameter
    pair["Match"] = int(parts[2])

    return pair

# Get matches and non-matches from the dataset
matches, non_matches = [], []
with open(PATH) as file: 
    lines = file.readlines()
    for line in lines:
        arr = line.split("\t")
        if "1" in arr[-1]: matches.append(line.strip())
        else: non_matches.append(line.strip())

# Set up the BERT model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

if len(os.listdir('./model/') ) != 0: model = BertForMaskedLM.from_pretrained("./model/")
else:
    model = BertForMaskedLM.from_pretrained('bert-base-uncased')

    # Creating the inputs tensor
    inputs = tokenizer(matches, return_tensors='pt', max_length=512, truncation=True, padding='max_length')

    # Creating the masked inputs
    inputs['labels'] = inputs.input_ids.detach().clone()
    rand = torch.rand(inputs.input_ids.shape)
    mask_arr = (rand < 0.15) * (inputs.input_ids != 101) * (inputs.input_ids != 0) * (inputs.input_ids != 102)
    selection = [torch.flatten(mask_arr[i].nonzero()).tolist() for i in range(mask_arr.shape[0])]

    # Masking selected items
    for i in range(mask_arr.shape[0]): inputs.input_ids[i, selection[i]] = 103

    # Creating a dataset for the model to use
    dataset = MatchesDataset(inputs)
    dataloader = torch.utils.data.DataLoader(dataset, shuffle=True)

    # Not enough GPU power :smiling_face_with_tear:
    #device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    device = torch.device('cpu')
    model.to(device)

    # Setting the model into training mode
    model.train()

    optim = AdamW(model.parameters(), lr=1e-5)

    # Training the model
    for epoch in range(EPOCHS):
        loop = tqdm(dataloader, leave=True)
        for batch in loop:
            optim.zero_grad()
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            loss.backward()
            optim.step()

            loop.set_description(f'Epoch {epoch}')
            loop.set_postfix(loss=loss.item())

    model.save_pretrained("./model/")

#TODO: Figure out how to get the model to predict stuff
inputstring = "COL Beer_Name VAL Bourbon Barrel Aged Panama Red Ale COL Brew_Factory_Name VAL Flossmoor Station Restaurant & Brewery COL Style VAL American Amber / Red Ale COL ABV VAL 7.00 % 	COL Beer_Name VAL [MASK] [MASK] [MASK] [MASK] COL Brew_Factory_Name VAL [MASK] [MASK] [MASK] [MASK] COL Style VAL [MASK] [MASK] [MASK] [MASK]  COL ABV VAL [MASK] % 	1"
input = tokenizer(inputstring, return_tensors='pt', max_length=512, padding='max_length')

outputs = model(**input)
