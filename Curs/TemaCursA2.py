import random

buget_max=5000

costuri=[100,60,50]
autonomii=[6000,4200,2800]
vizibilitati=[1500,2400,1600]

dim_pop=50
generatii=100
rata_mutatie=0.1

def fitness(individ):
    a,b,c=individ
    cost_total=a*costuri[0]+b*costuri[1]+c*costuri[2]
    total_avioane=a+b+c

    if total_avioane==0:
        return 0
    if cost_total>buget_max:
        return 0

    autonomie_medie = (a * autonomii[0] + b * autonomii[1] + c * autonomii[2]) / total_avioane
    vizibilitate_medie = (a * vizibilitati[0] + b * vizibilitati[1] + c * vizibilitati[2]) / total_avioane

    if vizibilitate_medie <=2000:
        return 0

    return autonomie_medie

def individ_random():
    return [
        random.randint(0,50),
        random.randint(0,50),
        random.randint(0,50)
    ]

def crossover(p1,p2):
    punct=random.randint(1,2)
    copil=p1[:punct]+p2[punct:]
    return copil

def mutatie(individ):
    if random.random()<rata_mutatie:
        pozitie=random.randint(0,2)
        individ[pozitie]=random.randint(0,50)
    return individ

populatie=[ individ_random() for _ in range(dim_pop) ]

for generatie in range(generatii):
    populatie.sort(key=lambda x:fitness(x),reverse=True)

    populatie_noua=populatie[:10]

    while len(populatie_noua)<dim_pop:
        p1=random.choice(populatie[:20])
        p2=random.choice(populatie[:20])

        copil=crossover(p1,p2)
        copil=mutatie(copil)

        populatie_noua.append(copil)
    populatie=populatie_noua

populatie.sort(key=lambda x:fitness(x),reverse=True)
sol=populatie[0]

print("Cea mai buna solutie gasita (EA):")
print("I",sol[0])
print("II",sol[1])
print("III",sol[2])
print("Autonomie medie:",fitness(sol))