from datetime import *
from math import floor

from ..utils.dates import DATE_FORMAT
from ..utils.dates import eh_feriado
from .. import app


@app.template_filter('tipo_evento')
def tipo_evento(data_inicio, data_fim):
    start_datetime = datetime.strptime(data_inicio, DATE_FORMAT)
    end_datetime = datetime.strptime(data_fim, DATE_FORMAT)

    tipos = []

    adicional_noturno = calcula_adicional_noturno(start_datetime, end_datetime)
    horas_em_dobro = calcula_horas_em_dobro(start_datetime, end_datetime)
    horas_extras = calcula_horas_extras(start_datetime, end_datetime)

    if adicional_noturno != 0:
        tipos.append({
            'codigo': '21030',
            'tipo': 'AD. NOTURNO',
            'duracao': floor(adicional_noturno * 100) / 100
        })

    if horas_em_dobro != 0:
        tipos.append({
            'codigo': '20070',
            'tipo': 'HORAS DOBRO',
            'duracao': floor(horas_em_dobro * 100) / 100
        })

    elif horas_extras != 0:  # quando não for domingo ou feriado
        tipos.append({
            'codigo': '00045',
            'tipo': 'HORAS EXTRA',
            'duracao': floor(horas_extras * 100) / 100
        })

    return tipos


def calcula_adicional_noturno(start_datetime, end_datetime):
    # Ad. Noturno = das 22:00 às 5:00

    a = start_datetime.replace(hour=22, minute=0, second=1) - timedelta(days=1)
    b = start_datetime.replace(hour=5, minute=0, second=1)
    c = start_datetime.replace(hour=22, minute=0, second=1)
    d = start_datetime.replace(hour=5, minute=0, second=1) + timedelta(days=1)

    if intervalo_datas_sobrepoem(start_datetime, end_datetime, a, b) or \
            intervalo_datas_sobrepoem(start_datetime, end_datetime, c, d):
        # timedelta já lida com o problema de normalizar valores
        # negativos similar a regra do complemento de 2.
        secs = (end_datetime - start_datetime).seconds
        hours = secs / 3600
        mins = secs % 3600 // 60

        # certifica o máx de horas recebidas nessa modalidade
        if secs > 25200:  # 7 horas = 25200 segundos
            hours = 7
            mins = 0

        return hours
    else:
        return 0


def calcula_horas_em_dobro(start_datetime, end_datetime):  # todo
    # Horas em Dobro = domingos e feriados

    hours = 0
    mins = 0

    if start_datetime.weekday() == 6 or eh_feriado(start_datetime):
        if start_datetime.date() == end_datetime.date():
            slice_datetime = start_datetime.replace(hour=end_datetime.hour,
                                                    minute=end_datetime.minute)
        else:
            slice_datetime = start_datetime.replace(hour=23, minute=59, second=59)

        secs = (slice_datetime - start_datetime).seconds
        hours += secs / 3600
        mins += secs % 3600 // 60

    elif end_datetime.weekday() == 6 or eh_feriado(end_datetime):
        if start_datetime.date() == end_datetime.date():
            slice_datetime = end_datetime.replace(hour=start_datetime.hour,
                                                  minute=start_datetime.minute)
        else:
            slice_datetime = end_datetime.replace(hour=0, minute=0, second=1)
            
        secs = (slice_datetime - end_datetime).seconds
        hours += secs / 3600
        mins += secs % 3600 // 60

    return hours


def calcula_horas_extras(start_datetime, end_datetime):
    # Horas Extra = das 18:00 às 5:00

    a = start_datetime.replace(hour=18, minute=00, second=1) - timedelta(days=1)
    b = start_datetime.replace(hour=5, minute=00, second=1)
    c = start_datetime.replace(hour=18, minute=00, second=1)
    d = start_datetime.replace(hour=5, minute=00, second=1) + timedelta(days=1)

    if intervalo_datas_sobrepoem(start_datetime, end_datetime, a, b) or \
            intervalo_datas_sobrepoem(start_datetime, end_datetime, c, d):

        secs = (end_datetime - start_datetime).seconds
        hours = secs / 3600
        mins = secs % 3600 // 60

        if secs > 39600:  # 11 horas = 39600 segundos
            hours = 11
            mins = 0

        return hours
    else:
        return 0


def intervalo_datas_sobrepoem(start_datetime, end_datetime,
                              start_slice, end_slice):
    return start_datetime <= end_slice and start_slice <= end_datetime
