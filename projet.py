from flask import Flask, render_template, url_for

app = Flask(__name__)


#Initialisation de la base de donnees
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, User, Tournaments

engine = create_engine('sqlite:///tournament.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
#Fin de l'initialisation de la base de donnees


@app.route ('/')
@app.route ('/home')
def Home():	
	return render_template('home.html')


@app.route ('/tournois/<int:tournament_id>/')
def tournois(tournament_id):
	tournois = session.query(Tournaments).filter_by(id=tournament_id).one()
	output = tournois.tournamentName
	output += '<br>'
	output += tournois.gameSystem
	output += '<br>'
	output += tournois.postCode
	output += '<br>'
	output += tournois.city
	output += '<br>'
	output += tournois.startDate
	output += '<br>'
	return output


@app.route("/description")
def about():
    return render_template('about.html', title='Description')

@app.route("/nav")
def navigation():
    return render_template('nav.html', title='Navigation')

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)