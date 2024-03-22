import numpy as np
from datetime import datetime
from genetic_algorithm import genetic_algorithm
from tabulate import tabulate
from tqdm import tqdm
mssv = 21520976

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class Bisectoion_method:
    def __init__(self, start_seed, objective, num_parameters, crossover_):
        self.seed = start_seed
        self.objective = objective
        self.num_parameters = num_parameters
        self.crossover = crossover_
        print(color.PURPLE + f'\n{objective}' + color.END + color.YELLOW + f' : {num_parameters} parameters, starting seed = {self.seed}, crossover = {self.crossover}'  + color.END)
    
    def print_result_table(self, mrps, average_number_of_evaluations):
        data = [
            ["Random seed", f"{self.seed + mssv} -> {self.seed + mssv + 9}"],
            # ["Benchmark function", f"{self.objective}"],
            # ["Number of parameters", f"{self.num_parameters}"],
            # ["Crossover method", f"{self.crossover}"],
            # ["< Result >"],
            ["MRPS", f"{int(mrps)}"],
            ["Average number of evaluations", f"{average_number_of_evaluations}"]
        ]
        print(tabulate(data, headers=[], tablefmt="fancy_grid"))
        

    def Check10time( self, num_individuals ):
        total_evaluation_cost = 0
        for i in range(10):
            np.random.seed(mssv + self.seed + i) 
            evaluation_cost, max_fitness = genetic_algorithm().POPOP( self.objective, num_individuals, self.num_parameters,
                                                            self.crossover )
            if max_fitness < self.num_parameters:
                return False, -1, max_fitness
            else:
                total_evaluation_cost += evaluation_cost

        return True, round(total_evaluation_cost/10,4), max_fitness
    
    def upper_bound(self):
        upper = 4
        print("(1) The upper bound of population size is being sought.")
        max_fitness = 0
        progress_bar = tqdm(total=self.num_parameters, desc='Progress:', unit=' steps')
        while max_fitness < self.num_parameters:
            flag, average_number_of_evaluations, max_fitness = self.Check10time( upper )
            progress_bar.update(max_fitness - progress_bar.n)
            if flag:
                break
            else:
                upper *= 2
            if upper > 2**13+1:
                print(color.RED + '\t + Upper found failed when fitness convergene at {max_fitness}' + color.END)
                return -1, -1
        progress_bar.close()
        print(color.GREEN + '\t + Successfully found upper = ', upper, ' individuals' + color.END)
        return upper, average_number_of_evaluations

    
    def MRPS( self ):
        upper, average_number_of_evaluations = self.upper_bound()
        if upper == -1:
            return None, None
        
        lower = upper / 2
        print(f'\n(2) Calculating MRPS ... ')
        while (upper - lower) / upper > 0.1:
            num_individuals = int((upper + lower) / 2)
            success, temp_average_number_of_evaluations, max_fitness = self.Check10time(num_individuals)
            if success:
                upper = num_individuals
                average_number_of_evaluations = temp_average_number_of_evaluations
            else:
                lower = num_individuals
            if upper - lower <= 4:
                break

        print(color.GREEN + f'\t+ MRPS = {upper} individuals!\n' + color.END)
        mrps = upper
        self.print_result_table(mrps, average_number_of_evaluations)
        return mrps, average_number_of_evaluations

def OneMaxReport(log_file_path, crossover_method):
    with open(log_file_path, 'a') as txt_file:
        txt_file.write(f'Running in {datetime.now()}\n')
        objective = 'onemax'
        problem_size = [160]
        crossover_ = crossover_method
        for num_parameters in problem_size:
            for random_seed in range(0, 100, 10):
                bisection = Bisectoion_method( random_seed, objective, num_parameters, crossover_ )
                mrps, average_number_of_evaluations = bisection.MRPS()
                if mrps == None:
                    txt_file.write(f'{random_seed},{crossover_method},{num_parameters},{-1},{-1}\n')
                    return
                else:
                    txt_file.write(f'{random_seed},{crossover_method},{num_parameters},{mrps},{average_number_of_evaluations}\n')
    return 

def TrapKReport(log_file_path, crossover_method):
    with open(log_file_path, 'a') as txt_file:
        txt_file.write(f'Running in {datetime.now()}\n')
        objective = 'concatenated_trap_k'
        problem_size = [10, 20, 40, 80, 160]
        crossover_ = crossover_method
        for num_parameters in problem_size:
            for random_seed in range(0, 100, 10):
                bisection = Bisectoion_method( random_seed, objective, num_parameters, crossover_ )
                mrps, average_number_of_evaluations = bisection.MRPS()
                if mrps == None:
                    txt_file.write(f'{random_seed},{crossover_method},{num_parameters},{-1},{-1}\n')
                    return
                else:
                    txt_file.write(f'{random_seed},{crossover_method},{num_parameters},{mrps},{average_number_of_evaluations}\n')
    return

def LeadingOneReport(log_file_path, crossover_method):
    with open(log_file_path, 'a') as txt_file:
        txt_file.write(f'Running in {datetime.now()}\n')
        objective = 'LeadingOne'
        problem_size = [10, 20, 40, 80, 160]
        crossover_ = crossover_method
        for num_parameters in problem_size:
            for random_seed in range(0, 100, 10):
                bisection = Bisectoion_method( random_seed, objective, num_parameters, crossover_ )
                mrps, average_number_of_evaluations = bisection.MRPS()
                if mrps == None:
                    txt_file.write(f'{random_seed},{crossover_method},{num_parameters},{-1},{-1}\n')
                    return
                else:
                    txt_file.write(f'{random_seed},{crossover_method},{num_parameters},{mrps},{average_number_of_evaluations}\n')
    return

