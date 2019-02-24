# coding: utf-8

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

fichier = "articleDevoir.csv"

p = ["No. d'article", "Titre", "section",  "Date de publication", "Texte", "URL"]

henri = open(fichier,"a")

bourassa = csv.writer(henri)

bourassa.writerow(p)

df = pd.read_csv("pays.csv")

for i in range(339458, 548559):

	#création d'une liste vide pour contenir les variables

	s = []

	url = "http://m.ledevoir.com/article-" + str(i)

	contenu = requests.get(url, headers = entete)

	condition = contenu.status_code

	#Cette condition permet d'aller chercher uniquement les fichiers existants

	if condition < 400:

		page = BeautifulSoup(contenu.text.encode("utf-8").decode("utf-8"), "html.parser")

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

		#Cette partie teste tous les noms de pays dans la liste mots, si un article contient un nom de pays, le code ajoute +1 au nom du pays

		print("Les pays dont le nom est contenu dans l'article sont: ")

		for i,x in enumerate(df["PAYS"]):

			country = texte.count(x)
	
			if country > 0:

				print(x)

				df.iat[i, 1] += country

				print("Nombre d'occurence: " + str(country))

				print("-" * 80)
		
				df.to_csv("pays.csv", index=False)

			


