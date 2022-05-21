from http.client import NOT_IMPLEMENTED
from typing import List


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


def virus_visualisation():
    pass


def virus_table(ghost_infected: int, infected: int, recovered: int, not_infected:int) -> List:
    virus_table = []
    

def start(ghost_infected: int, infected: int, recovered: int, not_infected: int):
    for i in range(10):
        ghost_infected, not_infected = calculate_ghost_infected(ghost_infected, not_infected)
        infected, ghost_infected = calculate_infected(infected, ghost_infected)
        recovered, infected = calculate_recovered(recovered, infected)

        if not_infected < 0:
            print("Negative number of populatives of step {step}. Stopping...".format(step=i+1))
            break

        print("Recovered: {}, Ghost_infected: {}, infected: {}, Not infected: {}".format(recovered, ghost_infected, infected, not_infected))


if __name__ == '__main__':
    not_infected = 100000
    ghost_infected = 1
    infected = 1
    recovered = 1
    #print(calculate_ghost_infected(ghost_infected, not_infected))
    start(ghost_infected, infected, recovered, not_infected)

