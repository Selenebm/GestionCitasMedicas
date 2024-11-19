from flask import Blueprint, make_response, jsonify
from .models import Medico

main = Blueprint('main', __name__)

# @main.route('/')
# def index():
#     medicos = Medico.query.all()
#     return render_template('index.html', medicos=medicos)

@main.route('/')
def test():
    return make_response(jsonify({'message': 'test route'}), 200)