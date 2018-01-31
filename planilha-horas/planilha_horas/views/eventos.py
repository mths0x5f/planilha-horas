from flask import redirect
from flask import render_template

from .. import app
from ..models import Eventos


@app.route('/')
def index():
    return redirect('/eventos')


@app.route('/eventos')
def eventos():
    return render_template('eventos.html',
                           eventos=Eventos.query.all())
