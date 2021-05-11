# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#
import os

from dotenv import load_dotenv

from src import create_app

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, os.getenv('DOT_ENV', '.env')))

app = create_app(os.getenv('FLASK_CONFIG', ''))


if os.getenv('NUKE', '') in ['True', 'true', '1']:
    """
    Nuke the existing database and recreate the schema from scratch.
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    """
    from src.database.models import db_drop_and_create_all
    print('\n ** Nuking the database...\n')
    db_drop_and_create_all()


if __name__ == '__main__':
    app.run()
