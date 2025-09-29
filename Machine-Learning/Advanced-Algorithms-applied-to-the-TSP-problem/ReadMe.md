# Trois algorithmes de Machine Learning appliqués au problème du N-Puzzle et du Voyageur de commerce (Travelling Salesman Problem)

## Cadre

Ce projet a été réalisé en 2025 en 1ère année de master de sécurité informatique à l'Université de Limoges dans le cadre de l'UE IA avancée encadrée par Mr Karim TAMINE. 

## Contributeurs 

- Anaïs ESPICIER : algorithmes génétique + colonnie de fourmis appliqués au problème du voyageur de commerce
- Noah STAPLE : algorithme A* + BFS appliqués au N-Puzzle, colonnie de fourmis appliqué au TSP

## Description

L'objectif de ce projet était de mettre en pratique les connaissances théoriques acquises au cours du semestre sur la recherche d'états, les différente heuristiques et optimisations dans le cadre de problème réputés difficiles bien connus : 
- le N-puzzle : C’est un jeu de tuiles numérotées disposées dans une grille de taille N×N, avec une case vide (souvent représentée par un 0 ou _) qu’on peut déplacer en échangeant avec une tuile voisine. L'objectif est d'obtenir une configuration cible (ici les tuiles rangées dans l'ordre croissant de gauche à droite) à partir d'un état de départ aléatoire, en déplaçant les tuiles une par une.
- le Voyageur de commerce : C'est un problème NP-Complet défini ainsi : Un voyageur doit visiter une liste de villes exactement une fois chacune, puis revenir à son point de départ, en minimisant la distance totale parcourue (ou le coût, le temps, etc.). Cela revient à cherche un cycle hamiltonien de poids minimal dans un graphe pondéré complet.

Pour le N-puzzle, nous utiliserons les algorithmes **Best First Search** et **A étoile**. Pour le TSP, nous utiliserons l'**algorithme génétique** et l'algorithme de **colonnie de fourmis**. Le détail des algorithmes et le fonctionnement du code sont décrits dans le rapport de projet ci-dessus.
