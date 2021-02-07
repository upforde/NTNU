import LinReg
import numpy as np

#region------------------------Function definitions------------------------

def list_equals(list1, list2):
    """
    Utility function that checks wether the two lists sent in as parameters
    are identicle or not, both in element value and their position.
    """
    for i in range(len(list1)):
        if list1[i] != list2[i]: return False
    return True

def generate_initial_population(individual_size, population_size=15):
    """
    Function that generates a population of size `population_size` with individuals
    of size `individual_size`. The function uses the randint function from numpy to
    generate individuals with random starting positions for each bit.
    """
    return np.random.randint(2, size=[population_size, individual_size])

def parent_selection(measured_population, cheat=0.01):
    """
    Function that probabilistically selects which individuals to select for future breeding.
    """
    fitness_sum=0                   # Instantiate the sum of all fitness across the population
    fitness_max = float('-inf')     # Instantiate the max of fitness across the population
    fitness_min = float('inf')      # Instantiate the min of fitness acroos the population

    # This part finds the sum, max and min of fitness
    for x in measured_population:
        fitness_sum += measured_population[x][1]
        if measured_population[x][1] > fitness_max: fitness_max = measured_population[x][1]
        if measured_population[x][1] < fitness_min: fitness_min = measured_population[x][1]
    
    fitness_dif = fitness_max - fitness_min                 # Calculate the difference between max and min fitness
    
    # This part tries to normalise the values to a range of [0, 1]
    prob_max = 0
    for x in measured_population:
        probability = ((measured_population[x][1])-fitness_min)/fitness_dif # Redistribute the probability from range [fitness_min, fitness_max] to [0, 1]
        measured_population[x].append(probability)                          # Append the probability to the array, so that the number is assosiated with the bitstring
        prob_max += probability                                             # Sum all the probabilities together so that you can later make all probabilities sum to 1

    scalar = 1/prob_max     # Calculate the scalar value that all probabilities need to be scaled by so that they sum to 1

    # This part scales the probabilities and calculates the expected number of individuals in the next population
    for x in measured_population:
        measured_population[x][2] = measured_population[x][2]*scalar                        # Scale the probability
        measured_population[x].append(len(measured_population)*measured_population[x][2])   # Append the calculated expected amount of this indicidual to the array

    parents = []        # Initialising a list that will contain the selected parents
    index = 0           # Initialising an index counter

    # This part selects which parents to choose for further reproduction
    while len(parents) != len(measured_population):                                                     # While the list isn't full
        print(f"{len(parents)} {len(measured_population)}")
        if measured_population[index][2] < 0: measured_population[index][2] = 0                         # Ensure that all probabilities are at least 0. Because of some sloppy code, some probabilities can end up slightly negative
        if cheat < 0.1 : measured_population[index][2] += cheat                                         # If the probability is 0, then add a small "cheat" value to make it non-zero
        count = 0                                                                                       # initiating the count of bitstrings
        for x in parents:                                                                               # Checking if the parents list already contains the
            if list_equals(x, measured_population[index][0]): count+=1                                  # expected amount of bitstrings. If some bitstring is extremely successfull
        if count < measured_population[index][3]:                                                       # then not restrincting it in that way would result in less variety in the parents
            if np.random.rand() <= measured_population[index][2]:                                       # Rolling the dice. If the random number is within the probability of the bitstring
                parents.append(measured_population[index][0])                                           # then the bitstring gets appended to the parents list
        else: print(f"{count} {np.floor(measured_population[index][3])}\n{measured_population}\n{parents}")
        if index+1 == len(measured_population): index = 0                                               # Since this is a while loop, indexing of the list gets reset if the index exceeds the lists length
        else: index += 1            # Since random numbers are rolled, the whole measured_population list might get passed by without a bitstring being added to the parents list, meaning that it needs to be reset

    return parents

def xover(parents, mutation_coefficient=0.05):
    """
    The function that crosses the tails between parents to crate new children. Asexual mating is not allowed in this 
    christian houshold, so if there is a lonly specimen left (such as the case when the population size is an odd number),
    then that individual will not get to mate. After the crossover, the new children are subject to mutation. If there is
    one parent that didn't get to mate, then it too is subject to mutation, so that it has at least a chance to change 
    slightly before continuing into the new generation.
    """
    new_population = []                                                         # Initialize the array that will hold the new population
    while parents:                                                              # While the parent list is not empty
        if len(parents)%2 == 0:                                                 # If there are an even number of individuals
            p1 = parents.pop()                                                  # Pop the first and second parents
            p2 = parents.pop()
            l = np.random.randint(0, len(p1))                                   # Generate the length of the tail that will get crossed over to the other parent
            for i in range(len(p1)):                                            # It's worth mentioning that the tail can be of length 0 or the entire bitstring
                if i>len(p1)-l:                                                 # When the tail is reached
                    temp = p1[i]                                                # Save the bit from the first parent
                    p1[i] = p2[i]                                               # Change that bit to the bit of the second parent
                    p2[i] = temp                                                # Change the bit of the second parent to that of the first
            new_population.append(mutation(p1, mutation_coefficient))           # Append both new children to the new population after subjecting
            new_population.append(mutation(p2, mutation_coefficient))           # them to mutation
        else:
            new_population.append(mutation(parents.pop(), mutation_coefficient))# If the parent is alone, then just append it to the new population after subjecting it to mutation
    
    return new_population

def mutation(individual, mutation_coefficient):
    """
    Function that goes through each bit in a bitstring and mutates it with the `mutation_coefficient` probability.
    """
    for x in individual:                                # For each bit in the bitstring
        if np.random.rand() <= mutation_coefficient:    # The dice is rolled. If the random number is less than the 
            individual[x] = x*(-1)+1                    # mutation coefficient, then the bit is flipped
    return individual

def eye_of_the_tiger(population, fitness_function):
    """
    Function for survivor selection. It doesn't really do anything else than 
    check the fitnes of the members of the population. Since even the badly 
    performing individuals should have a non-zero chanse at reproduction, none can
    be removed at this stage. The selection happens at parent_selection
    """
    measured_population = {}                                                    # Initialize a dictionary that will store the individuals and their fitness
    for i in range(len(population)):
        measured_population[i]=[population[i], fitness_function(population[i])] # Measure the fitness of each individual
    return measured_population

def survivor_crowding():
    pass

def a_sin_of_the_times(bitstring):
    """
    Function that takes a bitstring, calculates it's value in decimal,
    normalises it to be between 0 and 128 and returns the sin of the normalized value
    """
    val = 0                                                     # Initiallizing a value
    for i in range(0, len(bitstring)):
        val += bitstring[i]*np.power(2, len(bitstring)-1-i)     # Calculating the value of the bitstring
    val = val/(np.power(2, len(bitstring))-1)*128               # Normalizing the value to the range [0, 128]
    return np.sin(val)                                          # Returning the sin of the normalized value

def determine_termination(bitstring, fitness_function, threshold):
    return fitness_function(bitstring) >= threshold

def plot():
    pass

def SGA(individual_size=7, population_size=15, num_iterations=100, cheat=0.01, threshold=1):
    print("Initialising population")
    population = generate_initial_population(individual_size, population_size)
    print("Checking fitness")
    measured_population = eye_of_the_tiger(population, a_sin_of_the_times)

    termination = False
    iteration = 0
    while not termination or iteration!=num_iterations:
        iteration += 1
        print(f"Iteration: {iteration}")
        print("Selecting parents")
        parents = parent_selection(measured_population, cheat)
        print("Commencing pating")
        children = xover(parents)
        for child in children:
            termination = determine_termination(child, a_sin_of_the_times, threshold)
            if termination: 
                print(f"Bitstring: {child}\nFitness:{a_sin_of_the_times(child)}\nIteration: {iteration}")
        plot()
        print("Checking children fitness")
        measured_population = eye_of_the_tiger(children, a_sin_of_the_times)
    if not termination:
        print(f"Failed to converge in {num_iterations} iterations")
        print(measured_population)


#endregion-----------------------------------------------------------------

#region------------------------Running the code------------------------

SGA()

#endregion-------------------------------------------------------------