from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
db = SQLAlchemy(app)

import planilha_horas.views
import planilha_horas.api_controllers
import planilha_horas.filters.dates
import planilha_horas.filters.regras_th

