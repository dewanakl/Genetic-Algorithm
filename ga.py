import os
import random


# OK representasi genetika
def createGen(target):
    return ''.join([chr(random.randint(32, 126)) for o in range(len(target))])


# OK fitness
def calculateFitness(gen, target):
    fitness = 0
    for i in range(len(target)):
        if (gen[i] == target[i]):
            fitness += 1
    return (fitness / len(target)) * 100


# OK populasi
def createPopulation(target, besarPopulasi):
    populasi = dict()
    for i in range(besarPopulasi):
        temp = dict()
        gen = createGen(target)
        temp['gen'] = gen
        temp['fitness'] = calculateFitness(gen, target)
        populasi[str(i+1)] = temp
    return populasi


# OK seleksi
def selection(populasi):
    result1 = dict()
    result2 = dict()
    arryGen = []
    arryFitness = []

    for i in populasi:
        arryFitness.append(float(populasi[i]['fitness']))
        arryGen.append(populasi[i]['gen'])

    indexparent1 = arryFitness.index(max(arryFitness))
    result1['gen'] = arryGen[indexparent1]
    result1['fitness'] = arryFitness[indexparent1]

    arryFitness[indexparent1] = 0.0
    indexparent2 = arryFitness.index(max(arryFitness))
    if (indexparent1 == indexparent2):
        indexparent2 += 1

    result2['gen'] = arryGen[indexparent2]
    result2['fitness'] = arryFitness[indexparent2]

    return result1, result2


# OK crossover
def crossOver(parent1, parent2, point):
    p1, p2 = list(parent1), list(parent2)
    for i in range(point, len(p1)):
        p1[i], p2[i] = p2[i], p1[i]
    return ''.join(p1), ''.join(p2)


# OK mutasi
def mutation(child, lajuMutasi):
    mutant = list(child)
    for i in range(len(mutant)):
        if random.uniform(0.0, 1.0) <= lajuMutasi:
            mutant[i] = chr(random.randint(32, 126))
    return ''.join(mutant)


# OK regenerasi
def regeneration(children, oldPopulasi):
    newPopulasi = dict()
    templist = []

    for i in range(len(oldPopulasi)):
        temp = []
        temp.append(oldPopulasi[str(i+1)]['gen'])
        temp.append(oldPopulasi[str(i+1)]['fitness'])
        templist.append(temp)

    templist.sort(key=lambda x: x[1])

    for j in range(len(templist)):
        tempd = dict()
        tempd['gen'] = templist[j][0]
        tempd['fitness'] = templist[j][1]
        newPopulasi[str(j+1)] = tempd

    for k in range(len(children)):
        newPopulasi[str(k+1)] = children[k]

    return newPopulasi


# OK stop
def termination(populasi):
    best, none = selection(populasi)
    if (int(best['fitness']) == 100):
        isLoop = False
    else:
        isLoop = True
    return best['gen'], isLoop


# OK hasil
def logging(populasi, target, solusi, generasi):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Target  :", target, "\n")
    print("Solusi  :", solusi)
    print("Generasi:", generasi, "\n")
    for i in range(len(populasi)):
        gen = populasi[str(i+1)]['gen']
        fitness = populasi[str(i+1)]['fitness']
        print("Gen :", gen, "| Fitness :", fitness)


# Main
if __name__ == "__main__":

    target = str(input('Target   : '))
    besarPopulasi = int(input('Populasi : '))
    lajuMutasi = float(input('Mutasi   : '))

    populasi = createPopulation(target, besarPopulasi)
    isLoop = True
    generasi = 0

    while isLoop:
        # individu terbaik / seleksi
        parent1, parent2 = selection(populasi)

        # crossover
        # cp = round(len(parent1['gen'])/2)  # -> fixed
        cp = random.randint(1, len(parent1['gen']))  # -> random
        child1, child2 = crossOver(parent1['gen'], parent2['gen'], cp)

        # mutasi
        mutasi1 = dict()
        mutasi2 = dict()
        result1 = mutation(child1, lajuMutasi)
        result2 = mutation(child2, lajuMutasi)
        mutasi1['gen'] = result1
        mutasi2['gen'] = result2
        mutasi1['fitness'] = calculateFitness(result1, target)
        mutasi2['fitness'] = calculateFitness(result2, target)

        # calon anggota / regenerasi
        children = [mutasi1, mutasi2]
        populasi = regeneration(children, populasi)

        # show
        generasi += 1
        best, isLoop = termination(populasi)
        logging(populasi, target, best, generasi)

    input("\nFinished")
