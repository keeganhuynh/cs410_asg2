import numpy as np
from ops import selection, crossover, benchmark

class genetic_algorithm:
    def __init__(self):
        return
    
    def initialize_population( self, num_individuals, num_variables ):
        pop = np.random.randint(2, size=(num_individuals, num_variables))
        return pop
    
    def convergene_check(self, pop):
        return all(element == pop[0] for element in pop)
    
    def success_check(self, pop, num_parameters):
        return all(element == num_parameters for element in pop)
        

    def POPOP( self, objective, num_individuals, num_parameters, crossover_ ):
        
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
        max_fitness = 0
        while True:
            O = crossover_(P)
            PO = np.vstack([P, O])
            selected_indices = selection().tournament_selection( PO, objective, selection_size )
            P = PO[selected_indices]
            num_evaluations += len(O)
            pop_fitness = np.array([objective(i) for i in P])
            max_fitness = np.max(pop_fitness)
            if self.convergene_check(pop_fitness) or self.success_check(pop_fitness, num_parameters):
                return num_evaluations, max_fitness
        
        return -1


