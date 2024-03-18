import numpy as np
from datetime import datetime
from genetic_algorithm import genetic_algorithm
from tabulate import tabulate

mssv = 21520976

class Bisectoion_method:
    def __init__(self, start_seed, objective, num_parameters, max_evaluations, crossover_):
        self.seed = start_seed
        self.objective = objective
        self.num_parameters = num_parameters
        self.max_evaluations = max_evaluations
        self.crossover = crossover_
    
    def print_result_table(self, mrps, average_number_of_evaluations):
        data = [
            ["Random seed", f"{self.seed + mssv} -> {self.seed + mssv + 9}"],
            ["Benchmark function", f"{self.objective}"],
            ["Number of parameters", f"{self.num_parameters}"],
            ["Number of max evaluations", f"{self.max_evaluations}"],
            ["Crossover method", f"{self.crossover}"],
            ["< Result >"],
            ["<-> MRPS is", f"{int(mrps)}"],
            ["<-> Average number of evaluations", f"{average_number_of_evaluations}"]
        ]
        print(tabulate(data, headers=[], tablefmt="fancy_grid"))
        

    def Check10time( self, num_individuals ):
        total_evaluation_cost = 0
        for i in range(10):
            np.random.seed(mssv + self.seed + i) 
            evaluation_cost = genetic_algorithm().POPOP( self.objective, num_individuals, self.num_parameters,
                                                        self.max_evaluations, self.crossover, convergence_option = True )
            if evaluation_cost == -1:
                return False, -1
            else:
                total_evaluation_cost += evaluation_cost

        return True, round(total_evaluation_cost/10,4)
    
    def upper_bound(self):
        upper = 4
        print("(1)The upper bound of population size is being sought.")
        while True:
            print('<-> Try with upper = ', upper, ' individuals')
            flag, _ = self.Check10time( upper )
            if flag:
                print('\t ... Success with upper = ', upper, ' individuals')
                return upper
            else:
                upper *= 2
            if upper > 2**13:
                return -1
    
    def MRPS( self ):
        upper = self.upper_bound()
        average_number_of_evaluations = -1
        if upper == -1:
            return None, None
        
        lower = upper / 2
        print(f'\n(2) Calculating MRPS ... ')
        while (upper - lower) / upper > 0.1 and int((upper + lower) / 2) % 4 == 0:
            num_individuals = int((upper + lower) / 2)
            success, temp_average_number_of_evaluations = self.Check10time(num_individuals)
            if success:
                upper = num_individuals
                average_number_of_evaluations = temp_average_number_of_evaluations
            else:
                lower = num_individuals
    
            if upper - lower <= 2:
                break
        print(f'Calculation done with {num_individuals} individuals!\n')
        mrps = upper
        self.print_result_table(mrps, average_number_of_evaluations)
        return mrps, average_number_of_evaluations

def OneMaxReport(log_file_path, crossover_method, max_evaluations = 100000):
    with open(log_file_path, 'a') as txt_file:
        txt_file.write(f'Running in {datetime.now()}\n')
        objective = 'onemax'
        problem_size = [10, 20, 40, 80, 160]
        crossover_ = crossover_method
        for num_parameters in problem_size:
            for random_seed in range(0, 100, 10):
                bisection = Bisectoion_method( random_seed, objective, num_parameters, max_evaluations, crossover_ )
                mrps, average_number_of_evaluations = bisection.MRPS()
                if mrps == None:
                    txt_file.write(f'{random_seed},{crossover_method},{num_parameters},{-1},{-1}\n')
                else:
                    txt_file.write(f'{random_seed},{crossover_method},{num_parameters},{mrps},{average_number_of_evaluations}\n')
    return 

def TrapKReport():
    return

def LeadingOneReport():
    return

