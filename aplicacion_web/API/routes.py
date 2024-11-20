from flask import Blueprint, render_template, make_response, jsonify
from .models import Medico
from ..webapp.app import db

main = Blueprint('main', __name__)


# @main.route('/')
# def test():
#     return render_template(jsonify({'message': 'test route'}), 200)

@main.route('/')
def index():
    medicos = Medico.query.all()
    return render_template('index.html', medicos=medicos)
