from flask import Blueprint

bp = Blueprint('stories', __name__)

from app.stories import routes  # noqa: E402, F401
