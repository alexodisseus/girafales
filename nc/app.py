import admin
import contest
import model
import panel


from flask import Flask
from flask_bootstrap import Bootstrap4


db = model


app = Flask(__name__)
app.config['TITLE'] = "Simulador de Conncurso - Girafales"
app.secret_key = b'guerra aos senhores'


admin.configure(app)
contest.configure(app)
panel.configure(app)
db.configure(app)

Bootstrap4(app)