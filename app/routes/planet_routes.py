from flask import Blueprint, abort, make_response, request, Response
from app.models.planet import Planet
from .route_utilities import validate_model
from ..db import db

bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@bp.get("/")
def get_all_planets():
    query = db.select(Planet)

    name_param = request.args.get("name")
    if name_param:
        query = query.where(Planet.name.ilike(f"%{name_param}%"))

    desc_param = request.args.get("description")
    if desc_param:
        query = query.where(Planet.description.ilike(f"%{desc_param}%"))

    distance_max = request.args.get("distance_max")
    if distance_max:
        query = query.where(Planet.distance_from_sun <= distance_max)

    query = query.order_by(Planet.id)
    planets = db.session.scalars(query)

    planets_response = []
    for planet in planets:
        planets_response.append(
            planet.to_dict()
        )
    return planets_response

@bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    return planet.to_dict()


@bp.post("/")
def create_planet():
    request_body = request.get_json()
    try:
            new_planet = Planet.from_dict(request_body)
    except KeyError:
        message = {"message": "Invalid request. Please include name, description, and distance_from_sun."}
        abort(make_response(message, 400))
    # except TypeError:
    #     message = {"message": "Name and Description must be strings. Distance from sun must be a number."}
    #     abort(make_response(message, 400))

    db.session.add(new_planet)
    db.session.commit()

    return new_planet.to_dict(), 201


@bp.put("/<planet_id>")
def replace_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    request_body = request.get_json()

    name = request_body["name"]
    description = request_body["description"]
    distance_from_sun = request_body["distance_from_sun"]

    planet.name = name
    planet.description = description
    planet.distance_from_sun = distance_from_sun
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# def validate_model(planet_id):
#     try:
#         planet_id = int(planet_id)
#     except ValueError:
#         msg = {"message": f"Planet {planet_id} invalid."}
#         abort(make_response(msg, 400))

#     query = db.select(Planet).where(Planet.id == planet_id)
#     planet = db.session.scalar(query)

#     if not planet:
#         msg = {"message" : f"Planet {planet_id} is not found."}  
#         abort(make_response(msg, 404))
        
#     return planet

