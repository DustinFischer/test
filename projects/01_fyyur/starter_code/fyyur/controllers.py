# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import logging
from logging import Formatter, FileHandler

from flask import render_template, request, flash, redirect, url_for, abort, jsonify
from flask_wtf.csrf import CSRFError

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
    shows = Show.query.join(Venue).filter(Show.venue_id == venue_id)

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
    venue = Venue.query.get(venue_id) or abort(404)

    try:
        with db_session() as session:
            session.delete(venue)
    except Exception:
        abort(404)

    flash('Venue was successfully deleted!', 'alert-success')
    return jsonify({'success': True})


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))

    return render_template('pages/search_venues.html', venues=venues,
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
    shows = Show.query.join(Venue).filter(Show.artist_id == artist_id)

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
    search_term = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))

    return render_template('pages/search_artists.html', artists=artists,
                           search_term=request.form.get('search_term', ''))


#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def list_shows():
    # Only list upcoming shows
    shows = Show.query.filter(Show.start_time > datetime.now())
    return render_template('pages/shows.html', shows=shows)


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


@app.errorhandler(CSRFError)
def csrf_error(reason):
    return render_template('errors/csrf.html', reason=reason)


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')
