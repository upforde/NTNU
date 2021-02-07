import LinReg
import numpy as np
import matplotlib.pyplot as plt

#region------------------------Function definitions------------------------

def generate_initial_population(individual_size, population_size=15):
    """
    Function that generates a population of size `population_size` with individuals
    of size `individual_size`. The function uses the randint function from numpy to
    generate individuals with random starting positions for each bit.
    """
    return np.random.randint(2, size=[population_size, individual_size])

def parent_selection(measured_population, cheat=0.1):
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
    if fitness_dif == 0: fitness_dif = 0.0001

    # This part tries to normalise the values to a range of [0, 1]
    prob_max = 0
    for x in measured_population:
        probability = ((measured_population[x][1])-fitness_min)/fitness_dif # Redistribute the probability from range [fitness_min, fitness_max] to [0, 1]
        measured_population[x].append(probability)                          # Append the probability to the array, so that the number is assosiated with the bitstring
        prob_max += probability                                             # Sum all the probabilities together so that you can later make all probabilities sum to 1

    if prob_max == 0: prob_max = 1
    scalar = 1/prob_max     # Calculate the scalar value that all probabilities need to be scaled by so that they sum to 1

    # This part scales the probabilities and calculates the expected number of individuals in the next population
    for x in measured_population:
        measured_population[x][2] = measured_population[x][2]*scalar                        # Scale the probability
        measured_population[x].append(len(measured_population)*measured_population[x][2])   # Append the calculated expected amount of this indicidual to the array

    parents = []        # Initialising a list that will contain the selected parents
    index = 0           # Initialising an index counter

    # This part selects which parents to choose for further reproduction
    while len(parents) != len(measured_population):                                                     # While the list isn't full
        if measured_population[index][2] < 0: measured_population[index][2] = 0                         # Ensure that all probabilities are at least 0. Because of some sloppy code, some probabilities can end up slightly negative
        if measured_population[index][2] == 0 and cheat < 1 : measured_population[index][2] += cheat    # If the probability is 0, then add a small "cheat" value to make it non-zero
        if measured_population[index][3] > -1:                                                          # Each time a parent is selected, it's expected number is decreased to ensure that the parent isn't selected a lot more than expected
            if np.random.rand() <= measured_population[index][2]:                                       # Rolling the dice. If the random number is within the probability of the bitstring
                parents.append(measured_population[index][0])                                           # then the bitstring gets appended to the parents list
                measured_population[index][3] -= 1
        
        if index+1 == len(measured_population): index = 0                                               # Since this is a while loop, indexing of the list gets reset if the index exceeds the lists length
        else: index += 1            # Since random numbers are rolled, the whole measured_population list might get passed by without a bitstring being added to the parents list, meaning that it needs to be reset

    return parents

def xover(parents, mutation_coefficient=0.05):
    """
    The function that crosses the tails between parents to crate new children. It also adds the parents into the new population.
    This is to ensure that if the parents are fitter than their children, then they're still in the genepool. Asexual mating is not allowed in this 
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
            new_population.append(mutation(p1, mutation_coefficient))           # Putting the parents through mutation and adding them to the new population, ensuring
            new_population.append(mutation(p2, mutation_coefficient))           # that if they're better than their offspring, then the genepool still has their DNA in it
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
            if individual[x] == 0: individual[x]=1      # mutation coefficient, then the bit is flipped
            else: individual[x]=0
    return individual

def eye_of_the_tiger(population, fitness_function, survivor_count):
    """
    Function for survivor selection. `survivor_count` dictates how many survivors are left in the
    population. The population is sorted by their fitness and then "trimmed", so that the worst
    individuals don't survive.
    """
    population_fitness = {}                                         # Initialize a dictionary that will store the individuals' fitness
    survivors = {}                                                  # Initialize a dictionary that will hold the survivors
    for i in range(len(population)):
        population_fitness[i]=fitness_function(population[i])       # Measure the fitness of each individual
    
    # Sorting the population by fitness, so that the fittest individuals are at the start, while the least fit individuals are at the end of the dictionary 
    population_fitness = dict(sorted(population_fitness.items(), key=lambda item: item[1], reverse=True))

    for i in range(survivor_count):
        key = list(population_fitness.keys())[i]                    # Finding the keys to the most fit individuals. The key is their index in the population
        survivors[i] = [population[key], population_fitness[key]]   # Adding the individual and their fitness to the survivors list.
    
    return survivors

def survivor_crowding():
    pass

def a_sin_of_the_times(bitstring):
    """
    Function that takes a bitstring, calculates it's value in decimal,
    normalises it to be between 0 and 128 and returns the sin of the normalized value
    """
    return np.sin(convert_bin_to_dec(bitstring))  # Returning the sin of the normalized value of the bitstring

def convert_bin_to_dec(bitstring):
    """
    Utility function to convert binary strings to decimal numbers
    """
    val = 0                                                 # Initialising a value
    for i in range(0, len(bitstring)):
        val += bitstring[i]*np.power(2, len(bitstring)-1-i) # Calculating the value of the bitstring in base 10
    return val/(np.power(2, len(bitstring))-1)*128          # Return the value normalised to range between [0, 128]

def plot(children):
    """
    Utility function to plot all children on the plot based on their fitness.
    """
    x = np.arange(0, 128, 0.1)                                              # Defining the range to be [0, 128]
    y = np.sin(x)                                                           # Defining the function to be sin(x)
    plt.plot(x, y, color='red')                                             # Plotting the sin(x) function
    for child in children:
        plt.plot(convert_bin_to_dec(child), a_sin_of_the_times(child), 'bo')# Plotting each child as a point on the graph
    # Adding decorative text to the plot
    plt.title("Simple Genetic Algorithm without crowding")
    plt.xlabel("x")
    plt.ylabel("sin(x)")
    plt.show()

def SGA(threshold=1, individual_size=7, population_size=15, num_iterations=100, cheat=0.1, mutation_coefficient=0.05, plot_step_size=10):
    """
    Function that runs the SGA algorithm as shown in the progect description.
    """
    best = {}                                                                                           # Initialise a dictionary to hold the best individuals of all generations
    population = generate_initial_population(individual_size, population_size)                          # Generate the initial population
    measured_population = eye_of_the_tiger(population, a_sin_of_the_times, population_size)             # Evaluate the fitness of the initial population

    termination = False                                                                                 # Initialise the termination boolean. If this is true, then the wanted individual has appeared
    iteration = 0                                                                                       # Initialising an int that keeps track of the number of itirations
    
    while not termination:
        iteration += 1                                                                                  # Incrimenting the iteration counter

        parents = parent_selection(measured_population, cheat)                                          # Running parent selection from the population
        children = xover(parents, mutation_coefficient)                                                 # Creating the children population
        if iteration%plot_step_size == 0: plot(children)                                                # Plotting the graph every time we're on a plotting step
        
        fitness_max = [[], float('-inf')]                                                               # Initializing a value that'll keep track of this generation's closest thing to Einstein
        for child in children:
            fitness = a_sin_of_the_times(child)                                                         # Measuring fitness of each child
            if fitness_max[1] < fitness: fitness_max = [child, fitness]                                 # Chhecking if the child is this generation's closest thing to Einstein
            termination = fitness >= threshold                                                          # Checking if the child has reached the coveted threshold of fitness
            if termination: 
                print(f"Bitstring: {child}\nFitness:{a_sin_of_the_times(child)}\nIteration: {iteration}")#If the child has reached the threshold, then it's bitstring is printed out in the terminal
                break                                                                                   # together with its fitness value
        best[iteration] = fitness_max                                                                   # This generation's closest thing to Einstein is added to the best dictionary
        measured_population = eye_of_the_tiger(children, a_sin_of_the_times, population_size)           # The measured_population dictionary replaced with the new population measurements
        
        if iteration == num_iterations: break                                                           # If the max number of itterations is reached, then break out of the lööp

    if not termination:                                                                                 # If the coveted threshold fitness value has not been reached when the lööp ends,
        print(f"Failed to reach threshold value of {threshold} " +                                      # then a messege is displayed in the terminal indicating the situation.
        f"in {num_iterations} iterations. Here is the best individual" + 
        " from the entire evolution:")
        max_key = 0                                                                                     # Initialising the int that will hold the key for the best of the best
        max_fitness = float('-inf')                                                                     # Initialising the fitnessvalue that will be used to find the best of the best
        for x in best:
            if best[x][1]>max_fitness:                                                                  # Finding the child that was the best out of all of the children thoughout the generations
                max_fitness = best[x][1]
                max_key = x
        print(f"Bitstring: {best[max_key][0]}\nFitness: {best[max_key][1]}")                            # Printing out Einsteins bitstring and fitness value


#endregion-----------------------------------------------------------------

#region------------------------Running the code------------------------

SGA(individual_size=10, population_size=100, threshold=1, mutation_coefficient=0.1, num_iterations=10, plot_step_size=1)

#endregion-------------------------------------------------------------