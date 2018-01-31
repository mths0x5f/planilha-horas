from .. import db


class Feriados(db.Model):  # TODO: Populate with default values
    id = db.Column('id', db.Integer, primary_key=True)
    data = db.Column('data', db.Text, unique=True, nullable=False)
    nome = db.Column('nome', db.Text, unique=True, nullable=False)

    def __str__(self):
        return self.nome
