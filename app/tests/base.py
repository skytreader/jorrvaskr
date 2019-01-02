from flask_testing import TestCase
import app as App
import unittest

app = App.make_app()
app.config["TESTING"] = True

class AppTestCase(TestCase):

    def create_app(self):
        return app
