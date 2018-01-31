from datetime import *

from ..models.feriados import Feriados


DATE_FORMAT = '%Y-%m-%dT%H:%M'


def eh_feriado(data):
    d = data.date().strftime('%m-%d')
    if Feriados.query.filter_by(data=d).first():
        return True
    else:
        return False


def retroativo(data):
    d = datetime.strptime(data, DATE_FORMAT)
    hoje = date.today()
    data_limite = hoje.replace(day=15, month=hoje.month - 1)
    if d.date() < data_limite:
        return True
    return False

def evento_maior_que_24h(data_inicio, data_fim):
    s = datetime.strptime(data_inicio, DATE_FORMAT)
    e = datetime.strptime(data_fim, DATE_FORMAT)
    if (e - s).days > 0:
        return True
    else:
        return False
