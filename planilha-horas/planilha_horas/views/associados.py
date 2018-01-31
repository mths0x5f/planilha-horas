from flask import render_template

from .. import app
from ..models import Associados, Empresas


@app.route('/associados')
def associados():
    return render_template('associados.html',
                           empresas=Empresas.query.all(),
                           associados=Associados.query.order_by(
                               Associados.nome).all(),
                           facilitadores=Associados.query.filter_by(
                               perfil='FACILITADOR').all()
                           )
