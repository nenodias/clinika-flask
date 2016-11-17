# -*- coding: utf-8 -*-
import json
from pdb import set_trace
from flask import (Blueprint, render_template, request, redirect, url_for, flash, 
    jsonify, render_template, Response)
from app import auth_require
from app.db import db, especialidades as _table, tupla_status

especialidade_blueprint = Blueprint('especialidade', __name__)

@especialidade_blueprint.route('/')
@auth_require()
def index():
    contexto = {}
    _descricao = request.args.get('descricao', '')
    _status = request.args.get('status', '')
    contexto['tupla_status'] = tupla_status
    contexto['model'] = {
        'descricao':_descricao,
        'status':_status
    }
    return render_template('especialidade/consulta.html', **contexto)

@especialidade_blueprint.route('/form/', defaults={'pk':None}, methods = ['post', 'get'])
@especialidade_blueprint.route('/form/<pk>', methods = ['post', 'get'])
@auth_require()
def form(pk):
    #Pega os dados dos campos na tela
    contexto = {}
    contexto['model'] = {}
    contexto['tupla_status'] = tupla_status
    if request.method == 'POST':
        descricao = request.form.get("descricao")
        status = request.form.get("status")
      
        #Criar dicionário com os dados
        dicionario = {
            "descricao":descricao,
            "status": bool(status),
        }
        mensagem = None
        try:
            contexto['tipo_mensagem'] = 'success'
            if pk:
                dicionario['id'] = pk
                id_cadastro = _table.update(dicionario,['id'])
                flash( u'Especialidade {0} atualizada com sucesso'.format(id_cadastro), 'success')
            else:
                id_cadastro = _table.insert(dicionario,['id'])
                flash( u'Especialidade {0} cadastrada com sucesso'.format(id_cadastro), 'success')
            return redirect(url_for('especialidade.index'))
        except:
            contexto['mensagem'] = u'Erro ao cadastrar especialidade'
            contexto['tipo_mensagem'] = 'danger'
    elif pk:
        data = _table.find_one(id=pk)
        contexto['model'] = dict(data)
    return render_template('especialidade/cadastro.html', **contexto)


@especialidade_blueprint.route('/delete/<pk>', methods = ['post'])
@auth_require()
def delete(pk):
    data = _table.find_one(id=pk)
    if data:
        if _table.delete(id=pk):
            return '', 200
    return '',404

@especialidade_blueprint.route('/ajax', methods = ['get'])
@auth_require()
def ajax():
    _limit = int(request.args.get('limit','10'))
    _offset = int(request.args.get('offset','0'))
    _descricao = request.args.get('descricao', '')
    _status = request.args.get('status', '')
    items = []
    params = {}
    sql = 'SELECT * FROM {0} WHERE 1 = 1 '.format(_table.table.name)
    if _descricao:
        params['descricao'] = '%'+_descricao+'%'
        sql += ' AND descricao like :descricao '
    if _status:
        params['status'] = 1 if _status == 'True' else 0
        sql += ' AND status = :status '
    
    sql += ' LIMIT :offset,:limit'
    params['offset'] = _offset
    params['limit'] = _limit

    try:
        fetch = db.engine.execute(sql, params)
        colunas = fetch.keys()
        for dado in fetch:
            items.append( dict(zip(colunas, dado)) )
    except Exception as ex:
        print(ex)
    return Response(response=json.dumps( items ), status=200, mimetype="application/json")

@especialidade_blueprint.route('/count', methods = ['get'])
@auth_require()
def count():
    _descricao = request.args.get('descricao', '')
    _status = request.args.get('status', '')
    items = []
    params = {}
    sql = 'SELECT COUNT(1) as count FROM {0} WHERE 1 = 1 '.format(_table.table.name)
    if _descricao:
        params['descricao'] = '%'+_descricao+'%'
        sql += ' AND descricao like :descricao '
    if _status:
        params['status'] = 1 if _status == 'True' else 0
        sql += ' AND status = :status '
    try:
        fetch = db.engine.execute(sql, params)
        colunas = fetch.keys()
        for dado in fetch:
            item = dict(zip(colunas, dado))
            items.append( item )
    except Exception as ex:
        print(ex)
    return Response(response=json.dumps( items[0] ), status=200, mimetype="application/json")

@especialidade_blueprint.route('/ajax/<pk>', methods = ['get'])
@auth_require()
def ajax_by_id(pk):
    data = _table.find_one(id=pk)
    if data:
        return Response(response=json.dumps( data ), status=200, mimetype="application/json")
    return '',404
