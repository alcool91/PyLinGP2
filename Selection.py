##################################################################################
# Library for selection of generations in genetic programming
#
#
import random

def I(program, inp):
    """ Interprets program when run on input inp """
    program.reset()
    program._set_input(inp)
    return_val = program.execute()

    return return_val


def tournament_selection(initial_population, fitness, fitness_cases, opt_max = False, pop_fitnesses=None, next_gen_size=None, k=2, p=1):
    """ 
    initial_population: An array of programs,
    next_gen_size:      Number of individuals to select from the intial population (defaults to the size of initial_population),
    fitness:            Fitness function to use in selection of individuals. Should take a program and set of fitness cases as input.
    fitness_cases:      List of inputs to evaluate fitness on
    pop_fitnesses:      Optionally pass a list of fitnesses of individuals to avoid recomputing them
    opt_max             True if fitter individuals have higher fitness, false if fitter individuals have lower fitness
    k:                  Number of individuals to randomly select for the tournament (default 2)
    p:                  Probability of choosing the best individual (default 1 - deterministic tournament)
    ------------------------------------------------------------------------------------------------------------------------------------
    returns:            A list of programs selected of size next_gen_size
    """
    if next_gen_size == None:
        next_gen_size = len(initial_population)
    if pop_fitnesses == None:
        pop_fitnesses = []
        for individual in initial_population:
            ind_fit = 0
            for case in fitness_cases:
                ind_fit += fitness(individual, cases)
            pop_fitnesses.append(ind_fit)
    next_gen = []
#    probs   = [p*((1-p)**(k-i-1)) for i in range(k)]
    while len(next_gen) < next_gen_size:
        indxs             = [random.randint(0, len(initial_population)) for i in range(k)] 
        fittest           = sorted(indxs, key=lambda x: pop_fitnesses[x], reverse = not opt_max)  
        i = 0
        while True:
            val = random.random()
            if val <= p:
                next_gen.append(initial_population[fittest[i]])
                break
            i = (i+1) % k
        
    return next_gen


def random_selection(initial_population, next_gen_size=None):
    """ 
    initial_population: An array of programs,
    next_gen_size:      Number of individuals to select from the intial population (defaults to the size of initial_population),

    ------------------------------------------------------------------------------------------------------------------------------------
    returns:            A list of programs selected of size next_gen_size
    
    Randomly select individuals (with replacement) from initial population
    """
    if next_gen_size == None:
        next_gen_size = len(initial_population)
    next_gen = []
    while len(next_gen) < next_gen_size:
        next_gen.append(random.choice(initial_population))
    return next_gen

def elite_selection(initial_population, fitness, fitness_cases, opt_max = False, pop_fitnesses=None, next_gen_size=None, k=1):
    """ 
    initial_population: An array of programs,
    next_gen_size:      Number of individuals to select from the intial population (defaults to the size of initial_population),
    fitness:            Fitness function to use in selection of individuals. Should take a program and set of fitness cases as input.
    fitness_cases:      List of inputs to evaluate fitness on
    pop_fitnesses:      Optionally pass a list of fitnesses of individuals to avoid recomputing them
    opt_max             True if fitter individuals have higher fitness, false if fitter individuals have lower fitness
    k:                  Number of fittest individuals to keep (default 1)

    ------------------------------------------------------------------------------------------------------------------------------------
    returns:            A list of programs selected of size next_gen_size
    """
    if pop_fitnesses == None:
        pop_fitnesses = []
        for individual in initial_population:
            ind_fit = 0
            for case in fitness_cases:
                ind_fit += fitness(individual, cases)
            pop_fitnesses.append(ind_fit)
            
    fittest_pop = sorted(range(len(initial_population)), key=lambda x: pop_fitnesses[x], reverse = not opt_max)
    return fittest_pop[:k]