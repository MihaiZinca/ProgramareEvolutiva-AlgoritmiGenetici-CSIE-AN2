import copy
import random

import matplotlib.pyplot as grafic
import numpy as np
from FunctiiCrossoverIndivizi import crossover_simplu


# checks feasibility of the choice x and also computes the objective function
def ok(x, c, v, max):
    val = np.dot(x, v)
    cost = np.dot(x, c)
    return cost <= max, val


# generates the initial population
# I:
# c, v - cost and value vectors
# max - maximum capacity
# dim - number of individuals in the population
# E:
# pop - population together with fitness values

def gen(c, v, max, dim):

    # n = problem dimension
    n = v.size

    # works with the population as a list of dim elements – lists with n+1 individuals each
    pop = []

    for i in range(dim):

        gata = False

        while gata == False:

            # generates candidate x with elements in the interval [0,1]
            x = [random.uniform(0, 1) for _ in range(n)]

            gata, val = ok(x, c, v, max)

        # a feasible candidate solution was found, stored as list x

        # add the fitness value
        x.append(val)

        # add the new individual with objective function value
        # adds another list with n+1 elements as an element of the list pop
        pop.append(x)

    vectv = [pop[i][-1] for i in range(dim)]

    grafic.plot(vectv, "gs", markersize=11, label="Initial")

    return pop


# crossover on the parent population pop, of size dim x (n+1)
# I: pop - as above
#     c, v, max - problem data
#     pc - crossover probability
# E: po - offspring population, offspring fitness values
# asexual recombination is implemented

def crossover_populatie(pop, c, v, max, pc, alpha):

    dim = len(pop)

    n = c.size

    po = copy.deepcopy(pop)

    # the population is traversed such that individuals 0,1 then 2,3 and so on are selected
    for i in range(0, dim-1, 2):

        # selects parents
        x = pop[i][:-1].copy()
        y = pop[i+1][:-1].copy()

        r = np.random.uniform(0, 1)

        if r <= pc:

            c1, c2 = crossover_simplu(x, y, n, alpha)

            fez, val = ok(c1, c, v, max)

            if fez:
                po[i][:-1] = c1.copy()
                po[i][-1] = val

            fez, val = ok(c2, c, v, max)

            if fez:
                po[i+1][:-1] = c2.copy()
                po[i+1][-1] = val

    vectv = [po[i][-1] for i in range(dim)]

    grafic.plot(vectv, "rs", markersize=9, label="Children")

    return po


if __name__ == "__main__":

    alpha = 0.3

    DMax = 50

    c = np.genfromtxt("cost.txt")

    v = np.genfromtxt("valoare.txt")

    pop = gen(c, v, DMax, 12)

    po = crossover_populatie(pop, c, v, DMax, 0.8, alpha)

    grafic.legend()

    grafic.show()

    # print(po)