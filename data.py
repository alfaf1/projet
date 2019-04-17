from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import User, Base, Tournaments


engine = create_engine('sqlite:///tournament.db')

Base.metadata.bind = engine


#Les imports pour la session de la partie 'parse'
DBSession = sessionmaker(bind=engine)
session = DBSession()


#les import beautifulSoup
import os, sys
import csv
import requests
from bs4 import BeautifulSoup


#La recuperation de donnees
requete = requests.get("https://www.tabletoptournaments.net/eu/overview")
page = requete.content
soup = BeautifulSoup(page, "html.parser")

i = 0
j = 0
n = 0

list = []

nb = soup.find_all('a', {'itemprop' : 'name'})
nbElement = len(nb)
print ("nbElement : ",nbElement)

v = 5

"""
La variable v de la boucle while ne sert que de test. A remplacer par 'nbElement qui est bcp plus grand mais plus lent
"""

count = 0
while i<nbElement and j<nbElement*2:

    nomTournois = soup.find_all('a', {'itemprop' : 'name'})[i].text
    list.append(nomTournois)
    titre = soup.find_all('td', {'class' : 'category'})[i].text
    list.append(titre)
    postCode = soup.find_all('span', {'itemprop': 'postalCode'})[i].text
    list.append(postCode)
    locality = soup.find_all('span' , {'itemprop': 'addressLocality'})[i].text
    list.append(locality)
    
    if j%2 :
        
        j += 1
        startDate = soup.find_all('td', {'class' : 'ctr'})[j].text
        list.append(startDate)

    else :
        startDate = soup.find_all('td', {'class' : 'ctr'})[j].text
        list.append(startDate)

    n += 1    
    i += 1
    j += 1
    tournois=Tournaments(tournamentName=list[count], gameSystem=list[count+1], postCode=list[count+2], city=list[count+3], startDate=list[count+4])
    session.add(tournois)
    
    count = count+5

session.commit()

"""
taille = 5
while count < len(list):
    while count < taille:
        tournois=Tournaments(tournamentName=list[count], gameSystem=list[count+1], postCode=list[count+1], city=list[count+1], date=list[count+1])
        session.add(tournois)
        session.commit()
        for i in tournois:
            print(i.tournamentName)
            print(i.gameSystem)
            print(i.postCode)
            print(i.city)
            print(i.date)
            print("-------")
    taille = taille+5
    count += 1
"""

"""
print(nomTournois)
print(titre)
print(postCode)
print(locality)
print ("_____")
"""
    

"""
    
"""

