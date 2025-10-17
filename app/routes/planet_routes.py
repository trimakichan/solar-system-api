from flask import Blueprint
from app.models.planet import PLANETS

planet_bp = Blueprint("planet_bp", __name__, url_prefix="/planets")


@planet_bp.get("")
def get_planets():
    results = []

    for planet in PLANETS:
        results.append({
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "distance_from_sun": planet.distance_from_sun
        })

    return results