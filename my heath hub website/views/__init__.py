# Views/__init__.py
from flask import Blueprint

views = Blueprint('views', __name__)

from . import views