from .. import db


class Empresas(db.Model):  # TODO: Populate with default values
    id = db.Column('id', db.Integer, primary_key=True)
    codigo = db.Column('codigo', db.Integer, unique=True, nullable=False)
    nome = db.Column('nome', db.Text, unique=True, nullable=False)

    def __str__(self):
        return self.nome
