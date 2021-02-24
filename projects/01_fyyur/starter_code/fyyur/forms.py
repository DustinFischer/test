from datetime import datetime

from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, URL, Optional

from . import enums


class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )


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
    phone = StringField(  # TODO implement validation logic for state
        'phone'
    )

    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=enums.Genre.choices()
    )

    facebook_link = StringField(
        'facebook_link', validators=[Optional(), URL()]
    )
    image_link = StringField(
        'image_link', validators=[Optional(), URL()]
    )

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
