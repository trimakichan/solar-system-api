from flask import Blueprint, abort, make_response, request, Response
from app.models.planet import Planet
from app.models.moon import Moon
from .route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db

bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@bp.get("/")
def get_all_planets():
    return get_models_with_filters(Planet, request.args)

@bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    return planet.to_dict()

@bp.post("/")
def create_planet():
    request_body = request.get_json()
    return create_model(Planet, request_body)

@bp.post("/<planet_id>/moons")
def create_moon_with_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    request_body = request.get_json()
    request_body["planet_id"] = planet.id


    return create_model(Moon, request_body)

@bp.get("/<planet_id>/moons")
def get_all_moons(planet_id):
    planet = validate_model(Planet, planet_id)
    moons = [moon.to_dict() for moon in planet.moons]

    return moons

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

