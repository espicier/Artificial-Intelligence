from graphe import Graphe
from arete import best_path
import random
import time

test_city = {
    0: {1: 278, 2: 250, 3: 72, 4: 96},
    1: {0: 278, 2: 162, 3: 270, 4: 132},
    2: {0: 250, 1: 162, 3: 450, 4: 64},
    3: {0: 72, 1: 270, 2: 450, 4: 186},
    4: {0: 96, 1: 132, 2: 64, 3: 186}
}

test_big_city = {
    0: {1: 470, 2: 149, 3: 362, 4: 398, 5: 60, 6: 417, 7: 316, 8: 139, 9: 289, 10: 117, 11: 439, 12: 248, 13: 169, 14: 74, 15: 146, 16: 177, 17: 144, 18: 364, 19: 337},
    1: {0: 470, 2: 254, 3: 407, 4: 120, 5: 133, 6: 488, 7: 489, 8: 167, 9: 95, 10: 193, 11: 316, 12: 445, 13: 297, 14: 445, 15: 373, 16: 363, 17: 481, 18: 202, 19: 225},
    2: {0: 149, 1: 254, 3: 439, 4: 101, 5: 291, 6: 191, 7: 454, 8: 343, 9: 335, 10: 221, 11: 428, 12: 210, 13: 164, 14: 448, 15: 257, 16: 71, 17: 398, 18: 384, 19: 407},
    3: {0: 362, 1: 407, 2: 439, 4: 224, 5: 262, 6: 326, 7: 248, 8: 470, 9: 60, 10: 106, 11: 270, 12: 304, 13: 220, 14: 221, 15: 248, 16: 289, 17: 207, 18: 65, 19: 359},
    4: {0: 398, 1: 120, 2: 101, 3: 224, 5: 140, 6: 239, 7: 385, 8: 464, 9: 84, 10: 229, 11: 142, 12: 134, 13: 83, 14: 491, 15: 493, 16: 94, 17: 364, 18: 285, 19: 171},
    5: {0: 60, 1: 133, 2: 291, 3: 262, 4: 140, 6: 242, 7: 215, 8: 439, 9: 88, 10: 238, 11: 148, 12: 199, 13: 475, 14: 293, 15: 185, 16: 476, 17: 365, 18: 211, 19: 118},
    6: {0: 417, 1: 488, 2: 191, 3: 326, 4: 239, 5: 242, 7: 202, 8: 240, 9: 486, 10: 274, 11: 334, 12: 213, 13: 126, 14: 495, 15: 347, 16: 429, 17: 160, 18: 64, 19: 76},
    7: {0: 316, 1: 489, 2: 454, 3: 248, 4: 385, 5: 215, 6: 202, 8: 279, 9: 299, 10: 320, 11: 420, 12: 471, 13: 348, 14: 160, 15: 189, 16: 349, 17: 459, 18: 340, 19: 61},
    8: {0: 139, 1: 167, 2: 343, 3: 470, 4: 464, 5: 439, 6: 240, 7: 279, 9: 165, 10: 322, 11: 111, 12: 316, 13: 354, 14: 492, 15: 277, 16: 290, 17: 453, 18: 84, 19: 472},
    9: {0: 289, 1: 95, 2: 335, 3: 60, 4: 84, 5: 88, 6: 486, 7: 299, 8: 165, 10: 262, 11: 308, 12: 493, 13: 163, 14: 178, 15: 132, 16: 287, 17: 403, 18: 113, 19: 191},
    10: {0: 117, 1: 193, 2: 221, 3: 106, 4: 229, 5: 238, 6: 274, 7: 320, 8: 322, 9: 262, 11: 319, 12: 465, 13: 123, 14: 166, 15: 122, 16: 304, 17: 493, 18: 65, 19: 387},
    11: {0: 439, 1: 316, 2: 428, 3: 270, 4: 142, 5: 148, 6: 334, 7: 420, 8: 111, 9: 308, 10: 319, 12: 69, 13: 141, 14: 138, 15: 268, 16: 71, 17: 466, 18: 308, 19: 132},
    12: {0: 248, 1: 445, 2: 210, 3: 304, 4: 134, 5: 199, 6: 213, 7: 471, 8: 316, 9: 493, 10: 465, 11: 69, 13: 354, 14: 454, 15: 353, 16: 129, 17: 293, 18: 318, 19: 109},
    13: {0: 169, 1: 297, 2: 164, 3: 220, 4: 83, 5: 475, 6: 126, 7: 348, 8: 354, 9: 163, 10: 123, 11: 141, 12: 354, 14: 160, 15: 402, 16: 222, 17: 417, 18: 142, 19: 430},
    14: {0: 74, 1: 445, 2: 448, 3: 221, 4: 491, 5: 293, 6: 495, 7: 160, 8: 492, 9: 178, 10: 166, 11: 138, 12: 454, 13: 160, 15: 413, 16: 174, 17: 413, 18: 272, 19: 250},
    15: {0: 146, 1: 373, 2: 257, 3: 248, 4: 493, 5: 185, 6: 347, 7: 189, 8: 277, 9: 132, 10: 122, 11: 268, 12: 353, 13: 402, 14: 413, 16: 181, 17: 486, 18: 244, 19: 374},
    16: {0: 177, 1: 363, 2: 71, 3: 289, 4: 94, 5: 476, 6: 429, 7: 349, 8: 290, 9: 287, 10: 304, 11: 71, 12: 129, 13: 222, 14: 174, 15: 181, 17: 265, 18: 352, 19: 469},
    17: {0: 144, 1: 481, 2: 398, 3: 207, 4: 364, 5: 365, 6: 160, 7: 459, 8: 453, 9: 403, 10: 493, 11: 466, 12: 293, 13: 417, 14: 413, 15: 486, 16: 265, 18: 195, 19: 306},
    18: {0: 364, 1: 202, 2: 384, 3: 65, 4: 285, 5: 211, 6: 64, 7: 340, 8: 84, 9: 113, 10: 65, 11: 308, 12: 318, 13: 142, 14: 272, 15: 244, 16: 352, 17: 195, 19: 218},
    19: {0: 337, 1: 225, 2: 407, 3: 359, 4: 171, 5: 118, 6: 76, 7: 61, 8: 472, 9: 191, 10: 387, 11: 132, 12: 109, 13: 430, 14: 250, 15: 374, 16: 469, 17: 306, 18: 218}
}


class AlgoGenetique:

    def __init__(self, graphe, nb_gen, size, mut, crois):
        self.distances = {}
        self.graphe = graphe
        self.taille_population = size
        self.nb_generations = nb_gen
        self.alpha = mut
        self.actual_pop_size = size
        self.nb_croisement = crois

        self.population = self.generate_population()

        for _ in range(self.nb_generations):
            self.generation()

    #effectue un croisement entre deux parents et les ajoute à la population
    def generation(self):
        child = []
        for _ in range(self.nb_croisement):
            population_tmp = self.population
            parent1 = self.selection(population_tmp,True)
            p1_indiv = population_tmp[parent1]
            population_tmp.pop(parent1)
            parent2 = self.selection(population_tmp, True)
            p2_indiv = population_tmp[parent2]
            child.append(self.croisement(p1_indiv,p2_indiv))

        for i in child:
            if random.random() <= self.alpha:
                self.mutation(i)
            self.population.append(i)

        while self.taille_population < len(self.population):
            self.population.pop(self.selection(self.population))

    #retourne la distance du chemin le plus court
    def shortest_path(self):
        mini = 1000000
        min_indiv = None
        for indiv in self.population:
            tmp = self.distance_individu(indiv)
            if tmp < mini:
                mini = tmp
                min_indiv = indiv
        print("plus court circuit hamiltonien : coût = " + str(mini) + " et chemin : " + str(min_indiv))
        return mini

    def croisement(self, parent1, parent2):
        stack = []
        child = []

        for i in range(len(parent1)):
            if (random.random() < 0.5 or parent2[i] in child) and parent1[i] not in child:
                child.append(parent1[i])
                if parent2[i] not in child and parent2[i] not in stack:
                    stack.append(parent2[i])
            elif parent2[i] not in child:
                child.append(parent2[i])
                if parent1[i] not in child and parent1[i] not in stack:
                    stack.append(parent1[i])
            else:
                while len(child) != i+1:
                    st = stack.pop()
                    if st not in child:
                        child.append(st)
        return child

    #retourne la somme des distances de chaque individu
    def somme_distances(self):
        somme = 0
        for individu in self.population:
            somme += self.distance_individu(individu)
        return somme

    #retourne un individu "random" influencé par sa proximité avec le chemin le plus court
    def selection(self, population, inversed = False):
        somme = self.somme_distances()

        #utilisé seulement si inversé
        distances_inv = []
        somme_inv = 0

        if inversed:
            for individu in population:
                distances_inv.append(somme - self.distance_individu([tuple(individu)]))
                somme_inv += distances_inv[-1]

        rand = random.random()
        somme_proba = 0
        for i in range(len(population)):
            if inversed:
                somme_proba += distances_inv[i]/somme_inv
            else:
                somme_proba += self.distance_individu([population[i]]/somme)

            if somme_proba >= rand:
                return i

    def mutation(self, individu):
        #print(individu, "avant")
        indice1 = random.randint(0,len(individu)-1)
        indice2 = random.randint(0,len(individu)-1)
        while indice1 == indice2:
            indice2 = random.randint(0,len(individu)-1)
        tmp = individu[indice1]
        individu[indice1] = individu[indice2]
        individu[indice2] = tmp
        return individu

    def generate_population(self):
        population = []
        for _ in range(self.actual_pop_size):
            individu = list(range(self.graphe.nombre_ville)) # individu = chemin hamiltonien aléatoire
            random.shuffle(individu)
            population.append(individu)
            self.distances[tuple(individu)] = self.distance_individu(individu)  # Stockage en tuple
        return population

    def distance_individu(self, individu):
        distance = 0
        if tuple(individu) in self.distances:
            return self.distances[tuple(individu)]
        for i in range(len(individu) - 1):
            distance += self.graphe.villes[individu[i]][individu[i + 1]]
        self.distances[tuple(individu)] = distance
        return distance

    def print_population(self):
        for individu in self.population:
            print(individu, self.distance_individu(individu))



nb_generations = 100
taille_population = 100
taux_mutation = 0.3
nb_crois = 3
graphe1 = Graphe(5, test_city)
graphe2 = Graphe(19, test_big_city)

algo_genetique1 = AlgoGenetique(graphe1, nb_generations, taille_population, taux_mutation, nb_crois)
start = time.perf_counter()
for i in range(algo_genetique1.nb_generations):
    algo_genetique1.generation()
end = time.perf_counter()
time_exec1 = end - start

algo_genetique2 = AlgoGenetique(graphe2, nb_generations, taille_population, taux_mutation, nb_crois)
start = time.perf_counter()
for i in range(algo_genetique2.nb_generations):
    algo_genetique2.generation()
end = time.perf_counter()
time_exec2 = end - start

print("=== Résumé Moyen ===")
print("                         |  path  |  nodes  |  temps (s)")
print(f"Algorithme génétique ->   {algo_genetique1.shortest_path()}| {len(test_city)} | {time_exec1} sec")
print(f"Algorithme génétique ->   {algo_genetique2.shortest_path()}| {len(test_big_city)} | {time_exec2} sec")
print(f"Best First Search ->   {best_path(test_city)[1]} | {len(test_city)} | {best_path(test_city)[2]}   ")
print(f"Best First Search ->   {best_path(test_big_city)[1]} | {len(test_big_city)} | {best_path(test_big_city)[2]}   ")