from flask import Blueprint

bp = Blueprint('workplace', __name__)

from app.workplace import routes  # noqa: E402, F401
