from flask import jsonify
from flask import request
from flask import views

from .. import db
from ..models import Eventos
from ..utils.dates import retroativo
from ..utils.dates import evento_maior_que_24h


class EventosAPIController(views.MethodView):
    def get(self, id=None):
        if id is None:
            return jsonify([a.serialize for a in Eventos.query.all()])
        else:
            a = Eventos.query.filter_by(id=id).first_or_404()
            return jsonify(a.serialize)

    def post(self):
        if request.is_json:
            req = request.json
        else:
            req = request.form

        if (len(req.get('matricula')) == 0
            or len(req.get('descricao')) == 0
            or len(req.get('demandas')) == 0
            or len(req.get('data-inicio')) == 0
            or len(req.get('data-fim')) == 0
        ):
            return jsonify(
                {'message': 'Todos os campos são obrigatórios.'}), 500

        if retroativo(req.get('data-inicio')):
            return jsonify(
                {'message': 'Data retroativa fora dos limites. Contate seu facilitador.'}), 500

        if evento_maior_que_24h(req.get('data-inicio'), req.get('data-fim')):
            return jsonify(
                {'message': 'Evento maior do que 24 horas consecutivas.'}), 500

        a = Eventos().from_form_data(req)
        db.session.add(a)
        try:
            db.session.commit()
            return jsonify({'message': 'Operação realizada com sucesso!'})
        except Exception:
            return jsonify(
                {'message': 'Por favor, verifique todos os campos.'}), 409

    def put(self, id):
        a = Eventos.query.filter_by(id=id).first_or_404()
        if request.is_json:
            req = request.json
        else:
            req = request.form
        a = a.from_form_data(req)
        db.session.add(a)
        try:
            db.session.commit()
            return jsonify({'message': 'Operação realizada com sucesso!'})
        except Exception:
            return jsonify(
                {'message': 'Por favor, verifique todos os campos.'}), 409

    def delete(self, id=None):

        if id is None:
            for id in request.json:
                Eventos.query.filter_by(id=id).delete()
        else:
            Eventos.query.filter_by(id=id).delete()

        try:
            db.session.commit()
            return jsonify({'message': 'Remoção feita com sucesso.'})
        except Exception:
            return jsonify({'message': 'Remoção falhou.'}), 500
