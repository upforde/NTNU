import LinReg
import numpy as np

#region------------------------Function definitions------------------------

def generate_initial_population(individual_size, population_size=15):
    """
    Function that generates a population of size `population_size` with individuals
    of size `individual_size`. The function uses the randint function from numpy to
    generate individuals with random starting positions for each bit.
    """
    return np.random.randint(2, size=[population_size, individual_size])

def parent_selection(population, fitness_function):

    pass

def xover():
    pass

def eye_of_the_tiger():
    pass

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

#endregion-----------------------------------------------------------------

#region------------------------Running the code------------------------

#endregion-------------------------------------------------------------