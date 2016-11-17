# -*- coding: utf-8 -*-
from app import app, request, render_template, redirect, session, auth_require, url_for
from medico_blueprint import medico_blueprint
from paciente_blueprint import paciente_blueprint
from agendamento_blueprint import agendamento_blueprint
from especialidade_blueprint import especialidade_blueprint

@app.route('/login', methods=['POST', 'GET'])
def login():
    contexto = {}
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        if usuario == 'admin' and senha == '123':
            session['login'] = True
            return redirect(url_for('index'))
        else:
            contexto['tipo_mensagem'] = u'danger'
            contexto['mensagem'] = u'Usuário ou senha inválidos'

    return render_template('login.html', **contexto), 200


@app.route('/logout')
def logout():
    if 'login' in session:
        del session['login']
    return redirect(url_for('login'))

@app.route('/')
@auth_require()
def index():
    return render_template('index.html'), 200

app.register_blueprint(medico_blueprint, url_prefix='/medico')
app.register_blueprint(paciente_blueprint, url_prefix='/paciente')
app.register_blueprint(agendamento_blueprint, url_prefix='/agendamento')
app.register_blueprint(especialidade_blueprint, url_prefix='/especialidade')