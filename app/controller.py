# -*- coding: utf-8 -*-
from app import app, request, render_template
from app.medico_blueprint import medico_blueprint
from app.paciente_blueprint import paciente_blueprint
from app.agendamento_blueprint import agendamento_blueprint


@app.route('/')
def index():
    return render_template('index.html'), 200

app.register_blueprint(medico_blueprint, url_prefix='/medico')
app.register_blueprint(paciente_blueprint, url_prefix='/paciente')
app.register_blueprint(agendamento_blueprint, url_prefix='/agendamento')