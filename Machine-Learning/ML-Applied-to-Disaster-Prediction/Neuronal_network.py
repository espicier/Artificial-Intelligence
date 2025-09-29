#Importation de la bibliothèque pandas pour gérer le jeu de données
import pandas as pd

#Importation de StandardScaler de la bibliothèque sklearn afin d'harmoniser le jeu de données
from sklearn.preprocessing import StandardScaler

#Importation des classes models et layers de la bibbliothèque keras afin d'instancier le réseau de neurones
from keras import models                                                                       
from keras import layers

def train():
  global model
  training_data = pd.read_csv("\\".join(__file__.split("\\")[:-1])+"\\"+"train.csv")
  training_data=training_data.drop("Cabin", axis=1)
  training_data ["Age"] = training_data ["Age"].fillna (round (training_data ["Age"].mean()))
  training_data.at [829, "Embarked"] = "S"; training_data.at [61, "Embarked"] = "S"
  training_data=training_data.drop(["Name", "PassengerId", "Ticket"], axis=1)
  training_data.replace({'Sex':{'male':0, 'female':1}, 'Embarked':{'S':0,'Q':1,'C':2}}, inplace=True)

  #Crée une variable contenant toutes les colonnes servant au réseau de neurones
  X = training_data[training_data.columns.drop(['Survived'])]

  #Crée une variable contenant uniquement les valeurs de survie des passagers
  Y = training_data['Survived']

  #Mise à l'échelle du jeu de données afin d'améliorer les performances du réseau de neurones
  X = pd.DataFrame(StandardScaler().fit_transform(X), columns=X.columns)

  #Création d'un modèle de réseau de neurones
  model = models.Sequential()

  #Ajout des neurones par couches
  #Première couche : 7 neurones d'entrée, 21 neurones de calcul connectés aux 7 d'entrée
  model.add(layers.Dense(21, input_dim=7, activation='relu'))
  #Deuxième couche : 10 neurones de calcul interconnectés aux 21 précédentes
  model.add(layers.Dense(10, activation='relu'))
  #Troisième et dernière couche : 1 neurone de sortie (fonction d'activation renvoyant 0 ou 1)
  model.add(layers.Dense(1, activation='sigmoid'))

  #Compilation du modèle selon les données renseignées
  model.compile(loss='binary_crossentropy', optimizer='adam',metrics=['accuracy', 'mse'])

  #Entraînement du modèle, sur 5000 répétitions, par lots de 32 individus
  history=model.fit(X, Y, epochs=5000, batch_size=32)

def is_float(element: any):
    try:
        float(element)
        return True
    except ValueError:
        return False

def test():
  global model
  i1=None
  while i1 not in ['1','2','3']:
    i1=input("Classe du passager (1, 2 ou 3) : ")
  i2=None
  while i2 not in ['M', 'F']:
    i2=input("Sexe du passager (M = Masculin, F = Féminin)  : ")
  i2=['M', 'F'].index(i2)
  i3=''
  while not is_float(i3):
    i3=input("Âge du passager (en chiffres) : ") 
  i4=''
  while not i4.isdigit():
    i4=input("Nombre d'épouse, de frères ou sœurs du passager (entier) : ")
  i5=''
  while not i5.isdigit():
    i5=input("Nombre d'enfants ou de parents du passager (entier) : ")
  i6=''
  while not is_float(i6):
    i6=input("Tarif du billet du passager (en chiffres) : ")
  i7=None
  while i7 not in ['S', 'Q', 'C']:
    i7=input("Port d'embarquement (C = Cherbourg, Q = Queenstown, S = Southampton) du passager : ")
  i7=['S', 'Q', 'C'].index(i7)

  dict={"Pclass":int(i1), "Sex":int(i2), "Age":float(i3), "SibSp":int(i4), "Parch":int(i5), "Fare":float(i6), "Embarked":int(i7)}
  data=pd.DataFrame(dict, index=[0])
  if(round(model.predict(data)[0][0]))==1:
    print("Le passager a survécu !")
  else:
    print("Le passager est décédé !")

train()
test()