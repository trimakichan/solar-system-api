import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
from app.models.planet import Planet
import os

load_dotenv()

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_DATABASE_URI_TEST')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def add_one_planet(app):
    planet_1 = Planet(name='Mercury',
                    description='Smallest planet, closest to the Sun', 
                    distance_from_sun=57910000)

    db.session.add(planet_1)
    db.session.commit()

@pytest.fixture
def add_two_planet(app):
    planet_1 = Planet(name='Mercury',
                    description='Smallest planet, closest to the Sun', 
                    distance_from_sun=57910000)
    
    planet_2 = Planet(name='Earth',
                    description='Our beautiful home', 
                    distance_from_sun=149600000)

    db.session.add_all([planet_1,planet_2])
    db.session.commit()