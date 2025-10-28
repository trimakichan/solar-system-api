from flask import Blueprint, abort, make_response, request, Response
from app.models.planet import Planet
from ..db import db

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@planets_bp.get("/")
def get_all_planets():
    query = db.select(Planet).order_by(Planet.id)
    planets = db.session.scalars(query)

    planets_response = []
    for planet in planets:
        planets_response.append(
            generate_dict(planet)
        )
    return planets_response

@planets_bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)
    return generate_dict(planet)


@planets_bp.post("/")
def create_planet():
    request_body = request.get_json()
    try:
        name = request_body["name"]
        description = request_body["description"]
        distance_from_sun = request_body["distance_from_sun"]
    except KeyError:
        message = {"message": "Invalid request. Please include name, description, and distance_from_sun."}
        abort(make_response(message, 400))
    except TypeError:
        message = {"message": "Name and Description must be strings. Distance from sun must be a number."}
        abort(make_response(message, 400))

    new_planet = Planet(name=name,  description=description, distance_from_sun=distance_from_sun)

    db.session.add(new_planet)
    db.session.commit()

    response = generate_dict(new_planet)
    return response, 201


@planets_bp.put("/<planet_id>")
def replace_planet(planet_id):
    planet = validate_planet(planet_id)
    request_body = request.get_json()

    name = request_body["name"]
    description = request_body["description"]
    distance_from_sun = request_body["distance_from_sun"]

    planet.name = name
    planet.description = description
    planet.distance_from_sun = distance_from_sun
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@planets_bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_planet(planet_id)
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        msg = {"message": f"Planet {planet_id} invalid."}
        abort(make_response(msg, 400))

    query = db.select(Planet).where(Planet.id == planet_id)
    planet = db.session.scalar(query)

    if not planet:
        msg = {"message" : f"Planet {planet_id} is not found."}  
        abort(make_response(msg, 404))
        
    return planet


def generate_dict(planet):
    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "distance_from_sun": planet.distance_from_sun
    }
