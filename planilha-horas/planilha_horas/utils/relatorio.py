import locale
from datetime import *
from math import floor

import openpyxl
import openpyxl.styles

from ..utils.dates import DATE_FORMAT
from ..filters import regras_th
from ..models import Eventos


def gera_relatorio_consolidado():
    locale.setlocale(locale.LC_ALL, '')
    from io import BytesIO
    output = BytesIO()

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "FOLHA MENSAL"

    agora = datetime.now()
    # bug janeiro - 1
    data_inicial = agora.replace(day=15, month=agora.month - 1, hour=0,
                                 minute=0, second=0, microsecond=0)
    data_final = agora.replace(day=15, hour=0, minute=0, second=0,
                               microsecond=0)

    mes_passado = data_inicial.strftime("%B").title()
    mes_atual = data_final.strftime("%B").title()

    worksheet.merge_cells('A1:J1')
    worksheet.row_dimensions[1].height = 50
    worksheet['A1'].value = ("Planilha de Lançamentos de Folha\n"
                             "Mês de Competência: {}/{}".format(mes_passado,
                                                                mes_atual))
    worksheet['A1'].alignment = openpyxl.styles.Alignment(vertical="center",
                                                          horizontal="center",
                                                          wrap_text=True)

    worksheet.column_dimensions['A'].width = 12
    worksheet.column_dimensions['B'].width = 12
    worksheet.column_dimensions['C'].width = 30
    worksheet.column_dimensions['D'].width = 17
    worksheet.column_dimensions['E'].width = 15
    worksheet.column_dimensions['F'].width = 20
    worksheet.column_dimensions['G'].width = 10
    worksheet.column_dimensions['H'].width = 15
    worksheet.column_dimensions['I'].width = 20
    worksheet.column_dimensions['J'].width = 20

    worksheet.auto_filter.ref = "A2:J1000000"

    colunas = ('EMPRESA',
               'MATRÍCULA',
               'NOME',
               'TIPO DE EVENTO',
               'COD. EVENTO',
               'DESCRIÇÃO EVENTO',
               'VALOR',
               'QTDE HORAS',
               'DATA INÍCIO',
               'DATA FIM')
    worksheet.append(colunas)

    for info in consolida_eventos_por_associado(Eventos.query.all(),
                                                data_inicial, data_final):
        for evento in info['eventos'].values():
            worksheet.append((info['empresa'], info['matricula'], info['nome'],
                              'PROVENTO', evento['codigo'], evento['descricao'],
                              0, '='+str(floor(evento['duracao'] * 100) / 100)+'/24',
                              data_inicial, data_final))

    for _cell in worksheet['H']:
        _cell.number_format = 'hh:mm'

    name = '{}-{}-ProventosEDescontos-{}{}.xlsx'.format(data_inicial.year,
                                                        'CAP', mes_passado,
                                                        mes_atual)
    workbook.save(output)
    output.seek(0)

    return output, name


def consolida_eventos_por_associado(eventos, data_inicial, data_final):
    associados = {}
    for evento in eventos:

        if (datetime.strptime(evento.data_inicio,
                              DATE_FORMAT) < data_inicial or
                    datetime.strptime(evento.data_inicio,
                                      DATE_FORMAT) > data_final):
            continue

        if evento.associado.matricula not in associados:
            associados[evento.associado.matricula] = {
                'matricula': evento.associado.matricula,
                'nome': evento.associado.nome,
                'empresa': evento.associado.empresa.codigo,
                'eventos': {}
            }

        for tipo in regras_th.tipo_evento(evento.data_inicio, evento.data_fim):
            if tipo['codigo'] not in associados[evento.associado.matricula][
                'eventos']:
                associados[evento.associado.matricula]['eventos'][
                    tipo['codigo']] = {
                    'codigo': '',
                    'descricao': '',
                    'duracao': 0
                }

            associados[evento.associado.matricula]['eventos'][tipo['codigo']][
                'codigo'] = tipo['codigo']
            associados[evento.associado.matricula]['eventos'][tipo['codigo']][
                'descricao'] = tipo['tipo']
            associados[evento.associado.matricula]['eventos'][tipo['codigo']][
                'duracao'] += tipo['duracao']

    return associados.values()
