import numpy as np
import matplotlib.pyplot as grafic
from FunctiiCrossoverIndivizi import crossover_OCX, crossover_CX

# objective function
def foNR(x):
    # objective function for the N-Queens problem

    # I: x - the evaluated individual (permutation), n - problem dimension
    # E: c - quality (number of pairs of queens that do not attack each other)

    n = x.size
    c = len([(i, j) for i in range(n-1) for j in range(i+1, n) if abs(i-j) != abs(x[i]-x[j])])

    return c


# generates the initial population
# I:
# n - problem dimension
# dim - number of individuals in the population
# E: pop - initial population
def gen(n, dim):
    # defines an ndarray variable with all elements equal to zero
    pop = np.zeros((dim, n+1), dtype="int")

    for i in range(dim):
        # generates the candidate permutation with n elements
        pop[i, :n] = np.random.permutation(n)
        pop[i, n] = foNR(pop[i, :n])

    return pop


# crossover on the parent population pop, with dimension dim x (n+1)
# I: pop, dim, n - as above
#    pc - crossover probability
# E: po - children population
# asexual recombination is implemented
def crossover_populatie(pop, pc):

    # initializes the children population, po, with the parent population
    dim = pop.shape[0]
    m = pop.shape[1]
    n = m - 1

    po = pop.copy()

    # the population is traversed such that individuals 0,1 then 2,3 etc. are selected
    for i in range(0, dim-1, 2):

        # selects the parents
        x = pop[i, :-1]
        y = pop[i+1, :-1]

        r = np.random.uniform(0, 1)

        if r <= pc:

            # crossover x with y - OCX or CX - suitable for N-Queens
            c1, c2 = crossover_OCX(x, y, n)

            val1 = foNR(c1)
            val2 = foNR(c2)

            po[i][:n] = c1.copy()
            po[i][n] = val1

            po[i+1][:n] = c2.copy()
            po[i+1][n] = val2

    figureaza(pop[:, n], po[:, n], dim)

    return po


def figureaza(valori, val, dim):

    grafic.plot(valori, "go", markersize=12, label='Parents')
    grafic.plot(val, "ro", markersize=9, label='Children')

    # include a legend
    grafic.legend(loc="lower left")

    grafic.xlabel('Individuals')
    grafic.ylabel('Fitness')

    grafic.show()


if __name__ == "__main__":

    p = gen(10, 8)

    o = crossover_populatie(p, 0.8)