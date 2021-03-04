from datetime import datetime

from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, IntegerField
from wtforms.validators import DataRequired, URL, Optional, ValidationError

from . import enums
from . import models


class ShowForm(Form):
    artist_id = IntegerField(
        'artist_id',
    )
    venue_id = IntegerField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )

    def validate_artist_id(self, field):
        if models.Artist.query.get(field.data) is None:
            raise ValidationError('Artist matching ID not found')

    def validate_venue_id(self, field):
        if models.Venue.query.get(field.data) is None:
            raise ValidationError('Venue matching ID not found')


class VenueForm(Form):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=enums.State.choices()
    )
    address = StringField('address', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])

    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=enums.Genre.choices(), coerce=int,
    )
    seeking_talent = BooleanField('seeking_talent', default=True)
    seeking_description = StringField('seeking_description', validators=[Optional()])

    website = StringField('website', validators=[Optional(), URL()])
    facebook_link = StringField('facebook_link', validators=[Optional(), URL()])
    image_link = StringField('image_link', validators=[Optional(), URL()])


class ArtistForm(Form):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=enums.State.choices()
    )
    phone = StringField('phone', validators=[DataRequired()])

    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=enums.Genre.choices(), coerce=int,
    )
    seeking_venue = BooleanField('seeking_venue', default=True)
    seeking_description = StringField('seeking_description', validators=[Optional()])

    website = StringField('website', validators=[Optional(), URL()])
    facebook_link = StringField('facebook_link', validators=[Optional(), URL()])
    image_link = StringField('image_link', validators=[Optional(), URL()])


