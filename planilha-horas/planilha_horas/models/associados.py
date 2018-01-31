from .. import db


class Associados(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    fk_empresa = db.Column('empresa', db.Integer,
                           db.ForeignKey('empresas.codigo'), nullable=False)
    empresa = db.relationship('Empresas')
    matricula = db.Column('matricula', db.Text, unique=True, nullable=False)
    cr = db.Column('cr', db.Text, nullable=False)
    nome = db.Column('nome', db.Text, nullable=False)
    usuario = db.Column('usuario', db.Text, unique=True, nullable=False)
    perfil = db.Column('perfil', db.Text, nullable=False)
    fk_facilitador = db.Column('facilitador', db.Text,
                           db.ForeignKey('associados.matricula'), nullable=False)
    facilitador = db.relationship('Associados', remote_side=[matricula])

    def from_form_data(self, form):
        if form.get('empresa') is not None:
            self.fk_empresa = form.get('empresa')
        if form.get('matricula') is not None:
            self.matricula = form.get('matricula')
        if form.get('cr') is not None:
            self.cr = form.get('cr').upper()
        if form.get('nome-associado') is not None:
            self.nome = form.get('nome-associado')
        if form.get('usuario') is not None:
            self.usuario = form.get('usuario')
        if form.get('perfil') is not None:
            self.perfil = form.get('perfil')
        if form.get('facilitador') is not None:
            self.fk_facilitador = form.get('facilitador')

        return self

    @property
    def serialize(self):
        return {'matricula': self.matricula,
                'nome': self.nome,
                'usuario': self.usuario,
                'perfil': self.perfil,
                'facilitador': str(self.facilitador.nome),
                'empresa': int(self.fk_empresa),
                'cr': self.cr}

    def __str__(self):
        return self.nome
