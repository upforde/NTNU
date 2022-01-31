from difflib import SequenceMatcher
from random import seed, random, shuffle
import time
from numpy import math
import argparse

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

def get_pairs(path):
    '''
    Reads the file at the path and creates an array of dictionairies with the pairs
    '''
    pairs = []
    matches = []

    with open(path) as file:
        lines = file.readlines()
        
        for line in lines:
            pair = {}
            # Each item of the pair is split up by a \t
            parts = line.split("\t")
            
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

            if pair["Match"] == 1: matches.append(pair)
            else: pairs.append(pair)
        file.close()

    return pairs, matches

def lowest_similarity(matches):
    '''
    Finds the lowest string similarity of the matching pairs
    '''
    lowest = 1
    for pair in matches:
        match = pair_to_string(pair).split("\t")
        similarity = SequenceMatcher(None, match[0], match[1]).ratio()
        if lowest > similarity: lowest = similarity

    return lowest

def current_milli_time():
    return round(time.time() * 1000)

def create_new_match(pair1, pair2, match):
    '''
    Makes a new pair out of two other pairs.
    '''
    new_pair = {}

    for key in pair1.keys():
        if key == "Match": new_pair[key] = match
        else: 
            if random() > 0.5: new_pair[key] = [pair1[key][round(random())], pair2[key][round(random())]]
            else: new_pair[key] = pair1[key]

    return new_pair


if __name__ == "__main__":
    length = 0

    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str)
    parser.add_argument("--match_chance", type=float, default=0.25)
    parser.add_argument("--augment", type=bool, default=True)

    hp = parser.parse_args()

    pairs, matches = get_pairs(hp.path)

    new_pairs = []
    
    lowest = lowest_similarity(matches)

    seed(current_milli_time())

    for _ in range(len(pairs) + len(matches)):
        # Sometimes create a "new match" out of old matches
        if random() < hp.match_chance:
            match1 = matches[math.trunc((len(matches)-1)*random())]
            match2 = matches[math.trunc((len(matches)-1)*random())]
            # Append the new match into the new pairs array
            new_pairs.append(create_new_match(match1, match2, 1))
        else:
            # Getting two random pairs to make a new pair with
            # There can never be two pairs that are matches, but there can be two non-match pairs
            if random() > 0.5:
                pair1 = pairs[math.trunc((len(pairs)-1)*random())]
                if random() > 0.5: pair2 = pairs[math.trunc((len(pairs)-1)*random())]
                else: pair2 = matches[math.trunc((len(matches)-1)*random())]
            else: 
                pair1 = matches[math.trunc((len(matches)-1)*random())]
                pair2 = pairs[math.trunc((len(pairs)-1)*random())]
            
            # Append the new pair into the new pairs array
            new_pairs.append(create_new_match(pair1, pair2, 0))

    with open("train.txt", "a") as file:
        if hp.augment:
            pairs += matches
            shuffle(pairs)
            for pair in pairs:
                file.write(pair_to_string(pair) + "\n")
        for pair in new_pairs:
            file.write(pair_to_string(pair) + "\n")
        
        file.close()

# ====================== Testing ========================
