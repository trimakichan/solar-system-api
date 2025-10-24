from flask import Blueprint, abort, make_response, request
from app.models.planet import Planet
from ..db import db
# from app.models.planet import planets

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@planets_bp.post("/")
def create_planet():
    request_body = request.get_json()
    # try:
    name = request_body["name"]
    description = request_body["description"]
    distance_from_sun = request_body["distance_from_sun"]
    # except KeyError:
    #     msg = {"message: ": "Please provide a valid name, description and distance from sun."}
    #     abort(make_response(msg,401))

    new_planet = Planet(name=name,  description=description, distance_from_sun=distance_from_sun)

    db.session.add(new_planet)
    db.session.commit()

    response = {
        "id": new_planet.id,
        "name": new_planet.name,
        "description": new_planet.description,
        "distance_from_sun": new_planet.distance_from_sun
    }
    return response, 201

@planets_bp.get("/")
def get_all_planets():
    query = db.select(Planet).order_by(Planet.id)
    planets = db.session.scalars(query)

    planets_response = []
    for planet in planets:
        planets_response.append(
            {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "distance_from_sun": planet.distance_from_sun
            }
        )
    return planets_response

# @planets_bp.get("/")
# def get_all_planets():
#     planets_response = []

#     for planet in planets:
#         planet_dict = generate_dict(planet)
#         planets_response.append(planet_dict)

#     return planets_response

# @planets_bp.get("/<planet_id>")
# def get_one_planet(planet_id):
#     planet = validate_planet(planet_id)

#     return generate_dict(planet)

# def validate_planet(planet_id):
#     try:
#         planet_id = int(planet_id)
        
#     except ValueError:
#         invalid = {"message": f"Planet id {planet_id} is invalid."}

#         abort(make_response(invalid, 400))
    
#     for planet in planets:
#         if planet.id == planet_id:
#             return planet
        
#     not_found = {"message": f"Planet with id {planet_id} not found."}
#     abort(make_response(not_found, 404))


# def generate_dict(planet):
#     return {
#         "id": planet.id,
#         "name": planet.name,
#         "description": planet.description,
#         "distance_from_sun": planet.distance_from_sun
#     }
