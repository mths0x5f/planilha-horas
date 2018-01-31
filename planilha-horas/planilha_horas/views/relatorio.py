from flask import render_template
from flask import send_file

from .. import app
from ..models import Eventos
from ..utils.relatorio import gera_relatorio_consolidado


@app.route('/relatorio')
def relatorio():
    return render_template('relatorio.html',
                           eventos=Eventos.query.all())


@app.route('/gerar-relatorio')
def gera_relatorio():
    output, filename = gera_relatorio_consolidado()
    return send_file(output, attachment_filename=filename,
                     as_attachment=True)
