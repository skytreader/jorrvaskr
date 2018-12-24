from app import app
from flask_testing import TestCase
import unittest

app.config["TESTING"] = True
app.make_app()

class AppTestCase(TestCase):

    def create_app(self):
        return app
