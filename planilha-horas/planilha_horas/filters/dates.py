from datetime import *

from ..utils.dates import DATE_FORMAT
from .. import app


@app.template_filter('date_print')
def date_print(start_date):
    d = datetime.strptime(start_date, DATE_FORMAT)
    return d.strftime('%d/%m/%Y às %H:%M')


@app.template_filter('date_delta')
def date_delta(start_date, end_date):
    s = datetime.strptime(start_date, DATE_FORMAT)
    e = datetime.strptime(end_date, DATE_FORMAT)
    seconds = (e - s).seconds
    hours = seconds // 3600
    minutes = seconds % 3600 // 60

    return hours, minutes
