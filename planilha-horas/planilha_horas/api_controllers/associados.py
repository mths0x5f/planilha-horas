from flask import jsonify
from flask import request
from flask import views

from .. import db
from ..models import Associados


class AssociadosAPIController(views.MethodView):
    def get(self, matricula=None):
        if matricula is None:
            return jsonify([a.serialize for a in Associados.query.all()])
        else:
            a = Associados.query.filter_by(matricula=matricula).first_or_404()
            return jsonify(a.serialize)

    def post(self):
        if request.is_json:
            req = request.json
        else:
            req = request.form

        if (len(req.get('empresa')) == 0
            or len(req.get('matricula')) == 0
            or len(req.get('cr')) == 0
            or len(req.get('nome-associado')) == 0
            or len(req.get('usuario')) == 0
            or len(req.get('perfil')) == 0
            or len(req.get('facilitador')) == 0
        ):
            return jsonify(
                {'message': 'Todos os campos são obrigatórios.'}), 500

        a = Associados().from_form_data(req)
        db.session.add(a)
        try:
            db.session.commit()
            return jsonify({'message': 'Operação realizada com sucesso!'})
        except Exception:
            return jsonify(
                {'message': 'Por favor, verifique todos os campos.'}), 409

    def put(self, matricula):
        a = Associados.query.filter_by(matricula=matricula).first_or_404()
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

    def delete(self, matricula=None):

        if matricula is None:
            for matricula in request.json:
                Associados.query.filter_by(matricula=matricula).delete()
        else:
            Associados.query.filter_by(matricula=matricula).delete()

        try:
            db.session.commit()
            return jsonify({'message': 'Remoção feita com sucesso.'})
        except Exception:
            return jsonify({'message': 'Remoção falhou.'}), 500
