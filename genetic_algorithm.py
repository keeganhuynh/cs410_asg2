import numpy as np
from ops import selection, crossover, benchmark

class genetic_algorithm:
    def __init__(self):
        return
    
    def initialize_population( self, num_individuals, num_variables ):
        pop = np.random.randint(2, size=(num_individuals, num_variables))
        return pop

    def POPOP( self, objective, num_individuals, num_parameters, max_evaluations, crossover_, convergence_option = False ):
        
        if objective not in ['onemax', 'LeadingOne', 'concatenated_trap_k']:
            raise ValueError("objective must be 'onemax', 'LeadingOne', 'concatenated_trap_k'")

        if crossover_ not in ['1X', 'UX']:
            raise ValueError("crossover must be '1X', 'UX'")
                
        if objective == 'onemax':
            objective = benchmark().onemax
        elif objective == 'LeadingOne':
            objective = benchmark().LeadingOne
        elif objective == 'concatenated_trap_k':
            objective = benchmark().concatenated_trap_k

        if crossover_ == '1X':
            crossover_ = crossover().OneX_crossver
        elif crossover_ == 'UX':
            crossover_ = crossover().UX_crossover

        pop = self.initialize_population(num_individuals, num_parameters)
        pop_fitness = np.array([objective(ind) for ind in pop])
        num_evaluations = num_individuals
        selection_size = num_individuals // 2
        P = pop
        poor_generation = 0 
        max_fitness, last_max_fitness = 0, 0

        while num_evaluations < max_evaluations:
            O = crossover_(P)
            PO = np.vstack([P, O])
            selected_indices = selection().tournament_selection( PO, objective, selection_size )
            P = PO[selected_indices]
            num_evaluations += len(O)
            pop_fitness = np.array([objective(i) for i in P])
            max_fitness = np.max(pop_fitness)
            
            if max_fitness == num_parameters:
                return num_evaluations
            
            if convergence_option == True and max_fitness <= last_max_fitness:
                poor_generation += 1
                if poor_generation == np.log2(num_individuals):
                    return -1
                
            last_max_fitness = max_fitness
        
        # print("Max fitness: ", max_fitness ,' / ', num_parameters)
        return -1


