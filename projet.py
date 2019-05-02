from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a39938273acbdcd3fbd1e96a1b9efb36'

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

@app.route("/listeTournois")
def ListeTournois():
	tournaments = session.query(Tournaments).all()
	output = '<table border=3><tr><th>Start date</th><th>Nom</th><th>game System</th><th>city</th></tr>'
	for tourn in tournaments:
		output += '<tr><td>'
		output += tourn.startDate
		output += '</td><td>'
		output += tourn.tournamentName
		output += '</td><td>'
		output += tourn.gameSystem
		output += '</td><td>'
		output += tourn.city
		output += '</td><td>'
		output += str(tourn.id)  #str pour convertion de int vers string
		output += '</td></tr>'
	output+='table'
	#return render_template('listeTournois.html', title='Liste des tournois', output=output)
	return output



@app.route("/navigation")
def Navigation():
    return render_template('navigation.html', title='Navigation')

@app.route("/nav")
def Nav():
    return render_template('nav.html', title='Navigation')

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
			flash('You have been logged in!', 'success')
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check your username and your password', 'danger')
	return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
