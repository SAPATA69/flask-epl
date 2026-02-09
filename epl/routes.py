from epl import app, db
from epl import models
from flask import flash, render_template, request, redirect, url_for

# ==================== HOME ====================
@app.route('/')
def index():
    return render_template('index.html', title='Home')


# ==================== CLUBS ====================
@app.route('/clubs')
def all_clubs():
    clubs = db.session.scalars(db.select(models.Club)).all()
    return render_template('clubs/index.html', title='Clubs', clubs=clubs)


@app.route('/clubs/new', methods=['GET', 'POST'])
def club_new():
    if request.method == 'POST':
        # รับข้อมูลจาก form (field names ต้องตรงกับ HTML)
        name = request.form.get('club_name')
        stadium = request.form.get('stadium')
        year = request.form.get('year')
        logo = request.form.get('logo')
        
        # Validation
        if not name or not stadium or not year or not logo:
            flash('All fields are required!', 'danger')
            return render_template('clubs/new_club.html', title='Add Club')
        
        try:
            year = int(year)
            club = models.Club(
                name=name,
                stadium=stadium,
                founded_year=year,
                logo=logo
            )
            db.session.add(club)
            db.session.commit()
            flash(f'Club "{name}" added successfully!', 'success')
            return redirect(url_for('all_clubs'))
            
        except ValueError:
            flash('Founded year must be a number!', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('clubs/new_club.html', title='Add Club')


@app.route('/clubs/search', methods=['GET', 'POST'])
def search_clubs():
    clubs = []
    search_query = ''
    
    if request.method == 'POST':
        search_query = request.form.get('club_name', '').strip()
        
        if search_query:
            # ค้นหาจากชื่อสโมสรหรือสนาม
            clubs = db.session.scalars(
                db.select(models.Club).where(
                    db.or_(
                        models.Club.name.ilike(f'%{search_query}%'),
                        models.Club.stadium.ilike(f'%{search_query}%')
                    )
                )
            ).all()
            
            if not clubs:
                flash(f'No clubs found for "{search_query}"', 'info')
        else:
            flash('Please enter a search term', 'warning')
    
    # Return partial HTML for HTMX
    return render_template('clubs/search_club.html', clubs=clubs)


@app.route('/clubs/<int:club_id>')
def club_info(club_id):
    club = db.session.get(models.Club, club_id)
    if club is None:
        flash('Club not found!', 'danger')
        return redirect(url_for('all_clubs'))
    
    return render_template('clubs/info_club.html', title=club.name, club=club)


@app.route('/clubs/<int:club_id>/edit', methods=['GET', 'POST'])
def club_edit(club_id):
    club = db.session.get(models.Club, club_id)
    if club is None:
        flash('Club not found!', 'danger')
        return redirect(url_for('all_clubs'))
    
    if request.method == 'POST':
        club.name = request.form.get('name')
        club.stadium = request.form.get('stadium')
        club.founded_year = int(request.form.get('year'))
        club.logo = request.form.get('logo')
        
        try:
            db.session.commit()
            flash(f'Club "{club.name}" updated successfully!', 'success')
            return redirect(url_for('club_info', club_id=club.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('clubs/update_club.html', title='Edit Club', club=club)


@app.route('/clubs/<int:club_id>/delete', methods=['POST'])
def club_delete(club_id):
    club = db.session.get(models.Club, club_id)
    if club is None:
        flash('Club not found!', 'danger')
        return redirect(url_for('all_clubs'))
    
    try:
        club_name = club.name
        db.session.delete(club)
        db.session.commit()
        flash(f'Club "{club_name}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('all_clubs'))


# ==================== PLAYERS ====================
@app.route('/players')
def all_players():
    players = db.session.scalars(db.select(models.Player)).all()
    return render_template('players/index.html', title='Players', players=players)


@app.route('/players/new', methods=['GET', 'POST'])
def player_new():
    if request.method == 'POST':
        name = request.form.get('name')
        position = request.form.get('position')
        age = request.form.get('age')
        nationality = request.form.get('nationality')
        goals = request.form.get('goals', 0)
        squad_no = request.form.get('squad_no')
        img = request.form.get('img')
        club_id = request.form.get('club_id')
        
        try:
            player = models.Player(
                name=name,
                position=position,
                age=int(age),
                nationality=nationality,
                goals=int(goals) if goals else 0,
                squad_no=int(squad_no) if squad_no else None,
                img=img,
                club_id=int(club_id) if club_id else None
            )
            db.session.add(player)
            db.session.commit()
            flash(f'Player "{name}" added successfully!', 'success')
            return redirect(url_for('all_players'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    clubs = db.session.scalars(db.select(models.Club)).all()
    return render_template('players/new_player.html', title='Add Player', clubs=clubs)


@app.route('/players/<int:player_id>')
def player_info(player_id):
    player = db.session.get(models.Player, player_id)
    if player is None:
        flash('Player not found!', 'danger')
        return redirect(url_for('all_players'))
    
    return render_template('players/info_player.html', title=player.name, player=player)


@app.route('/players/<int:player_id>/edit', methods=['GET', 'POST'])
def player_edit(player_id):
    player = db.session.get(models.Player, player_id)
    if player is None:
        flash('Player not found!', 'danger')
        return redirect(url_for('all_players'))
    
    if request.method == 'POST':
        player.position = request.form.get('position')
        player.goals = int(request.form.get('goals', 0))
        player.squad_no = int(request.form.get('squad_no')) if request.form.get('squad_no') else None
        player.img = request.form.get('img')
        player.club_id = int(request.form.get('club_id')) if request.form.get('club_id') else None
        
        try:
            db.session.commit()
            flash(f'Player "{player.name}" updated successfully!', 'success')
            return redirect(url_for('player_info', player_id=player.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    clubs = db.session.scalars(db.select(models.Club)).all()
    return render_template('players/update_player.html', 
                         title='Edit Player', 
                         player=player, 
                         clubs=clubs)


@app.route('/players/search', methods=['POST'])
def search_players():
    search_query = request.form.get('player_name', '').strip()
    players = []
    
    if search_query:
        players = db.session.scalars(
            db.select(models.Player).where(
                db.or_(
                    models.Player.name.ilike(f'%{search_query}%'),
                    models.Player.nationality.ilike(f'%{search_query}%')
                )
            )
        ).all()
    
    return render_template('players/search_player.html', players=players)