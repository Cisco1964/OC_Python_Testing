import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions

def init_places(comps, clubs):
    mylist = []
    for comp in comps:
        for club in clubs:
            mylist.append({'competition': comp['name'], 'booked': [0, club['name']]})
    return mylist


def update_places(competition, club, places, placesRequired):
    for elem in places:
        if elem['competition'] == competition['name']:
            if elem['booked'][1] == club['name']:
                if elem['booked'][0] + placesRequired <= 12:
                    elem['booked'][0] += placesRequired
                    break
                else:
                    raise ValueError("Vous ne pouvez pas reserver plus de 12 places")
    return places

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
places = init_places(competitions, clubs)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions)
    except IndexError:
        # test email à blanc ou inconnu
        if request.form['email'] == "":
            flash("Veuillez saisir votre adresse mail")
        else:
            flash("Email inconnu")
        status_code = 401
        return render_template('index.html'), status_code


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundclub = [c for c in clubs if c['name'] == club][0]

    # Booking_places_in_past_competition
    try:
        foundcompetition = [c for c in competitions if c['name'] == competition][0]

        if datetime.strptime(foundcompetition['date'], '%Y-%m-%d %H:%M:%S') < datetime.now():
            flash("Cette competition est déjà terminée.", 'error')
            status_code = 400
        else:
            return render_template('booking.html', club=foundclub, competition=foundcompetition)
    except IndexError:
        flash("Il y a un dysfonctionnement, Veuillez recommencer", 'error')
        status_code = 404

    return render_template('welcome.html', club=foundclub), status_code


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    try: 
        #### Point updates are not reflected
        placesRequired = int(request.form['places'])

        # Clubs_use_more_than_their_points_allowed

        if placesRequired > 12:
            flash('Vous ne pouvez pas reserver plus de 12 places')
            status_code = 400
            return render_template('booking.html', club=club, competition=competition), status_code
        elif placesRequired * 3 > int(club['points']):
            flash('Pas assez de place disponible')
            status_code = 400
            return render_template('booking.html', club=club, competition=competition), status_code
        
        else:
            try:
                # Sauvegarde du nombre de reservations par club et par competition
                update_places(competition, club, places, placesRequired)
                competition['numberOfPlaces'] = int(competition['numberOfPlaces'])- placesRequired

                # Bonjour à tous Je viens de terminer une conférence téléphonique avec 
                # l'équipe régionale, et il semble qu'il n'y ait pas un seul point / place. 
                # Il s'agit de 3 points/place. Je ne sais pas si cela change quelque chose, 
                # mais j'ai besoin que vous mettez ça en place pour la démo. 
                # Ils vont être très contents !

                club['points'] = int(club['points'])- (placesRequired *  3)
                flash("Great-booking complete!")
                status_code = 200
                return render_template('welcome.html', club=club, competitions=competitions), status_code
            except ValueError as error_message:
                # Retour message d'erreur --> on ne peut pas réserver plus de 12 places par compétition
                flash(error_message)
                status_code = 400
                return render_template('booking.html', club=club, competition=competition), status_code
    except ValueError:
        flash("Saisir un nombre entre 0 et 12, Veuillez recommencer")
        status_code = 400
        return render_template('booking.html', club=club, competition=competition), status_code


# Affichage de la liste des clubs avec leur point
@app.route('/clubpoints')
def clubpoints():
    clublist = sorted(clubs, key=lambda club: club['name'])
    return render_template('club_points.html', clubs=clublist)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))