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


especialidade_rest_blueprint = Blueprint('especialidade_rest', __name__)

@especialidade_rest_blueprint.route('/')
def ajax_list():
    _limit = int(request.args.get('limit','10'))
    _offset = int(request.args.get('offset','0'))
    _criteria = request.args.get('search', '')
    _value = request.args.get('value', '')
    _table = db.especialidades
    
    count = _table.count()
    total_pages = count // _limit;
    page = _offset + 1;
    items = []

    search = {
        '_limit':_limit,
        '_offset':_offset,
    }
    number_results = 0
    if _criteria and _value:
        search[_criteria] = _value
    try:
        for item in _table.find(**search):
            items.append( item )
            number_results += 1
    except Exception as ex:
        print(ex)
    data = {
        'page':page,
        'total_pages':total_pages,
        'results': number_results,
        'total':count,
        'data':items
    }
    return jsonify( data )

@especialidade_rest_blueprint.route('/', methods=['POST'])
def ajax_post():
    _table = db.especialidades
    data = request.form.to_dict()
    if 'id' in data:
        operation = _table.update(data,['id'])
    else:
        operation = _table.insert(update,['id'])
    if operation:
        data = _table.find_one(id=id)
        return jsonify(data), 200
    return '',404

@especialidade_rest_blueprint.route('/<id>', methods=['GET'])
def ajax_get(id):
    _table = db.especialidades
    data = _table.find_one(id=id)
    if data:
        return jsonify(data), 200
    return '',404

@especialidade_rest_blueprint.route('/<id>', methods=['PUT'])
def ajax_put(id):
    _table = db.especialidades
    data = _table.find_one(id=id)
    update = request.form.to_dict()
    update['id'] = id
    if data:
        _table.update(update,['id'])
        data = _table.find_one(id=id)
        return jsonify(data), 200
    return '',404

@especialidade_rest_blueprint.route('/<id>', methods=['DELETE'])
def ajax_delete(id):
    _table = db.especialidades
    data = _table.find_one(id=id)
    if data:
        if _table.delete(id=id):
            return '', 200
    return '',404