from flask import Blueprint


BP_NAME = 'foss'
bp = Blueprint(BP_NAME, __name__)

from . import views
