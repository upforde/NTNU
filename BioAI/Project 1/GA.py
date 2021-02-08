import LinReg as linreg
import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd

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
    #region----------------------------------LEGACY----------------------------------
    # I didn't like this approach, It felt convoluted and overcomplicated. This code was implemented before
    # the a_sin_of_the_times function returned values between 0 and 1. When this code was written, that function
    # returned only the sin(x) values, between -1 and 1

    # # fitness_max = float('-inf')     # Instantiate the max of fitness across the population
    # # fitness_min = float('inf')      # Instantiate the min of fitness acroos the population

    # # # This part finds the sum, max and min of fitness
    # # for x in measured_population:
    # #     fitness_sum += measured_population[x][1]
    # #     if measured_population[x][1] > fitness_max: fitness_max = measured_population[x][1]
    # #     if measured_population[x][1] < fitness_min: fitness_min = measured_population[x][1]
    
    # # fitness_dif = fitness_max - fitness_min                 # Calculate the difference between max and min fitness
    # # if fitness_dif == 0: fitness_dif = 0.0001

    # # # This part tries to normalise the values to a range of [0, 1]
    # # prob_max = 0
    # # for x in measured_population:
    # #     probability = ((measured_population[x][1])-fitness_min)/fitness_dif # Redistribute the probability from range [fitness_min, fitness_max] to [0, 1]
    # #     measured_population[x].append(probability)                          # Append the probability to the array, so that the number is assosiated with the bitstring
    # #     prob_max += probability                                             # Sum all the probabilities together so that you can later make all probabilities sum to 1

    # # if prob_max == 0: prob_max = 1
    # # scalar = 1/prob_max     # Calculate the scalar value that all probabilities need to be scaled by so that they sum to 1

    # # # This part scales the probabilities and calculates the expected number of individuals in the next population
    # # for x in measured_population:
    # #     measured_population[x][2] = measured_population[x][2]*scalar                        # Scale the probability
    # #     measured_population[x].append(len(measured_population)*measured_population[x][2])   # Append the calculated expected amount of this indicidual to the array
    #endregion-------------------------------LEGACY----------------------------------

    fitness_sum=0                                       # Instantiate the sum of all fitness across the population

    for x in measured_population:
        fitness_sum += measured_population[x][1]        # Find the sum of fitness across this generation

    if fitness_sum == 0: fitness_sum = 1                # Ensure that the sum is not zero. If it is, then make it 1 (because it will be divided by)
    for x in measured_population:
        prob = measured_population[x][1]/fitness_sum    # Find the percentege the fitness of the individual makes of the fitness of the entire generation
        measured_population[x].append(prob)             # Append that probability
        measured_population[x].append(len(measured_population)*prob)# Find out how many expected occurences of this individual there will be based on the probability
        
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
    The function that crosses the tails between parents to crate new children. Parents are inscentified to mate with different parents, 
    but if there are no different individuals, then they can still mate with identical individuals. Asexual reproduction is not allowed 
    in this christian houshold, so if there is a lonly specimen left (such as the case when the population size is an odd number), then 
    that individual will not get to mate. After the crossover, the new children are subject to mutation. If there is one parent that 
    didn't get to mate, then it too is subject to mutation, so that it has at least a chance to change slightly before continuing into 
    the new generation.
    """
    new_population = []                                                         # Initialize the array that will hold the new population
    while parents:                                                              # While the parent list is not empty
        if len(parents)%2 == 0:                                                 # If there are an even number of individuals
            p1 = parents.pop()                                                  # Pop the first parent
            p2 = []
            if not np.array_equal(p1, parents[0]): p2 = parents.pop()           # Check if the next parent isin't identical to p1
            else: 
                for i in range(len(parents)):                                   # If the second parent is identical to the first, then check if there are non-identical
                    if not np.array_equal(p1, parents[i]):                      # parents and set p2 to be the first non-identical parent
                        p2 = parents.pop(i)
                        break
            if np.array_equal(p2, []): p2 = parents.pop()                       # If p2 has not been set yet after the check, then it means that there are only identical parents left, and so just pop the next parent
            
            l = np.random.randint(0, len(p1))                                   # Generate the length of the tail that will get crossed over to the other parent
            c1 = np.concatenate((np.asarray(p1)[:l], np.asarray(p2)[l:]))       # Create child with head of the first parent and tail of the second
            c2 = np.concatenate((np.asarray(p2)[:l], np.asarray(p1)[l:]))       # Create child with head of the second parent and tail of the first
            new_population.append(mutation(c1, mutation_coefficient))           # Append both new children to the new population after subjecting
            new_population.append(mutation(c2, mutation_coefficient))           # them to mutation
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

def survivor_crowding(population, fitness_function, mutation_coefficient, allow_mutation = True):
    """
    Function that uses deterministic crowding as described on page 197 of the D. Simon book.
    This function uses 100% of the population to create children, which results in twice the 
    amount of children than the population, meaning more chances to mutate. This does however
    tank performance, meaning that optimisation could be implemented. A variable could be sent
    into the function to chose an amount of randomly chosen individuals that get to mate, making
    much less children.
    """
    survivors = {}                                                      # Initialize the dictionary that will hold survivors
    children = []                                                       # Initialize the array that will hold the children
    for x in population:
        p1 = x                                                          # The first parent
        p2 = population[np.random.randint(0, len(population))]          # The second parent chosen randomly
        l = np.random.randint(0, len(x))                                # Random length of the tail to be crossed
        c1 = np.concatenate((np.asarray(p1)[:l], np.asarray(p2)[l:]))   # Crossing the tails of first and second parent
        c2 = np.concatenate((np.asarray(p2)[:l], np.asarray(p1)[l:]))
        if allow_mutation:                                              # If mutation is allowed
            c1 = mutation(c1, mutation_coefficient)                     # Put both children through mutation
            c2 = mutation(c2, mutation_coefficient)     
        children.append(c1)                                             # Append both children to the children array
        children.append(c2)

    for i in range(len(population)):                                    # Each parent is paired with a child that is the most
        child = find_most_similar(population[i], children)              # similar to the parent without being identical
        fitness_parent = fitness_function(population[i])                # Both child and parent's fitness values are calculated
        fitness_child = fitness_function(child)
        if fitness_parent < fitness_child:
            survivors[i] = [child, fitness_child]                       # If the child is fitter, the child gets added to survivors
        else: survivors[i] = [population[i], fitness_parent]            # If the parent is fitter, the parent gets added to survivors

    return survivors

def find_most_similar(original, population):
    """
    Utility function for finding the most similar individual to the original. Note that it finds the
    most similar, but not identical.
    """
    least_difference = float('inf')                                             # Initialize variable for keeping track of the difference
    child = []                                                                  # Initialize variable for keeping track of the child
    for x in population:
        difference = abs(convert_bin_to_dec(original)-convert_bin_to_dec(x))    # Find the difference of the real world values of the bitstrings
        if difference != 0 and difference < least_difference:                   # If the child is less different than the least different child, then 
            child = x                                                           # replace the least different child with the new child
    return child                                                                # return the most similar child

def a_sin_of_the_times(bitstring):
    """
    Function that takes a bitstring, calculates it's value in decimal,
    normalises it to be between 0 and 128 and returns the sin of the normalized value
    """
    return (np.sin(convert_bin_to_dec(bitstring))+1)/2  # Returning the (sin+1)/2 of the normalized value of the bitstring.
                                                        # The +1 is to make all values above 0 , and the /2 is to make all values in range [0, 1]

def convert_bin_to_dec(bitstring):
    """
    Utility function to convert binary strings to decimal numbers
    """
    val = 0                                                 # Initialising a value
    for i in range(0, len(bitstring)):
        val += bitstring[i]*np.power(2, len(bitstring)-1-i) # Calculating the value of the bitstring in base 10
    return val/(np.power(2, len(bitstring))-1)*128          # Return the value normalised to range between [0, 128]

def convert_bin_to_dec_unnormalized(bitstring):
    """
    Utility function to convert binary strings to decimal numbers without normalizing the value 
    to a range of [0, 128]
    """
    val = 0                                                 # Initialising a value
    for i in range(0, len(bitstring)):
        val += bitstring[i]*np.power(2, len(bitstring)-1-i) # Calculating the value of the bitstring in base 10
    return val

def plot(children, title):
    """
    Utility function to plot all children on the plot based on their fitness.
    """
    x = np.arange(0, 128, 0.1)                                              # Defining the range to be [0, 128]
    y = np.sin(x)                                                           # Defining the function to be sin(x)
    plt.plot(x, y, color='red')                                             # Plotting the sin(x) function
    for child in children:
        plt.plot(convert_bin_to_dec(child), a_sin_of_the_times(child), 'bo')# Plotting each child as a point on the graph
    # Adding decorative text to the plot
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("sin(x)")
    plt.show()

def plot_fs(children, title):
    """
    Plotting the children of fs as points on a graph
    """
    for child in children:
        plt.plot(convert_bin_to_dec_unnormalized(child), feature_selection_fitness(child), 'bo')# Plotting each child as a point on the graph
    # Adding decorative text to the plot
    plt.title(title)
    plt.xlabel("Child value in decimal")
    plt.ylabel("Fitness")
    plt.show()

def SGA(fitness_function, feature_selection = False, crowding = True, crowding_mutation = True, threshold=1, individual_size=7, population_size=15, num_iterations=100, cheat=0.1, mutation_coefficient=0.05, plot_step_size=10):
    """
    Function that runs the SGA algorithm as shown in the progect description.
    """
    if crowding:
        if crowding_mutation:
            title = "SGA with crowding and mutation"                                                    # Setting the title for the plot
        else: title = "SGA with crowding and no mutation"
    else:
        title = "SGA without crowding"
    
    entropy = []                                                                                        # Initialise an array to hold the entropy of the SGA
    best = {}                                                                                           # Initialise a dictionary to hold the best individuals of all generations
    
    if feature_selection:
        population = generate_initial_population(data.shape[1], population_size)
    else: population = generate_initial_population(individual_size, population_size)                    # Generate the initial population

    entropy.append(measure_entropy(population))                                                         # Measure the entropy of the population

    if not crowding: 
        measured_population = eye_of_the_tiger(population, fitness_function, len(population))           # Evaluate the fitness of the initial population
    else: measured_population = survivor_crowding(population, fitness_function, mutation_coefficient, crowding_mutation)

    termination = False                                                                                 # Initialise the termination boolean. If this is true, then the wanted individual has appeared
    iteration = 0                                                                                       # Initialising an int that keeps track of the number of itirations
    
    while not termination:
        iteration += 1                                                                                  # Incrimenting the iteration counter

        parents = parent_selection(measured_population, cheat)                                          # Running parent selection from the population
        children = xover(parents, mutation_coefficient)                                                 # Creating the children population
        
        entropy.append(measure_entropy(children))                                                       # Measure the entropy of the population
        
        if not plot_step_size == 0 and iteration%plot_step_size == 0: 
            if not feature_selection: plot(children, title)                                             # Plotting the graph every time we're on a plotting step
            else: plot_fs(children, title)

        fitness_max = [[], float('-inf')]                                                               # Initializing a value that'll keep track of this generation's closest thing to Einstein
        for child in children:
            fitness = fitness_function(child)                                                           # Measuring fitness of each child
            if fitness_max[1] < fitness: fitness_max = [child, fitness]                                 # Chhecking if the child is this generation's closest thing to Einstein
            termination = fitness >= threshold                                                          # Checking if the child has reached the coveted threshold of fitness
            if termination: 
                print("Found a suitable solution!")
                print(f"Bitstring:{child}\nFitness:{abs(fitness)}\nIteration:{iteration}")              # If the child has reached the threshold, then it's bitstring is printed out in the terminal
                break                                                                                   # together with its fitness value
        best[iteration] = fitness_max                                                                   # This generation's closest thing to Einstein is added to the best dictionary
        if not crowding: measured_population = eye_of_the_tiger(children, fitness_function, len(children))  # The measured_population dictionary replaced with the new population measurements             
        else: measured_population = survivor_crowding(children, fitness_function, mutation_coefficient)     #Differentiating between using and not using crowding

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
        print(f"Bitstring: {best[max_key][0]}\nFitness: {abs(best[max_key][1])}")                       # Printing out Einsteins bitstring and fitness value
    
    return entropy

def feature_selection_fitness(bitstring):
    """
    Function for measuring the fitnes of feature selection bitstrings
    """
    new_data = lr.get_columns(data, bitstring)          # Get the data from the .csv file, omitting the columts represented by a 0 in the bitstring
    fitness = lr.get_fitness(new_data, values)          # Send the new data together with the last column in the .csv file containing the labels info the linear regression algorightm 
    return -fitness                                     # Since the fitness function measures error, we want to lower it to 0 or as low as possible. The 
                                                        # algorithm is meant for maximising fitness, which is why this fitness value is inverted. By doing so, 
                                                        # the highest possible fitness value becomes 0

def measure_entropy(population):
    """
    Function that measures the entropy of the GA algorithm at runtime. It's worth mentioning that 
    the entropy values may vary from run to run, as the bitstrings are instantiated randomly and
    might mutate randomly as well. Also, the initial parameters might alter the entropy values.
    """
    sums = np.zeros(population[0].shape)                    # Initializing an array that will hold sums of each bit throughout a generaiton
    entropy = 0                                             # Initializing the entropy variable
    for x in population:
        sums= np.add(np.asarray(sums), np.asarray(x))       # Sum each bit with all others at their respective positions
    for x in sums:
        x_prob = x/len(population)                          # Each bit gets divided by the amount of individuals in a generation to get the probability that that bit is a one in that generation
        if x_prob != 0: entropy += x*np.log2(x_prob)        # All probabilities get summed into the total entropy of that generation
    return -entropy                                         # The negative value of the entropy is returned

#endregion-----------------------------------------------------------------

#region------------------------Running the code------------------------

if len(sys.argv) > 1 and sys.argv[1] == "SGA":
    individual_size, population_size, threshold, mutation_coefficient, num_iterations, plot_step_size = int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])

    print("Running the SGA with no crowding:")
    entropy_no_crowding = SGA(a_sin_of_the_times, crowding=False, individual_size=individual_size, population_size=population_size, threshold=threshold, mutation_coefficient=mutation_coefficient, num_iterations=num_iterations, plot_step_size=plot_step_size)
    print("Running the SGA with crowding, no mutation")
    entropy_crowding_no_mutation = SGA(a_sin_of_the_times, crowding=True, crowding_mutation=False, individual_size=individual_size, population_size=population_size, threshold=threshold, mutation_coefficient=mutation_coefficient, num_iterations=num_iterations, plot_step_size=plot_step_size)
    print("Running the SGA with crowding and with mutation")
    entropy_crowding_mutation = SGA(a_sin_of_the_times, crowding=True, crowding_mutation=True, individual_size=individual_size, population_size=population_size, threshold=threshold, mutation_coefficient=mutation_coefficient, num_iterations=num_iterations, plot_step_size=plot_step_size)

if len(sys.argv) > 1 and sys.argv[1] == "FS":
    population_size, mutation_coefficient, num_iterations = int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])

    lr = linreg.LinReg()
    df = pd.read_csv("./Dataset.csv")
    data = df.drop(columns=df.columns[-1])
    values = df[df.columns[-1]]

    print("Running the SGA with no crowding:")
    entropy_no_crowding = SGA(feature_selection_fitness, feature_selection = True, crowding=False, population_size=population_size, threshold=0, mutation_coefficient=mutation_coefficient, num_iterations=num_iterations, plot_step_size=0)
    print("Running the SGA with crowding, no mutation")
    entropy_crowding_no_mutation = SGA(feature_selection_fitness, feature_selection = True, crowding=True, population_size=population_size, threshold=0, mutation_coefficient=mutation_coefficient, num_iterations=num_iterations, plot_step_size=0)
    print("Running the SGA with crowding and with mutation")
    entropy_crowding_mutation = SGA(feature_selection_fitness, feature_selection = True, crowding=True, crowding_mutation=True, population_size=population_size, threshold=0, mutation_coefficient=mutation_coefficient, num_iterations=num_iterations, plot_step_size=0)

    print("Getting fitness without feature selection")
    fitness = lr.get_fitness(data, values)
    print(fitness)

plt.plot(entropy_no_crowding, label = 'No crowding')
plt.plot(entropy_crowding_no_mutation, label = 'Crowding, no mutation')
plt.plot(entropy_crowding_mutation, label = 'Crowding, mutation')
plt.legend()
plt.title("Entropy levels of the three SGA algorithms")
plt.show()
#endregion-------------------------------------------------------------