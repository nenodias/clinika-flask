# -*- coding: utf-8 -*-
from pdb import set_trace
from flask import (Blueprint, render_template, request, redirect, url_for, flash, 
    jsonify, render_template)
from app.db import db, especialidades as _table

especialidade_blueprint = Blueprint('especialidade', __name__)

@especialidade_blueprint.route('/')
def index():
    contexto = {}
    _descricao = request.args.get('descricao', '')
    _status = request.args.get('status', '')
    contexto['tupla_status'] = ( ('', 'Selecionar'),(True, 'Ativo'),(False, 'Desativado') )
    contexto['model'] = {
        'descricao':_descricao,
        'status':_status
    }
    return render_template('especialidade/consulta.html', **contexto)

@especialidade_blueprint.route('/form/', defaults={'pk':None}, methods = ['post', 'get'])
@especialidade_blueprint.route('/form/<pk>', methods = ['post', 'get'])
def form(pk):
    #Pega os dados dos campos na tela
    contexto = {}
    contexto['model'] = {}
    contexto['tupla_status'] = ( ('', 'Selecionar'),(True, 'Ativo'),(False, 'Desativado') )
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
            if pk:
                dicionario['id'] = pk
                id_cadastro = _table.update(dicionario,['id'])
                contexto['mensagem'] = u'Especialidade {0} atualizada com sucesso'
            else:
                id_cadastro = _table.insert(dicionario,['id'])
                contexto['mensagem'] = u'Especialidade {0} cadastrada com sucesso'
        except:
            contexto['mensagem'] = u'Erro ao cadastrar especialidade'
    elif pk:
        data = _table.find_one(id=pk)
        contexto['model'] = dict(data)
        print(contexto['model'])
    return render_template('especialidade/cadastro.html', **contexto)


@especialidade_blueprint.route('/delete/<pk>', methods = ['post'])
def delete(pk):
    data = _table.find_one(id=id)
    if data:
        if _table.delete(id=id):
            return '', 200
    return '',404

@especialidade_blueprint.route('/ajax', methods = ['get'])
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
        params['status'] = int(_status)
        sql += ' AND status = :status '
    sql += ' LIMIT {offset},{limit}'.format(offset=_offset, limit=_limit)
    try:
        fetch = db.engine.execute(sql, params)
        colunas = fetch.keys()
        for dado in fetch:
            item = dict(zip(colunas, dado))
            items.append( item )
    except Exception as ex:
        print(ex)
    return jsonify( items )

@especialidade_blueprint.route('/count', methods = ['get'])
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
        params['status'] = _status
        sql += ' AND status = :status '
    try:
        fetch = db.engine.execute(sql, params)
        colunas = fetch.keys()
        for dado in fetch:
            item = dict(zip(colunas, dado))
            items.append( item )
    except Exception as ex:
        print(ex)
    return jsonify( items[0] )

@especialidade_blueprint.route('/ajax/<pk>', methods = ['get'])
def ajax_by_id(pk):
    data = _table.find_one(id=id)
    if data:
        return jsonify(data), 200
    return '',404
