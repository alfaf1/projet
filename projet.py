from flask import Flask, render_template, request, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a39938273acbdcd3fbd1e96a1b9efb36'

#Initialisation de la base de donnees
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, User, Tournaments


#engine = create_engine('sqlite:///tournament.db')
engine = create_engine('sqlite:///tournament.db?check_same_thread=False')
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
	tournois = session.query(Tournaments).all()
	
	return render_template('listeTournois.html', title='Liste des tournois', tournois=tournois, len = len(tournois))



@app.route("/majlatlong")
def Majlatlong():

	#fonction qui calcule les lat et long de chaque tournoi dans la DB
	#ne devrait pas être accessible par les utilisateurs.
	from geopy.geocoders import Nominatim
	geolocator = Nominatim(user_agent="TabTopProject")


	#borne inferieure et superieure, on le fait en plusieurs fois sinon on obtient un timeout
	#Nominatim ne trouve pas 2 tournois!
	tournaments = session.query(Tournaments).filter(Tournaments.id>=400).filter(Tournaments.id<=444).all()
	
	output = '<table border=3><tr><th>Start date</th><th>Nom</th><th>game System</th><th>city</th><th>id</th><th>latitude</th><th>longitude</th></tr>'
	for tourn in tournaments:
		location = geolocator.geocode(tourn.city)
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
		output += '</td><td>'
		output += str(location.latitude) #str pour convertion de int vers string
		output += '</td><td>'
		output += str(location.longitude) #str pour convertion de int vers string
		output += '</td></tr>'
		tourn.lat = str(location.latitude) 
		tourn.longg = str(location.longitude)
	output+='</table>'
	
	session.commit() #valide les modifications (update sqlalchemy)

	return output
	
@app.route("/choixSystJeu")
def ChoixSystJeu():
	tournaments = session.query(Tournaments.gameSystem).distinct(Tournaments.gameSystem).order_by(Tournaments.gameSystem)
	output = '<form action="/resultats" method="post">'
	#output+= '<input id="prodId" name="prodId" type="hidden" value="xm234jq">' #pour debug
	for tourn in tournaments:
		output += '<input type="checkbox" name="jeux" value="'
		output += tourn.gameSystem
		output += '" id="'
		output += tourn.gameSystem
		output += '"> <label for="'
		output += tourn.gameSystem
		output += '">'
		output += tourn.gameSystem
		output += '</label><br>'
	output += '<div class="button"><button type="submit">Rechercher</button></div>'
	output += '</form>'
	return output


@app.route('/resultats', methods=['POST'])
def ResultatsRecherche():
	if request.method == 'POST':
		if request.form['jeux']:

			strFilter = request.form.getlist('jeux')

			tournois = session.query(Tournaments).filter(Tournaments.gameSystem.in_(strFilter)).all()
			
			return render_template('listeTournois.html', title='Liste des tournois', tournois=tournois, len = len(tournois))


	else: 
		output = 'devrait être impossible'
		return output
	



@app.route('/resultatsOld', methods=['POST'])
def ResultatsRechercheOld():
	if request.method == 'POST':
		if request.form['jeux']:
			output = '<!DOCTYPE html>'
			output = '<html><head>'
			# Code pour pouvoir utiliser Leaflet
			output += '<title>Resultats</title>'
			output += '<meta charset="utf-8" />'
			output += '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
			output += '<link rel="shortcut icon" type="image/x-icon" href="docs/images/favicon.ico" />'
			output += '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.4.0/dist/leaflet.css" integrity="sha512-puBpdR0798OZvTTbP4A8Ix/l+A4dHDD0DGqYW6RQ+9jxkRFclaxxQb/SJAWZfWAkuyeQUytO7+7N4QKrDh+drA==" crossorigin=""/>'
			output += '<script src="https://unpkg.com/leaflet@1.4.0/dist/leaflet.js" integrity="sha512-QVftwZFqvtRNi0ZyCtsznlKSWOStnDORoefr1enyq5mVL4tmKB3S/EnC3rRJcxCPavG10IcrVGSmPh6Qw5lwrg==" crossorigin=""></script>'
			output += '</head>'
			
			output += '<body>'
			
			output += '<div id="mapid" style="width: 600px; height: 400px;"></div>'
			output += '<script>'

			output += "var mymap = L.map('mapid').setView([51.505, -0.09], 13);"

			output += "L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?		access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {"
			output += 'maxZoom: 18,'
			output += 'attribution: \'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, \' +'
			output += "'<a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, ' +"
			output += "'Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>',"
			output += "id: 'mapbox.streets'"
			output += "}).addTo(mymap);"
			output += 'L.marker([51.5, -0.09]).addTo(mymap)'
			output += '.bindPopup("<b>Hello world!</b><br />I am a popup.").openPopup();'
			output += 'L.circle([51.508, -0.11], 500, {'
			output += "color: 'red',"
			output += "fillColor: '#f03',"
			output += 'fillOpacity: 0.5'
			output += '}).addTo(mymap).bindPopup("I am a circle.");'
			output += 'L.polygon(['
			output += '[51.509, -0.08],'
			output += '[51.503, -0.06],'
			output += '[51.51, -0.047]'
			output += ']).addTo(mymap).bindPopup("I am a polygon.");'
			output += 'var popup = L.popup();'

			output += 'function onMapClick(e) {'
			output += 'popup'
			output += '.setLatLng(e.latlng)'
			output += '.setContent("You clicked the map at " + e.latlng.toString())'
			output += '.openOn(mymap);'
			output += '}'
			output += 'mymap.on(\'click\', onMapClick);'
			output += '</script>'

			strFilter = request.form.getlist('jeux')

			tournaments = session.query(Tournaments).filter(Tournaments.gameSystem.in_(strFilter)).all()
			output += '<table border=3><tr><th>Start date</th><th>Nom</th><th>game System</th><th>city</th></tr>'
			for tourn in tournaments:
				output += '<tr><td>'
				output += tourn.startDate
				output += '</td><td>'
				output += '<a href="/tournois/'+str(tourn.id)+'/"><img src="/static/images/info50px.jpg" alt="infos"/></a>' #une image doit tjs se trouver dans le dossier static
				output += tourn.tournamentName
				output += '</td><td>'
				output += tourn.gameSystem
				output += '</td><td>'
				output += tourn.city
				output += '</td><td>'
				output += str(tourn.id)  #str pour convertion de int vers string
				output += '</td></tr>'
			output+='</table>'
			output+='</body>'
			output+='</html>'
			
			#pas besoin de return render_template('listeTournois.html', title='Liste des tournois', output=output)
			return output			
	else: 
		output = 'devrait être impossible'
		return output
	

#test google map
@app.route("/navigation")
def Navigation():
    return render_template('navigation.html', title='Navigation')

#test
@app.route("/nav")
def Nav():
    return render_template('nav.html', title='Navigation')

@app.route("/testgeosearch")
def TestGeoSearch():
    return render_template('testgeosearch.html', title='Test geo search')
	
	

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
	
	
	

