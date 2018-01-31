from .. import db
from ..filters import regras_th

class Eventos(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    fk_associado = db.Column('associado', db.Integer,
                             db.ForeignKey('associados.matricula'),
                             nullable=False)
    associado = db.relationship('Associados')
    # tipo = db.Column('tipo', db.Text, nullable=False)
    # cod_tipo = db.Column('cod_tipo', db.Text, nullable=False)
    descricao = db.Column('descricao', db.Text, nullable=False)
    sgd = db.Column('sgd', db.Text, nullable=False)
    data_inicio = db.Column('data_inicio', db.Text, nullable=False)
    data_fim = db.Column('data_fim', db.Text, nullable=False)

    def from_form_data(self, form):
        if form.get('matricula') is not None:
            self.fk_associado = form.get('matricula')
        if form.get('descricao') is not None:
            self.descricao = form.get('descricao')
        if form.get('demandas') is not None:
            self.sgd = form.get('demandas')
        if form.get('data-inicio') is not None:
            self.data_inicio = form.get('data-inicio')
        if form.get('data-fim') is not None:
            self.data_fim = form.get('data-fim')

        return self

    @property
    def serialize(self):
        return {'id': self.id,
                'matricula-associado': self.fk_associado,
                'descricao': self.descricao,
                'demandas': self.sgd,
                'data-inicio': self.data_inicio,
                'data-fim': self.data_fim,
                'tipos': regras_th.tipo_evento(self.data_inicio, self.data_fim)}
