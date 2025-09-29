import pandas as pd

# nettoyage des données :
# - lignes où âge non spécifié : assigner moyenne de l'âge des passagers
# - transformer chaînes de caractères en chiffres interprétables par les algo

def nettoyage(nom_fichier : str): # fichier csv devant se trouver dans le repo courant
    # importation du jeu de données
    df = pd.read_csv(nom_fichier)

    # suppression de la colonne cabine
    df = df.drop("Cabin", axis=1)

    # remplissage de la colonne Age avec l'âge moyen des passagers
    df["Age"] = df["Age"].fillna(round(df["Age"].mean()))

    # Ajout du port d'embarquement manquant pour les 2 passagers
    df.at[829,"Embarked"] = "S"
    df.at[61,"Embarked"] = "S"

    # Suppression des colonnes Name, PassengerId, Ticket qui ne nous intéressent pas
    df = df.drop(["Name", "PassengerId", "Ticket"], axis=1)

    # Conversion des chaînes de caractères en valeurs booléennes
    df = pd.get_dummies(df, drop_first=True)


