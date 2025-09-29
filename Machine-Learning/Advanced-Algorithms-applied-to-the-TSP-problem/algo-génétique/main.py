import random

population_size = 20
cycles = 50
esperance_vie = 5
croisement = 6
mutations = 3
max_value = 100
target = 50


def fitness(individual, target):
    return abs(individual[0] - target)

def somme_fitness(fitness_list):
    return sum(fitness_list)

def random_choice(fitness_list, inversed = False):
    somme_fitness_list = somme_fitness(fitness_list)
    if inversed:
        fitness_list = [somme_fitness_list - a for a in fitness_list]
        somme_fitness_list = somme_fitness(fitness_list)
    rand = random.random()
    somme = 0
    for i in range(len(fitness_list)):
        somme += fitness_list[i] / somme_fitness_list
        print(somme,fitness_list[i], rand, "rand")
        if somme >= rand:
            return i

def main ():
    # Initialisation de la population avec (valeur, âge)
    population = [(random.randint(0, max_value), 0) for _ in range(population_size)]

    print("Initial population:", population)

    for cycle in range(cycles):
        print(f"Cycle {cycle}:")

        # Croisement
        new_population = population[:]

        new_population = [(ind[0], ind[1] + 1) for ind in new_population]

        fitness_list = [fitness(individual, target) for individual in population]

        for _ in range(croisement):
            parent1 = new_population[random_choice(fitness_list, True)][0]
            parent2 = new_population[random_choice(fitness_list, True)][0]
            print("Parents:", parent1, parent2)
            offspring = int((parent1 + parent2) / 2)
            new_population.append((offspring, 0))  # Nouveau né avec âge 0
            fitness_list.append(fitness(new_population[-1], target))

        # Mutations
        for _ in range(mutations):
            index = random.randint(0, len(new_population) - 1)
            new_population[index] = (random.randint(0, max_value), new_population[index][1])
            fitness_list[index] = fitness(new_population[index], target)

        # Mort des individus trop vieux

        for i in range(len(new_population) - 1, -1, -1):
            if new_population[i][1] > esperance_vie:
                new_population.pop(i)
                fitness_list.pop(i)

        # Réduction de la population à la taille initiale

        while len(new_population) > population_size:
            rand = random_choice(fitness_list)
            new_population.pop(rand)
            fitness_list.pop(rand)


        population = new_population

        print("Population:", population)
        print("Fitness:", fitness_list)

        # Vérification d'une solution
        for individual in population:

            if fitness(individual, target) == 0:
                print("Solution found:", individual)
                return

    print("Final population:", population)

main()