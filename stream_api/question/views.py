# api/question/views.py


from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from api import bcrypt, db
from api.db_access.models import Question


question_blueprint = Blueprint('question', __name__)


