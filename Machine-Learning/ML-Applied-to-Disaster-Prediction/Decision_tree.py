from sklearn.model_selection import train_test_split
from sklearn import tree
import pandas as pd
import numpy as np
from pandas import read_csv
import graphviz

data = read_csv('../titanic/train.csv')

data = data.drop(["Cabin","Name","PassengerId","Ticket"],axis=1)

data["Age"] = data["Age"].fillna(round(data["Age"].mean()))

data.at[829, "Embarked"] = 'S'
data.at[61, "Embarked"] = 'S'

data = pd.get_dummies(data, drop_first=True)

# colonne utilisée pour la prédiction
X = data.drop("Survived", axis=1) # on sélectionne la colonne (axis = 1) 'Survived'

y = data["Survived"] # colonne que l'on veut prédire

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42) #25% du volume total de 
# données seront utilisées en test, random_state = générateur de nbs aléatoires de seed égale à 42 pour mélanger
# données avant d'appliquer l'algorithme

dtm = tree.DecisionTreeClassifier(criterion='gini', splitter='best',max_depth=None, min_samples_split=2, min_samples_leaf=1, random_state=42)

dtm.fit(X_train, y_train)

tree.plot_tree(dtm)

with open("dtm.dot", 'w') as f:
    f = tree.export_graphviz(dtm, out_file=f, filled=True)

