# -*- coding: utf-8 -*-
import json
from datetime import datetime
from flask import (Blueprint, render_template, request, redirect, url_for, flash, 
    jsonify, render_template, Response)
from app import auth_require
from app.db import db, agendamentos as _table

agendamento_blueprint = Blueprint('agendamento', __name__)

@agendamento_blueprint.route('/')
@auth_require()
def index():
    contexto = {}
    _id_medico = request.args.get('id_medico', '')
    _id_paciente = request.args.get('id_paciente', '')
    _data = request.args.get('data', '')
    contexto['model'] = {
        'id_medico':_id_medico,
        'id_paciente':_id_paciente,
        'data':_data
    }
    return render_template('agendamento/consulta.html', **contexto)

@agendamento_blueprint.route('/form/', defaults={'pk':None}, methods = ['post', 'get'])
@agendamento_blueprint.route('/form/<pk>', methods = ['post', 'get'])
@auth_require()
def form(pk):
    #Pega os dados dos campos na tela
    contexto = {}
    contexto['model'] = {}
    if request.method == 'POST':
        id_medico = request.form.get("id_medico")
        id_paciente = request.form.get("id_paciente")
        data = request.form.get("data")
        hora = request.form.get("hora")
      
        #Criar dicionário com os dados
        dicionario = {
            "id_medico": int(id_medico),
            "id_paciente": int(id_paciente),
            "data":datetime.strptime(data, '%Y-%m-%d').date(),
            "hora":hora
        }
        mensagem = None
        try:
            contexto['tipo_mensagem'] = 'success'
            if pk:
                dicionario['id'] = pk
                id_cadastro = _table.update(dicionario,['id'])
                flash( u'Agendamento {0} atualizado com sucesso'.format(id_cadastro), 'success')
            else:
                id_cadastro = _table.insert(dicionario,['id'])
                flash( u'Agendamento {0} cadastrado com sucesso'.format(id_cadastro), 'success')
            return redirect(url_for('agendamento.index'))
        except:
            contexto['mensagem'] = u'Erro ao cadastrar Agendamento'
            contexto['tipo_mensagem'] = 'danger'
    elif pk:
        data = _table.find_one(id=pk)
        contexto['model'] = dict(data)
    return render_template('agendamento/cadastro.html', **contexto)


@agendamento_blueprint.route('/delete/<pk>', methods = ['post'])
@auth_require()
def delete(pk):
    data = _table.find_one(id=pk)
    if data:
        if _table.delete(id=pk):
            return '', 200
    return '',404

@agendamento_blueprint.route('/ajax', methods = ['get'])
@auth_require()
def ajax():
    _limit = int(request.args.get('limit','10'))
    _offset = int(request.args.get('offset','0'))
    _id_medico = request.args.get('id_medico', '')
    _id_paciente = request.args.get('id_paciente', '')
    _data = request.args.get('data', '')
    items = []
    params = {}
    sql = 'SELECT * FROM {0} WHERE 1 = 1 '.format(_table.table.name)
    if _id_medico:
        params['id_medico'] = int(_id_medico)
        sql += ' AND id_medico = :id_medico '
    if _id_paciente:
        params['id_paciente'] = int(_id_paciente)
        sql += ' AND id_paciente = :id_paciente '

    if _data:
        params['data'] = datetime.strptime(_data, '%Y-%m-%d').date()
        sql += ' AND data = :data '
    
    sql += ' LIMIT :offset,:limit'
    params['offset'] = _offset
    params['limit'] = _limit

    try:
        fetch = db.engine.execute(sql, params)
        colunas = fetch.keys()
        for dado in fetch:
            item = dict(zip(colunas, dado))
            items.append( item )
    except Exception as ex:
        print(ex)
    return Response(response=json.dumps( items ), status=200, mimetype="application/json")

@agendamento_blueprint.route('/count', methods = ['get'])
@auth_require()
def count():
    _id_medico = request.args.get('id_medico', '')
    _id_paciente = request.args.get('id_paciente', '')
    _data = request.args.get('data', '')
    items = []
    params = {}
    sql = 'SELECT COUNT(1) as count FROM {0} WHERE 1 = 1 '.format(_table.table.name)
    if _id_medico:
        params['id_medico'] = int(_id_medico)
        sql += ' AND id_medico = :id_medico '
    if _id_paciente:
        params['id_paciente'] = int(_id_paciente)
        sql += ' AND id_paciente = :id_paciente '

    if _data:
        params['data'] = datetime.strptime(_data, '%Y-%m-%d').date()
        sql += ' AND data = :data '
    try:
        fetch = db.engine.execute(sql, params)
        colunas = fetch.keys()
        for dado in fetch:
            item = dict(zip(colunas, dado))
            items.append( item )
    except Exception as ex:
        print(ex)
    return Response(response=json.dumps( items[0] ), status=200, mimetype="application/json")

@agendamento_blueprint.route('/ajax/<pk>', methods = ['get'])
@auth_require()
def ajax_by_id(pk):
    data = _table.find_one(id=pk)
    if data:
        return Response(response=json.dumps( data ), status=200, mimetype="application/json")
    return '',404
