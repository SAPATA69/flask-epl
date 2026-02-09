from epl import app, db
from epl import models
import epl.routes
from flask import flash, render_template, request

@app.route('/')
def index():
    return render_template('index.html', title= 'Home')

@app.route('/clubs')
def all_clubs():
    clubs = db.session.scalars(db.select(models.Club)).all()
    return render_template('clubs/index.html', title= 'Clubs', clubs=clubs)

@app.route('/Club/news')
def club_news():
    if request.method == 'POST':
        name = request.form.get('club_name')
        stadium = request.form.get('stadium')
        year = int(request.form.get('founded_year'))
        logo = request.form.get('logo_url')

        club = models.Club(name=name, stadium=stadium, founded_year=year, logo=logo)
        db.session.add(club)
        db.session.commit()
        flash('Club added successfully!', 'success')
    return render_template('clubs/news.html', title='Add Club')

@app.route('/clubs/search', methods=['GET', 'POST'])
def search_clubs():
    
    


   




