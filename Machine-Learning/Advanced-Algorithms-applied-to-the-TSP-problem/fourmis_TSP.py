import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
import random
import seaborn as sns
import time
class Fourmi:
    """
    Représente une fourmi individuelle dans la colonie

    Une fourmi construit une solution en se déplaçant de ville en ville
    en utilisant les informations d'heuristique et de phéromones
    """

    def __init__(self, nombre_villes: int, ville_depart: int = None):
        """
        Initialise une fourmi

        Args:
            nombre_villes: Nombre total de villes à visiter
            ville_depart: Ville de départ (aléatoire si non spécifiée)
        """
        self.nombre_villes = nombre_villes
        self.ville_depart = ville_depart if ville_depart is not None else random.randint(0, nombre_villes - 1)
        self.reset()

    def reset(self):
        self.chemin = [self.ville_depart]
        self.villes_non_visitees = list(range(self.nombre_villes))
        self.villes_non_visitees.remove(self.ville_depart)
        self.distance_totale = 0.0

    def choisir_prochaine_ville(self, matrice_pheromone: np.ndarray, matrice_distance: np.ndarray,
                                alpha: float, beta: float) -> int:
        """
        Sélectionne la prochaine ville à visiter selon la règle de probabilité décrite
        par l'algorithme (https://fr.wikipedia.org/wiki/Algorithme_de_colonies_de_fourmis).

        Args:
            matrice_pheromone: Matrice contenant les niveaux de phéromones entre les villes
            matrice_distance: Matrice contenant les distances entre les villes
            alpha: Paramètre contrôlant l'importance des phéromones
            beta: Paramètre contrôlant l'importance de l'heuristique

        Returns:
            L'indice de la prochaine ville à visiter
        """
        ville_actuelle = self.chemin[-1]

        # calcul des probabilités pour chaque ville non visitée
        probabilites = []

        for ville in self.villes_non_visitees:
            # niveau de phéromone
            tau = matrice_pheromone[ville_actuelle][ville] ** alpha

            # information heuristique (inverse de la distance)
            if matrice_distance[ville_actuelle][ville] == 0:
                eta = 1.0
            else:
                eta = (1.0 / matrice_distance[ville_actuelle][ville]) ** beta

            probabilites.append(tau * eta)

        # normalisation des probabilités
        somme = sum(probabilites)
        if somme == 0:
            # si toutes les probabilités sont nulles, choisir une ville au hasard
            prochaine_ville_index = random.randint(0, len(self.villes_non_visitees) - 1)
            prochaine_ville = self.villes_non_visitees[prochaine_ville_index]
        else:
            probabilites = [p / somme for p in probabilites]

            # sélection de la prochaine ville selon la distribution de probabilité
            cumul = 0
            r = random.random()
            for i, prob in enumerate(probabilites):
                cumul += prob
                if r <= cumul:
                    prochaine_ville = self.villes_non_visitees[i]
                    break

        return prochaine_ville

    def construire_solution(self, matrice_pheromone: np.ndarray, matrice_distance: np.ndarray,
                            alpha: float, beta: float):
        """
        Construit une solution complète (un tour complet des villes)

        Args:
            matrice_pheromone: Matrice contenant les niveaux de phéromones entre les villes
            matrice_distance: Matrice contenant les distances entre les villes
            alpha: Paramètre contrôlant l'importance des phéromones
            beta: Paramètre contrôlant l'importance de l'heuristique
        """
        while self.villes_non_visitees:
            prochaine_ville = self.choisir_prochaine_ville(matrice_pheromone, matrice_distance, alpha, beta)
            self.distance_totale += matrice_distance[self.chemin[-1]][prochaine_ville]

            # ajouter la ville au chemin et la retirer des villes non visitées
            self.chemin.append(prochaine_ville)
            self.villes_non_visitees.remove(prochaine_ville)

        # ajouter la distance de retour à la ville de départ pour compléter le circuit
        self.distance_totale += matrice_distance[self.chemin[-1]][self.chemin[0]]


class ColonieDefourmis:


    def __init__(self, matrice_distance: np.ndarray, nombre_fourmis: int = 10,
                 alpha: float = 1.0, beta: float = 2.0, rho: float = 0.5,
                 q: float = 100, iterations: int = 100):
        """
        Initialise une colonie de fourmis.

        Args:
            matrice_distance: Matrice des distances entre les villes
            nombre_fourmis: Nombre de fourmis dans la colonie
            alpha: Importance des phéromones (alpha ≥ 0)
            beta: Importance de l'heuristique (beta ≥ 1)
            rho: Taux d'évaporation des phéromones (0 < ρ < 1)
            q: Constante pour le dépôt de phéromones
            iterations: Nombre maximal d'itérations
        """
        self.matrice_distance = matrice_distance
        self.nombre_villes = len(matrice_distance)
        self.nombre_fourmis = nombre_fourmis
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q
        self.iterations = iterations

        self.fourmis = [Fourmi(self.nombre_villes) for _ in range(nombre_fourmis)]

        # on initialse les phéromones a 0.5 (comme dans la consigne)
        self.matrice_pheromone = np.ones((self.nombre_villes, self.nombre_villes)) * 0.5

        self.meilleur_chemin = None
        self.meilleure_distance = float('inf')

        self.historique_distances = []

    def executer(self) -> Tuple[List[int], float]:
        """
        Exécute l'algorithme de colonies de fourmis

        Returns:
            Un tuple contenant le meilleur chemin trouvé et sa distance
        """
        t0 = time.perf_counter()
        for iteration in range(self.iterations):
            # réinitialiser les fourmis
            for fourmi in self.fourmis:
                fourmi.reset()

            # construire les solutions
            for fourmi in self.fourmis:
                fourmi.construire_solution(self.matrice_pheromone, self.matrice_distance,
                                           self.alpha, self.beta)

                # mettre à jour la meilleure solution si nécessaire
                if fourmi.distance_totale < self.meilleure_distance:
                    self.meilleure_distance = fourmi.distance_totale
                    self.meilleur_chemin = fourmi.chemin.copy()
            self.historique_distances.append(self.meilleure_distance)
            self.mettre_a_jour_pheromones()
        run_time = time.perf_counter() - t0
        print(f"Temps d'exécution: temps = {run_time:.3f}s")
        return self.meilleur_chemin, self.meilleure_distance

    def mettre_a_jour_pheromones(self):
        """
        Met à jour les niveaux de phéromones sur toutes les arêtes.
        """
        self.matrice_pheromone *= (1 - self.rho)

        # dépôt de phéromones par chaque fourmi
        for fourmi in self.fourmis:
            # calculer la quantité de phéromones à déposer
            delta_tau = self.q / fourmi.distance_totale

            # déposer des phéromones sur le chemin parcouru
            for i in range(len(fourmi.chemin) - 1):
                ville_i = fourmi.chemin[i]
                ville_j = fourmi.chemin[i + 1]
                self.matrice_pheromone[ville_i][ville_j] += delta_tau
                self.matrice_pheromone[ville_j][ville_i] += delta_tau

            # fermer le circuit (retour à la ville de départ)
            ville_debut = fourmi.chemin[0]
            ville_fin = fourmi.chemin[-1]
            self.matrice_pheromone[ville_fin][ville_debut] += delta_tau
            self.matrice_pheromone[ville_debut][ville_fin] += delta_tau




    def afficher_solution(self, coordonnees: List[Tuple[float, float]] = None,
                          afficher: bool = True, sauvegarder: str = None):
        """
        Affiche la meilleure solution trouvée en utilisant seaborn pour afficher le graphe de la solution

        Args:
            coordonnees: Liste des coordonnées (x, y) des villes pour l'affichage graphique
            sauvegarder: Chemin du fichier où sauvegarder le graphique (ex: 'solution_seaborn.png')
        """
        if self.meilleur_chemin is None:
            print("Aucune solution trouvée. Exécutez d'abord l'algorithme.")
            return

        print(f"Meilleur chemin: {self.meilleur_chemin}")
        print(f"Distance totale: {self.meilleure_distance:.2f}")

        # affichage graphique si des coordonnées sont fournies
        if coordonnees:
            sns.set_theme(style="whitegrid")

            plt.figure(figsize=(12, 8))

            x = [coordonnees[i][0] for i in range(self.nombre_villes)]
            y = [coordonnees[i][1] for i in range(self.nombre_villes)]

            ax = sns.scatterplot(x=x, y=y, s=150, color='red', edgecolor='black')

            # on numeérote les villes
            for i in range(self.nombre_villes):
                plt.annotate(str(i), (x[i], y[i]), fontsize=12,
                             xytext=(5, 5), textcoords='offset points')

            chemin_x = []
            chemin_y = []



            for ville in self.meilleur_chemin:
                chemin_x.append(coordonnees[ville][0])
                chemin_y.append(coordonnees[ville][1])

            chemin_x.append(coordonnees[self.meilleur_chemin[0]][0])
            chemin_y.append(coordonnees[self.meilleur_chemin[0]][1])

            sns.lineplot(x=chemin_x, y=chemin_y, sort=False, color='blue',
                         linewidth=2, marker='o', markersize=8, ax=ax)

            start_city = self.meilleur_chemin[0]
            plt.scatter([coordonnees[start_city][0]], [coordonnees[start_city][1]],
                        s=250, color='green', edgecolor='black', zorder=5, label='Départ')

            plt.title('Meilleur chemin trouvé par les fourmis', fontsize=16)
            plt.xlabel('Coordonnée X', fontsize=14)
            plt.ylabel('Coordonnée Y', fontsize=14)
            plt.legend()

            # Amélioration de l'apparence
            ax.grid(True, linestyle='--', alpha=0.7)

            if sauvegarder:
                plt.savefig(sauvegarder, dpi=300, bbox_inches='tight')
                print(f"Solution graphique sauvegardée dans {sauvegarder}")

            if afficher:
                try:
                    plt.show()
                except Exception as e:
                    print(f"Impossible d'afficher le graphique. Erreur: {e}")
                    print("Essayez de sauvegarder le graphique dans un fichier à la place.")

            plt.close()


def creer_probleme_aleatoire(nombre_villes: int) -> Tuple[np.ndarray, List[Tuple[float, float]]]:
    """
    Crée un problème du voyageur de commerce aléatoire

    Args:
        nombre_villes: Nombre de villes dans le problème

    Returns:
        Un tuple contenant la matrice de distance et les coordonnées des villes
    """
    coordonnees = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(nombre_villes)]

    # Calculer la matrice de distance
    matrice_distance = np.zeros((nombre_villes, nombre_villes))
    for i in range(nombre_villes):
        for j in range(nombre_villes):
            if i != j:
                dx = coordonnees[i][0] - coordonnees[j][0]
                dy = coordonnees[i][1] - coordonnees[j][1]
                matrice_distance[i][j] = np.sqrt(dx * dx + dy * dy)

    return matrice_distance, coordonnees


def tester_solution_connue():
    print("\n=== Test sur un problème carré (solution optimale connue) ===")

    # créer un problème carré avec 4 villes
    coordonnees = [(0, 0), (10, 0), (10, 10), (0, 10)]  # carré 10x10

    # Calculer la matrice de distance
    matrice_distance = np.zeros((4, 4))
    for i in range(4):
        for j in range(4):
            if i != j:
                dx = coordonnees[i][0] - coordonnees[j][0]
                dy = coordonnees[i][1] - coordonnees[j][1]
                matrice_distance[i][j] = np.sqrt(dx * dx + dy * dy)

    # la solution optimale est le périmètre du carré: 40
    distance_optimale = 40.0

    # paramètres de l'algorithme
    nombre_fourmis = 20
    alpha = 1.0
    beta = 2.0
    rho = 0.5
    q = 100
    iterations = 100

    colonie = ColonieDefourmis(
        matrice_distance,
        nombre_fourmis,
        alpha,
        beta,
        rho,
        q,
        iterations
    )

    meilleur_chemin, meilleure_distance = colonie.executer()

    # calculer l'erreur relative
    erreur_relative = abs(meilleure_distance - distance_optimale) / distance_optimale

    # afficher les résultats
    print(f"Meilleur chemin trouvé: {meilleur_chemin}")
    print(f"Distance trouvée: {meilleure_distance:.2f}")
    print(f"Distance optimale: {distance_optimale:.2f}")
    print(f"Erreur relative: {erreur_relative:.2%}")

    # vérifier que l'erreur est inférieure à 5%
    tolerance = 0.05
    assert erreur_relative <= tolerance, f"Erreur trop importante: {erreur_relative:.2%} > {tolerance:.0%}"

    print(f"Test réussi! L'erreur ({erreur_relative:.2%}) est dans la limite acceptable ({tolerance:.0%}).")

    return True

def main():
    nombre_villes = 100

    matrice_distance, coordonnees = creer_probleme_aleatoire(nombre_villes)

    print(matrice_distance)
    print(coordonnees)

    # paramètres
    nombre_fourmis = 20
    alpha = 1.0  # importance des phéromones
    beta = 2.0  # importance de l'heuristique (distance)
    rho = 0.5  # taux d'évaporation des phéromones
    q = 100  # constante pour le dépôt de phéromones
    iterations = 100

    colonie = ColonieDefourmis(matrice_distance, nombre_fourmis, alpha, beta, rho, q, iterations)
    meilleur_chemin, meilleure_distance = colonie.executer()

    colonie.afficher_solution(coordonnees, afficher=True, sauvegarder="solution_seaborn.png")
    try:
        tester_solution_connue()
    except AssertionError as e:
        print(f"Fail du test: {str(e)}")


if __name__ == "__main__":
    main()