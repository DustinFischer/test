# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#
import os

from dotenv import load_dotenv

from flaskr import create_app

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, os.getenv('DOT_ENV', '.env')))

app = create_app(os.getenv('FLASK_CONFIG', ''))


if __name__ == '__main__':
    app.run()
