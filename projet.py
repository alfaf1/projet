from flask import Flask, render_template, request, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a39938273acbdcd3fbd1e96a1b9efb36'

#Initialisation de la base de donnees
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, User, Tournaments
from geopy.geocoders import Nominatim
from geopy import distance 				#calcul des distances entre deux points géographiques
import random


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
	
	


@app.route("/choixSystJeu", methods=['POST'])
def ChoixSystJeu():
	if request.method == 'POST':
		output = '<form action="/resultatsRecherche" method="post">'
		output+= '<input id="distance" name="distance" type="hidden" value="'+request.form['distance']+'">' 
		output+= '<input id="dateD" name="dateD" type="hidden" value="'+request.form['dateD']+'">' 
		output+= '<input id="ville" name="ville" type="hidden" value="'+request.form['ville']+'">' 
		tournois = session.query(Tournaments.gameSystem).distinct(Tournaments.gameSystem).order_by(Tournaments.gameSystem)
		for tourn in tournois:
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
	

@app.route('/resultatsRecherche', methods=['POST'])
def ResultatsRecherche2():
	if request.method == 'POST':
		if request.form['jeux']:

			strFilter = request.form.getlist('jeux')

			tournois = session.query(Tournaments).filter(Tournaments.gameSystem.in_(strFilter)).all()


			output = ''
			output += '<!DOCTYPE html>'
			output += '<html>'
			output += '  <head>'
			output += '<title>tournaments Page</title>'
			output += '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.4.0/dist/leaflet.css" integrity="sha512-puBpdR0798OZvTTbP4A8Ix/l+A4dHDD0DGqYW6RQ+9jxkRFclaxxQb/SJAWZfWAkuyeQUytO7+7N4QKrDh+drA==" crossorigin=""/>'
			output += '<script src="https://unpkg.com/leaflet@1.4.0/dist/leaflet.js" integrity="sha512-QVftwZFqvtRNi0ZyCtsznlKSWOStnDORoefr1enyq5mVL4tmKB3S/EnC3rRJcxCPavG10IcrVGSmPh6Qw5lwrg==" crossorigin=""></script>'
			output += '<script src="https://unpkg.com/leaflet-geosearch@2.2.0/dist/bundle.min.js"></script>'
			output += '<style type="text/css">'
			output += '#map 	{'
			output += '	width: 600px;'
			output += ' height: 400px;'
			output += '}'
			output += '</style>'
			output += '</head>'
			output += '<body>'
			output += "<div id='map'></div>"
			output += '<script>'
			output += 'var query_addr = "Paris";'
			output += 'var provider = new window.GeoSearch.OpenStreetMapProvider(); '
			output += 'var query_promise = provider.search({ query: query_addr}); '
			output += 'query_promise.then( value => { '
			output += '   for(i=0;i < 1; i++){ '
			output += '	var x_coor = value[i].x; '
			output += '   var y_coor = value[i].y; '
			output += '	var label = value[i].label; '
			output += "	var map = L.map( 'map', { "
			output += '		center: [y_coor,x_coor],'
			output += '		zoom: 5 '
			output += '	}); '
			output += "	L.tileLayer( 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { "
			output += '		attribution: \'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>\', '
			output += "		subdomains: ['a','b','c'] "
			output += '	}).addTo( map ); '
			listeVille = []

			for tourn in tournois:
				#rlat = 100000 *(tourn.lat )/(100000+ random.randint(1,1000))
				#rlong= 100000 *(tourn.longg )/(100000+ + random.randint(1,1000))
				rlat = tourn.lat
				rlong = tourn.longg
				#output += 'L.marker(['+str(rlat)+','+str(rlong)+']).addTo(map); '
				output += 'L.marker(['+str(rlat)+','+str(rlong)+']).addTo(map).bindPopup(\'<a href="/tournois/'+str(tourn.id)+'"><img src="/static/images/info50px.jpg" alt="infos"/></a>infos\'  );'
			if request.form['distance']:
					distanceMetre = int(request.form['distance'])*1000
					if request.form['ville']:
						geolocator = Nominatim(user_agent="TabTopProject")
						location = geolocator.geocode(request.form['ville'])
						latlong = (location.latitude, location.longitude)
						lat = location.latitude
						long = location.longitude
					else: 
						lat = 48.864716
						long = 2.349014
						paris = (lat,long)
						latlong = paris												
			output += 'var centerIcon = L.icon({'
			output += "iconUrl: '/static/images/icon.png',"
			output += "shadowUrl: '/static/images/icon.png',"
			output += "iconSize:     [77, 77]," 
			output += "shadowSize:	 [77,77],"
			output += "iconAnchor:   [38, 38],"
			output += "popupAnchor:  [-3, -76],"
			output += "shadowAnchor: [4,62]"
			output += "});"
			output += "L.marker(["+str(lat)+","+str(long)+", {icon: centerIcon}]).addTo(map).bindPopup('le centre de votre recherche!'); "
			output += 'var circle = L.circle(['+str(lat)+','+str(long)+'], {'
			output += "color: 'red',"
			output += "fillColor: '#f03',"
			output += 'fillOpacity: 0.1,'
			output += 'radius: '+str(distanceMetre) + ' '
			output += '}).addTo(map);'
			output += '   }; '
			output += '}, reason => { '
			output += '  console.log(reason); '
			output += '} ); '
			output +='</script> '
			output += '<table border=3><tr><th>Start date</th><th>Nom</th><th>game System</th><th>city</th><th>id</th><th>latitude</th><th>longitude</th><th>distance</th></tr>'
			for tourn in tournois:
				lieu = (tourn.lat, tourn.longg)
				if tourn.lat>=-90 and tourn.lat<=90:
					
					booDist = request.form['distance']
					if booDist:
						dist = distance.distance(latlong, lieu).km
					else:
						dist = 0
					booDate = request.form['dateD'] 
					if ((booDist and dist < int(request.form['distance'])) or not booDist) and ((booDate and request.form['dateD']==tourn.startDate) or not booDate):
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
						output += str(tourn.id)  #str pour conversion de int vers string
						output += '</td><td>'
						output += str(tourn.lat)
						output += '</td><td>'
						output += str(tourn.longg) 
						output += '</td><td>'
						output += str(round(dist,2))+'km'
						output += '</td></tr>'
			output+='</table>'
			output+='</body>'
			output+='</html>'
			return output
	else: 
		output = 'devrait être impossible'
		return output



@app.route('/resultatsRechercheold', methods=['POST'])
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
	
	
	

