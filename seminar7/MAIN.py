import numpy as np

#fitness function
def fitness(x):
    return 1 + np.sin(2*x[0]-x[2]) + np.cos(x[1])


def fitnessvect(x1, x2, x3, dim):
    values = np.zeros(dim)
    for i in range(dim):
        values[i] = 1 + np.sin(2*x1[i]-x3[i]) + np.cos(x2[i])

        # check feasibility IF NEEDED
        values[i] = round(values[i], 2)
    return values



#point_a
def point_a(dim,a,b):
    population=np.zeros([dim,4])
    x1 = np.round(np.random.uniform(a[0], b[0], dim), 2)
    x2 = np.round(np.random.uniform(a[1], b[1], dim), 2)
    x3 = np.round(np.random.uniform(a[2], b[2], dim), 2)
    fitnesss = fitnessvect(x1, x2, x3 ,dim)
    population = np.column_stack(((x1, x2, x3, fitnesss)))
    return population

#point_b
dim = 3
a = [-1, 0 , -2]
b = [1, 1, 1]
popInitial = point_a(dim,a , b)
newPop = [] # wher we store our new population
alpha = 0.5

# make a for loop for parsing our previous population of parents 2 at a time
# 0 1 and 1 2 and 2 3 and

# for dim - 1 => stop at including dim - 2

for i in range(dim - 1):
    p1 = popInitial[i]
    p2 = popInitial[ i + 1]

    for j in range(len(p1) - 1):

        # check if normalization is required
        if (p1[j] * alpha > b[j]):
            # first check if greater bounds if higher than its bound we normalize to max possible
            p1[j] = b[j]  # b is the max bound
        elif (p1[j] * alpha < a[j]):  # second check if the new value is below the minimum bound
            # if it is we normalize to allowed min
            p1[j] = a[j]
        else:  # if we get a correct value we just multiply by alpha
            p1[j] *= alpha

    p1[len(p1) - 1] = fitness(
        p1[0:3])  # we recalculate the fitness of p1 by sending only its first 3 elements using dynamic parsing of vect

        # repepat for p2
    for j in range(len(p2) - 1):

        if (p2[j] * (1- alpha) > b[j]):
            p2[j] = b[j]
        elif(p2[j] * (1 - alpha) < a[j]):
            p2[j] = a[j]
        else:
            p2[j] *= (1 - alpha)

    p2[len(p2) - 1] = fitness(
        p2[0:3])  # we recalculate the fitness of p1 by sending only its first 3 elements using dynamic parsing of vect

    newChild = np.zeros(dim + 1)
    # we begin creating the new child making sure each element belongs in the appropiate domain like previous

    #   0.1 0.3 0.6
    #   0.6 0.2 0.9
    #   0.7 0.5 1.5

    for j in range(len(p1) - 2):
        if (p1[j] + p2[j] > b[j]):
            newChild[j] = b[j]
        elif(p1[j] + p2[j] < a[j]):
            newChild[j] = a[j]
        else:
            newChild[j] = p1[j] + p2[j]
    print(len(newChild))
    newChild[len(p1) - 1] = fitness(newChild[0 : 3])

    newPop.append(newChild)

print(newPop[:])

