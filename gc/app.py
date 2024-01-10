import admin
#import quiz
import model

from flask import Flask
from flask_bootstrap import Bootstrap4


db = model


app = Flask(__name__)
app.config['TITLE'] = "Simulador de Conncurso - Girafales"
app.secret_key = b'guerra aos senhores'


admin.configure(app)
#quiz.configure(app)
db.configure(app)

Bootstrap4(app)