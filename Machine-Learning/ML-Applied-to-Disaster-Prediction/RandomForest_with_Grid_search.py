import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Ouvre le fichier et le nettoie
train_df = pd.read_csv('train.csv')
train_df = nettoyage(train_df)

# Colonnes utilisées pour la prédiction
X = df.drop("Survived", axis=1)

# Colonne que l'on veut prédire
y = df["Survived"]

# Séparation des données en échantillons d'entraînement et échantillon de test
train_X, verif_X, train_y, verif_y = train_test_split(X, y, test_size=0.2, random_state=9)

# Création d'un modèle avec une seed
randomForest = RandomForestClassifier(random_state=99)

# Recherche de la meilleur combinaison de paramètres (Grid Search)

# Array allant de 100 -> 1000 avec un pas de 100 (test de 100 à 1000 arbres)
n_estimators = np.arange(100, 1001, 100)

# Test du nombre de dimensions choisies aléatoirement allant de 2 à 6 (7 n'est pas inclus)
max_features = np.arange(2, 7)

# Dictionnaire qui stocke les paramètres à tester
params = {'n_estimators': n_estimators, 'max_features': max_features}

# Création de la grid search avec nos paramètres
most_accurate_model = GridSearchCV(randomForest, param_grid=params)

# Entrainement du meilleur modèle trouvé avec nos données d'entraînement
most_accurate_model.fit(train_X, train_y)

# Prédiction avec le meilleur modèle
predictions = most_accurate_model.predict(verif_X)
