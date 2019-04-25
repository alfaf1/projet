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
def Tournois(tournament_id):
	tournois = session.query(Tournaments).filter_by(id=tournament_id).one()
	return render_template('tournois.html', tournois=tournois)


@app.route("/description")
def Description():
    return render_template('description.html', title='Description')


@app.route("/about")
def About():
    return render_template('about.html', title='About')


@app.route("/navigation")
def Navigation():
    return render_template('navigation.html', title='Navigation')

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)