import babel
import dateutil.parser
from flask import Flask
from flask_moment import Moment

from fyyur.config import DevConfig
from .utils import env

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#
app = Flask(__name__)

DEBUG = env('DEBUG', default=True)
if DEBUG:
    app.config.from_object('fyyur.config.DevConfig')
else:
    app.config.from_object('fyyur.config.ProdConfig')

import fyyur.controllers

moment = Moment(app)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    # breakpoint()
    date = dateutil.parser.parse(value)
    # breakpoint()
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# # Default port:
# if __name__ == '__main__':
#     app.run()

# Or specify port manually:
#
# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)
#
