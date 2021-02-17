import numpy as np

# We first initialize the transitional matrix, and emission matrix with the given probabilities.
fish_prob = np.array([0.8, 0.3])
fish_prob_inv = np.array([0.2, 0.7])
birds_prob = np.array([0.75, 0.2])
birds_prob_inv = np.array([[0.25], [0.8]])

def forward(current_state, evidence=None):
    """
    Function that moves a state t to state t+1 given evidence t+1
    """
    # Calculating prediction
    prediction = fish_prob * current_state[0] + fish_prob_inv * current_state[1]

    # If no evidence is provided, then this is a prediction operation,
    # and thus should return the prediction
    if evidence == None: return prediction

    # If evidence is provided then adjust the prediction to the evidence
    if evidence: adjusted = np.array([prediction[0]*birds_prob[0], prediction[1]*birds_prob[1]])
    else: adjusted = np.array([prediction[0]*birds_prob_inv[0], prediction[1]*birds_prob_inv[1]])

    # Return the adjusted prediction normalized
    return adjusted * 1/sum(adjusted)
  

evidence = [True, True, False, True, False, True]                       # The for the tasks
probs = [[0.5,0.5]]                                                     # Probs array that will hold the probabilities of each state
                                                                        # Initially holds the starting prob for state 0
print("Task 1 b)")

for i in range(6):                                                      # Run it 6 times
    print(f"For t={i+1}")
    prob = forward(probs[i], evidence[i])                               # Calculate probs of this state given previous state and the evidence for this state
    print(f"\tProbability for P(X_{i+1}|e_1:{i+1})={prob}")
    probs.append(prob)                                                  # Append to the props array for the next round

print("\nTask 1 c)")

for i in range(6, 30):                                                  # Run the rest of 23 rounds
    print(f"For t={i+1}")
    prob = forward(probs[i])                                            # Calculate probs of this state without any new evidence 
    print(f"\tProbability for P(X_{i+1}|e_1:4)={prob}")
    probs.append(prob)                                                  # Append to the probs array for the next round