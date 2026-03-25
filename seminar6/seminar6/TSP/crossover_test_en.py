import numpy as np
from FunctiiCrossoverIndivizi import crossover_PMX
import matplotlib.pyplot as grafic


# objective function
def foTSP(p, c):
    n = p.size
    cost = c[p[0]][p[-1]] + sum([c[p[i]][p[i+1]] for i in range(n-1)])
    return 100 / cost


def gen(c, dim):
    n = c.shape[0]

    populatie = np.zeros([dim, n], dtype="int")

    valori = np.zeros(dim)

    for i in range(dim):
        populatie[i] = np.random.permutation(n)

        valori[i] = foTSP(populatie[i], c)

    return populatie, valori


# crossover on the parent population pop, of size dim x n
# I:   pop, valori, as in the generation function
#      c - problem data
#      pc - crossover probability
# E: po, val - offspring population, together with fitness values
# asexual recombination is implemented
def crossover_populatie(pop, valori, c, pc):

    # initializes the offspring population, po, with a matrix of zeros
    dim = pop.shape[0]

    n = pop.shape[1]

    po = np.zeros((dim, n), dtype="int")

    # initializes the fitness values of the offspring population, val, with a matrix of zeros
    val = np.zeros(dim, dtype="float")

    # the population is traversed such that 2 individuals are randomly selected
    # the matrix is accessed after a permutation of the set of row indices 0,2,...,dim-1
    # poz = np.random.permutation(dim)

    # or the population is traversed such that 2 consecutive individuals are selected
    poz = range(dim)  # to preserve order

    for i in range(0, dim-1, 2):

        # selects parents
        x = pop[poz[i]]

        y = pop[poz[i+1]]

        r = np.random.uniform(0, 1)

        if r <= pc:

            # crossover x with y - PMX - suitable for problems with adjacency dependency
            c1, c2 = crossover_PMX(x, y, n)

            v1 = foTSP(c1, c)

            v2 = foTSP(c2, c)

        else:

            # asexual recombination
            c1 = x.copy()

            c2 = y.copy()

            v1 = valori[poz[i]]

            v2 = valori[poz[i+1]]

        # copies the result into the offspring population
        po[i] = c1.copy()

        po[i+1] = c2.copy()

        val[i] = v1

        val[i+1] = v2

    valori = [valori[poz[i]] for i in range(dim)]

    figureaza(valori, val, dim)

    return po, val


def figureaza(valori, val, dim):

    x = range(dim)

    grafic.plot(x, valori, "go", markersize=14, label="Parent fitness")

    grafic.plot(x, val, "ro", markersize=10, label="Offspring fitness")

    grafic.legend()

    grafic.xlabel("Individual indices")

    grafic.ylabel("Individual fitness values")

    grafic.show()


if __name__ == "__main__":

    c = np.genfromtxt("costuri.txt")

    p, v = gen(c, 12)

    o, vo = crossover_populatie(p, v, c, 0.8)