# coding: utf-8

### Excellent script! Bien documenté!

#Ce code permet d'aller chercher tous les articles du Devoir entre le 1er janvier 2012 et le 24 février 2019
#Il permet aussi de compter l'occurence de chaque pays du monde dans les différents articles

import csv
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

entete = {
	"User-Agent":"Thomas Dufour: étudiant en journalisme à l'UQAM",
	"From":"thomasdufour4@gmail.com"
}

### Super! De tout ramasser te permet de faire de nouvelles recherches dans l'ensemble du corpus dans les cas où tu aurais oublié un pays ou territoire...
### comme «Grande-Bretagne» qui, même s'il n'est géographiquement pas synonyme de Royaume-Uni, est souvent considéré comme tel dans des articles.
### Certains pays sont écrits différemment par Le Devoir, comme Vietnam (et non Viêt Nam) -> https://www.ledevoir.com/monde/etats-unis/339597/obama-promet-une-armee-americaine-allegee-mais-toujours-puissante

#Création d'un ficher pour accueillir les articles

fichier = "articleDevoir_jhr.csv"

p = ["No. d'article", "Titre", "section", "Date de publication", "Texte", "URL"]

henri = open(fichier,"a")
bourassa = csv.writer(henri)
bourassa.writerow(p)

### Je vois que tu as recours à Pandas, ici. Très bien!
### Mais explique-nous ce que tu fais, au juste.

df = pd.read_csv("pays.csv")

# for i in range(339458, 548559):
for i in range(339776, 548559): ### Essai d'arrêt et de reprise du script

	#création d'une liste vide pour contenir les variables

	s = []
	url = "http://m.ledevoir.com/article-" + str(i)
	contenu = requests.get(url, headers = entete)
	condition = contenu.status_code

	#Cette condition permet d'aller chercher uniquement les fichiers existants

	if condition < 400:
### Il n'est pas nécessaire de faire un «encode» et un «decode» ici, car c'est de l'UTF-8 partout.
		# page = BeautifulSoup(contenu.text.encode("utf-8").decode("utf-8"), "html.parser")
		page = BeautifulSoup(contenu.text, "html.parser")

		#ce code permet d'aller chercher le titre de l'article
		titre = page.find("title").text.split("|")[0]

		#ce code permet d'aller chercher la date
		date = page.find("time").text

		#ce code permet d'aller chercher le texte
		texte = page.find("div", class_="editor scrolling-tracker").text.replace('\r', '').replace('\n', '').split("#mc")[0]
		texte = " ".join(re.split("\s+", texte, flags=re.UNICODE))

		section = page.find("link")["href"].split("/")[3]

		# cette partie ajoute les éléments à une liste que sera ensuite ajoutée au fichier csv

		s.append(i)
		s.append(titre)
		s.append(section)
		s.append(date)
		s.append(texte)
		s.append(url)

		#Cette partie ajoute les éléments de la liste au fichier csv
		henri = open(fichier,"a")
		bourassa = csv.writer(henri)
		bourassa.writerow(s)

		print("J'ai terminé le fichier numéro " + str(i))

		time.sleep(1)

### Bonne utilisation de pandas qui, effectivement, peut s'avérer plus rapide pour gérer des CSV qu'en python pur.
### Très bonne «mécanique», aussi, pour ajouter les occurrences d'un pays au fur et à mesure dans ton fichier source.
		#Cette partie teste tous les noms de pays, si un article contient un nom de pays, le code ajoute le nombre de fois que ce pays apparait

		print("Les pays dont le nom est contenu dans l'article sont: ")

		for i,x in enumerate(df["PAYS"]):

			country = texte.count(x)

			if country > 0:
				print(x)
				df.iat[i, 1] += country
				print("Nombre d'occurence: " + str(country))
				print("-" * 80)
				df.to_csv("pays.csv", index=False)

### J'ai laissé rouler le script jusqu'à 340111
