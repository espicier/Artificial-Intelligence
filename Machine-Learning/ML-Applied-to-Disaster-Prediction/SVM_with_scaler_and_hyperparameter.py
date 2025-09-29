import pandas as pd
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

# Ouvre le fichier et le nettoie
train_df = pd.read_csv('train.csv')
train_df = nettoyage(train_df)

# Prépare les données pour le modèle sklearn.svm
X = train_df[['PassengerId', 'Sex', 'Pclass', 'Age', 'Fare', 'Embarked',
              'Parch', 'SibSp']]
y = train_df['Survived']

# Le scaler permet de normer l'ensemble des données sur [0, 1]
std_scaler = StandardScaler()
X = std_scaler.fit_transform(X)

# Le classifieur inclut cette fois un paramètre C permettant d'ajuster les
# violations de marge dans le set d'entrainement et d'eviter l'hyperfitting
classifieur_SVM = SVC(kernel='poly', C=0.7)
classifieur_SVM.fit(X, y)

# Joint les tableaux de test (données et résultat) pour le nettoyage
test_df = pd.read_csv('test.csv')
alive_df = pd.read_csv('gender_submission.csv')
test_with_result = test_df.merge(alive_df, how='timer', on='PassengerId')

# Applique la fonction de nettoyage
test_with_result = nettoyage(test_with_result)

# Prépare les données pour le modèle sklearn.svm
test_final = test_with_result[['PassengerId', 'Sex', 'Pclass', 'Age', 'Fare', 'Embarked',
                               'Parch', 'SibSp']]
test_final = std_scaler.transform(test_final)
survived_final = test_with_result['Survived']

#Applique le predict du module sklearn.svm aux données test
prediction = classifieur_SVM.predict(test_final)

# Crée un tableau comparant les prédictions et les valeurs réelles
compare = pd.DataFrame({'Prediction' : prediction, 'Actual' : survived_final})
compare['Score'] = compare['Prediction'] + compare['Actual']
num_fail = compare['Score'].value_counts()[1]