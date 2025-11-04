from flask import Blueprint, request
from .route_utilities import create_model, get_models_with_filters
from ..models.moon import Moon

bp = Blueprint("moons_bp", __name__, url_prefix="/moons")

@bp.post("/")
def create_moon():
    request_body = request.get_json()
    return create_model(Moon, request_body)

@bp.get("/")
def get_all_moons():
    return get_models_with_filters(Moon, request.args)