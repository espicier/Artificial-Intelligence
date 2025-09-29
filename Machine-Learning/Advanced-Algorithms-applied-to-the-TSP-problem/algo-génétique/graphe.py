import random

class Graphe :
    def __init__(self, nombre_villes = 5,  villes= None):
        self.nombre_ville = nombre_villes
        self.smallest = 1000000
        self.best_path = []

        if villes is None:
            self.villes = {}
            self.create_villes()
        else:
            self.villes = villes

    def create_villes(self):
        for i in range (self.nombre_ville):
            if i not in self.villes:
                self.villes[i] = {}
            for j in range (self.nombre_ville):
                if i != j and j not in self.villes[i]:
                    distance = random.randint(100, 1000)

                    if j not in self.villes:
                        self.villes[j] = {}

                    self.villes[i][j] = distance
                    self.villes[j][i] = distance

    def print_ville(self):
        for i in range(self.nombre_ville):
            print(f"Ville {i}:")
            for j in range(self.nombre_ville):
                if i != j:
                    print(f"  -> Ville {j}: {self.villes[i][j]} km")

    def chemin_hamiltonien(self):
        for ville in self.villes:
            print(f"Chemin hamiltonien de la ville {ville}:")
            self.hamiltonien(ville, [ville], 0)

    def hamiltonien(self, ville, chemin, distance):
        if len(chemin) == self.nombre_ville:
            print(f"  -> {chemin} : {distance} km")
            if distance < self.smallest:
                self.smallest = distance
                self.best_path = chemin
            return
        for ville_suivante in self.villes[ville]:
            if ville_suivante not in chemin:
                self.hamiltonien(ville_suivante, chemin + [ville_suivante], distance + self.villes[ville][ville_suivante])
