# create list
# a. empty list
L=[]
print(L)

# b. list with N elements, without values
N=10
L=[None]*N
# L=[0]*N - N values, all 0

# accessing elements
L[0]=L[2]=7
print(L)

# removing all elements from the list
L.clear()
print(L)

# adding elements to L
L.append(7)
L=L+[10]
L.append(8)
print(L)

# deleting an element from a given position
L.pop(0)
print(L)

# inserting an element at a given position
L.insert(2,7)
print(L)

# extending L with another list
L.extend([2,3,4])
print(L)

# List comprehensions - examples

# L = {x | x in M and P(x)}

# PA=[x for x in range(10,31,5)]

# generating a list containing the arithmetic progression 45...-34 with ratio -5
L=[i for i in range(45,-34,-5)]

# selecting elements divisible by k from the list
k=3
LP=[x for x in L if x%k==0]

# computing the maximum of the list and determining its position
maxim=max(L)
index=L.index(maxim)

print("List L:",L)
print("Elements divisible by 3 in L:",LP)
print("\nThe maximum is",maxim,"and appears at position",index)

# all positions of occurrence of an element in a list
t=[1,2,3,4,1,2,3,4,1,2,3,4,3,2,1]
toate_poz=[i for i, j in enumerate(t) if j == 3]
# i = position in t, j = value
print("\n3 appears in the list",t)
print("at positions:",toate_poz)

# generating a set of values of the form -1, -1+eps, -1+2*eps, ..., 1
eps=0.1
L1=[-1+i*eps for i in range(10000) if -1+i*eps<=1]
print("\nValues in [-1,1] with step 0.1", L1)

# alternatively, using numpy
import numpy
L2=numpy.arange(-1,1+0.1,0.1)
print("\nValues in [-1,1] with step 0.1", L2)

# computing the dot product between 2 randomly generated lists
# the lists have 10 elements each, each element in {-2,3,7,2.5}
import random
l1=[random.choice([-2,3,7,2.5]) for _ in range(10)]
l2=[random.choice([-2,3,7,2.5]) for _ in range(10)]
dot_prod=sum(x*y for x,y in zip(l1,l2))
print(f"\n\nThe dot product between {l1} and {l2} is {dot_prod:.3f}")
