import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from random import random
import torch
from transformers import BertTokenizer, BertForMaskedLM, AdamW, TrainingArguments, Trainer
from tqdm import tqdm

PATH = "Data/Beer/train.txt"
EPOCHS = 3

class MatchesDataset(torch.utils.data.Dataset):
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

matches, non_matches = [], []
with open(PATH) as file: 
    lines = file.readlines()
    for line in lines:
        arr = line.split("\t")
        if "1" in arr[-1]: matches.append(line.strip())
        else: non_matches.append(line.strip())

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForMaskedLM.from_pretrained('bert-base-uncased')

inputs = tokenizer(matches, return_tensors='pt', max_length=512, truncation=True, padding='max_length')

inputs['labels'] = inputs.input_ids.detach().clone()

rand = torch.rand(inputs.input_ids.shape)

mask_arr = (rand < 0.15) * (inputs.input_ids != 101) * (inputs.input_ids != 0) * (inputs.input_ids != 102)

selection = [torch.flatten(mask_arr[i].nonzero()).tolist() for i in range(mask_arr.shape[0])]

for i in range(mask_arr.shape[0]):
    inputs.input_ids[i, selection[i]] = 103

dataset = MatchesDataset(inputs)

dataloader = torch.utils.data.DataLoader(dataset, shuffle=True)

# Not enough GPU power :smiling_face_with_tear:
# device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
device = torch.device('cpu')

model.to(device)

model.train()

optim = AdamW(model.parameters(), lr=1e-5)

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
