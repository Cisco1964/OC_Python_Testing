import json
from flask import Flask,render_template,request,redirect,flash,url_for


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
            if elem['booked'][1] == club['name'] and elem['booked'][0] + placesRequired <= 12:
                elem['booked'][0] += placesRequired
                break
            else:
                raise ValueError("Vous ne pouvez pas réserver plus de 12 places")
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
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    try:
        placesRequired = int(request.form['places'])

        if placesRequired > int(competition['numberOfPlaces']):
            flash('Pas assez de place disponible')
        elif placesRequired * 4 > int(club['points']):
            flash("Pas assez de place disponible")
        else:
            try:
                update_places(competition, club, places, placesRequired)
                competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
                club['points'] = int(club['points']) - (placesRequired * 4)
                flash('Great-booking complete!', 'success')

                return render_template(
                    'welcome.html',
                    club=club,
                    past_competitions=past_competitions,
                    present_competitions=present_competitions
                )

            except ValueError as error_message:
                flash(error_message, 'error')

    except ValueError:
        flash("Saisir un nombre entre 1 et 12")
        status_code = 400

    return render_template('booking.html', club=club, competition=competition), status_code


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))