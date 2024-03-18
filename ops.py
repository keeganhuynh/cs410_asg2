import numpy as np
import numpy.random as npr
import random

class benchmark:
    def __init__(self):
        return
    
    def onemax( self, ind ):
        value = np.sum(ind)
        return value

    def LeadingOne( self, ind ):
        if np.sum(ind) == len(ind):
            return len(ind)
        first_zero = np.argmax(ind == 0)
        return first_zero

    def concatenated_trap_k( self, genotype, k=5):
        fitness = 0
        for i in range(0, len(genotype), k):
            block = genotype[i:i + k]
            fitness += k if np.all(block == 1) else (k - np.count_nonzero(block == 1) - 1)
        return fitness
    
# -----------------------------------------------------------------------------------------------
class crossover:
    def __init__(self):
        return
        
    def OneX_crossver( self, pop ):
        num_individuals = len(pop)
        num_parameters = len(pop[0])
        indices = np.arange(num_individuals)
        np.random.shuffle(indices)
        offspring = []

        for i in range(0, num_individuals, 2):
            idx1 = indices[i]
            idx2 = indices[i+1]
            offspring1 = list(pop[idx1])
            offspring2 = list(pop[idx2])

            crossover_point = np.random.randint(1, num_parameters)
            temp = offspring1[crossover_point:]
            offspring1[crossover_point:] = offspring2[crossover_point:]
            offspring2[crossover_point:] = temp

            offspring.append(offspring1)
            offspring.append(offspring2)

        offspring = np.array(offspring)
        return offspring
    
    def UX_crossover( self, pop ):
        num_individuals = len(pop)
        num_parameters = len(pop[0])
        indices = np.arange(num_individuals)
        np.random.shuffle(indices)
        offspring = []

        for i in range(0, num_individuals, 2):
            idx1 = indices[i]
            idx2 = indices[i+1]
            offspring1 = list(pop[idx1])
            offspring2 = list(pop[idx2])

            for idx in range(0, num_parameters):
                r = np.random.rand()
                if r < 0.5:
                    temp = offspring2[idx]
                    offspring2[idx] = offspring1[idx]
                    offspring1[idx] = temp

            offspring.append(offspring1)
            offspring.append(offspring2)

        offspring = np.array(offspring)
        return offspring
    
class selection:
    def __init__(self):
        return
        
    def tournament(self, objective, pop, indices):
        best = indices[0]
        for i in indices:
            best = i if objective(pop[i]) > objective(pop[best]) else best
        return best

    def tournament_selection(self, pop, objective, selection_size, tournament_size = 4):
        selected_indices = []
        while len(selected_indices) < selection_size:
            individuals_index = np.arange(len(pop))
            np.random.shuffle(individuals_index)
            for i in range(0, len(pop), tournament_size):
                selected_indices.append(self.tournament(objective, pop, individuals_index[i:i+tournament_size]))
        return selected_indices
# ----------------------------------------------------------------------------------------------------------------------------------------