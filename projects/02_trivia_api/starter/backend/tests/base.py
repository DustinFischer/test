from unittest import TestCase

from flaskr import create_app
from config import TestConfig
from flaskr.models import db, setup_db


class BaseTestClass(TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.drop_all()
        setup_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
