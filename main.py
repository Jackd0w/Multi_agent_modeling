from typing import Dict, List
import matplotlib.pyplot as plt
import seaborn as sns

virus_dict = {'ghost_infected': [],
              'infected': [],
              'recovered': [],
              'not_infected': []}

def calculate_ghost_infected(ghost_infected: int, not_infected: int):
    ghost_infected *= 12
    not_infected -= ghost_infected
    return ghost_infected, not_infected

def calculate_infected(infected: int, ghost_infected: int):
    infected *= 6
    ghost_infected -= infected
    return infected, ghost_infected

def calculate_recovered(recovered: int, infected: int):
    recovered *= 2
    infected -= recovered
    return recovered, infected


def virus_visualisation(virus_dict: Dict):
    x = [0, 1000, 3000, 5000, 7000, 9000]
    y = [0, 1000, 3000, 5000, 7000, 9000]
    plt.plot(x, virus_dict['ghost_infected'], label="ghost_infected")
    plt.plot(x, virus_dict['infected'], label="infected")
    plt.plot(x, virus_dict['recovered'], label="recovered")
    plt.plot(x, virus_dict['not_infected'], label="not_infected")
    plt.legend()
    plt.show()


def virus_table(virus_dict: Dict, ghost_infected: int, infected: int, recovered: int, not_infected:int) -> Dict:
    virus_dict['ghost_infected'].append(ghost_infected)
    virus_dict['infected'].append(infected)
    virus_dict['recovered'].append(recovered)
    virus_dict['not_infected'].append(not_infected)
    return virus_dict
    

def start(virus_dict: Dict, ghost_infected: int, infected: int, recovered: int, not_infected: int):
    for i in range(10):
        ghost_infected, not_infected = calculate_ghost_infected(ghost_infected, not_infected)
        infected, ghost_infected = calculate_infected(infected, ghost_infected)
        recovered, infected = calculate_recovered(recovered, infected)
        virus_dict = virus_table(virus_dict, ghost_infected, infected, recovered, not_infected)
        if not_infected < 0:
            print("Negative number of populatives of step {step}. Stopping...".format(step=i+1))
            break
                
        print("Recovered: {}, Ghost_infected: {}, infected: {}, Not infected: {}".format(recovered, ghost_infected, infected, not_infected))
    virus_visualisation(virus_dict)
    print(virus_table(virus_dict, ghost_infected, infected, recovered, not_infected))


if __name__ == '__main__':
    not_infected = 100000
    ghost_infected = 1
    infected = 1
    recovered = 1
    start(virus_dict, ghost_infected, infected, recovered, not_infected)