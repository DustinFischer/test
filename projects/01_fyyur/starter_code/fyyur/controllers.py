# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import logging
from logging import Formatter, FileHandler

from flask import render_template, request, flash, redirect, url_for, abort

from .forms import *
from .models import *


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
@app.route('/venues')
def list_venues():
    #  TODO: num_shows should be aggregated based on number of upcoming shows per venue.

    # Find unique combinations of states existing in database
    distinct_states = db.session.query(Venue).distinct(Venue.state) \
        .with_entities(Venue.state) \
        .order_by(Venue.state).all()

    # Compile context
    # Loop by state to avoid excessive db hits with unique (state, city) combos
    data = []
    for state, in distinct_states:
        venues = Venue.query.filter_by(state=state).order_by(Venue.city)
        cities = {}
        for venue in venues:
            if venue.city not in cities:
                cities[venue.city] = {
                    'city': venue.city,
                    'state': venue.state.label,
                    'venues': []
                }

            cities[venue.city]['venues'].append({
                'id': venue.id,
                'name': venue.name,
                'num_upcoming_shows': 1  # TODO: Implement
            })
        data.extend(cities.values())
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/create', methods=['GET', 'POST'])
def create_venue():
    form = VenueForm(request.form)

    # Handle create form POST submission
    if form.is_submitted():
        success_msg = ['Venue ' + request.form['name'] + ' was successfully listed!', 'alert-success']
        if form.validate():
            try:
                with db_session() as session:
                    venue = Venue()
                    form.populate_obj(venue)
                    session.add(venue)
            except Exception:
                success_msg = ['Failed to add Venue ' + request.form['name'] + '!', 'alert-danger']
        else:
            return render_template('forms/change_venue.html', form=form)

        flash(*success_msg)
        return redirect(url_for('index'))

    # Return empty create form on GET
    return render_template('forms/change_venue.html', form=form, add=True)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id) or abort(404)

    # Join query for venue shows, extract artist and show details
    shows = Show.query.join(Venue).filter(Show.venue_id == venue_id) \
        .with_entities(Artist.id.label('artist_id'),
                       Artist.name.label('artist_name'),
                       Artist.image_link.label('artist_image_link'),
                       Show.start_time)

    past_shows = shows.filter(Show.start_time <= datetime.now())
    upcoming_shows = shows.filter(Show.start_time > datetime.now())

    context = {
        **venue.__dict__,
        'past_shows': past_shows.all(),
        'upcoming_shows': upcoming_shows.all(),
        'past_shows_count': past_shows.count(),
        'upcoming_shows_count': upcoming_shows.count(),
    }
    return render_template('pages/show_venue.html', venue=context)


@app.route('/venues/<int:venue_id>/edit', methods=['GET', 'POST'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id) or abort(404)
    form = VenueForm(obj=venue)

    if form.validate_on_submit():
        with db_session() as session:
            form.populate_obj(venue)
            session.add(venue)
        return redirect(url_for('show_venue', venue_id=venue_id))

    return render_template('forms/change_venue.html', form=form, venue=venue)


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    response = {
        "count": 1,
        "data": [{
            "id": 2,
            "name": "The Dueling Pianos Bar",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def list_artists():
    artists = Artist.query.order_by(Artist.name).with_entities(Artist.id, Artist.name)
    return render_template('pages/artists.html', artists=artists)


@app.route('/artists/create', methods=['GET', 'POST'])
def create_artist():
    form = ArtistForm(request.form)

    # Handle create form POST submission
    if form.is_submitted():
        success_msg = ['Artist ' + request.form['name'] + ' was successfully listed!', 'alert-success']
        if form.validate():
            try:
                with db_session() as session:
                    artist = Artist()
                    form.populate_obj(artist)
                    session.add(artist)
            except Exception as exc:
                success_msg = ['Failed to add Artist ' + request.form['name'] + '!', 'alert-danger']
        else:
            return render_template('forms/change_artist.html', form=form)

        flash(*success_msg)
        return render_template('pages/home.html')

    # Return empty create form
    return render_template('forms/change_artist.html', form=form, add=True)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id) or abort(404)

    # Join query for artist shows, extract artist and show details
    shows = Show.query.join(Venue).filter(Show.artist_id == artist_id) \
        .with_entities(Venue.id.label('venue_id'),
                       Venue.name.label('venue_name'),
                       Venue.image_link.label('venue_image_link'),
                       Show.start_time)

    past_shows = shows.filter(Show.start_time <= datetime.now())
    upcoming_shows = shows.filter(Show.start_time > datetime.now())

    context = {
        **artist.__dict__,
        'past_shows': past_shows.all(),
        'upcoming_shows': upcoming_shows.all(),
        'past_shows_count': past_shows.count(),
        'upcoming_shows_count': upcoming_shows.count(),
    }
    return render_template('pages/show_artist.html', artist=context)


@app.route('/artists/<int:artist_id>/edit', methods=['GET', 'POST'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id) or abort(404)
    form = ArtistForm(obj=artist)

    if form.validate_on_submit():
        with db_session() as session:
            form.populate_obj(artist)
            session.add(artist)
        return redirect(url_for('show_artist', artist_id=artist_id))

    return render_template('forms/change_artist.html', form=form, artist=artist)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {
        "count": 1,
        "data": [{
            "id": 4,
            "name": "Guns N Petals",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def list_shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "artist_id": 4,
        "artist_name": "Guns N Petals",
        "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "start_time": "2019-05-21T21:30:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 5,
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
    }]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create', methods=['GET', 'POST'])
def create_show():
    form = ShowForm(request.form)

    # Handle create form POST submission
    if form.is_submitted():
        success_msg = ['Show was successfully listed!', 'alert-success']
        if form.validate():
            try:
                with db_session() as session:
                    show = Show()
                    form.populate_obj(show)
                    session.add(show)
            except Exception:
                success_msg = ['Failed to add Show!', 'alert-danger']
        else:
            return render_template('forms/change_show.html', form=form)

        flash(*success_msg)
        return redirect(url_for('index'))

    # Return empty create form on GET
    return render_template('forms/change_show.html', form=form, add=True)


#  Default Handlers
#  ----------------------------------------------------------------

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# TODO: Add csrf handler see https://flask-wtf.readthedocs.io/en/stable/api.html
