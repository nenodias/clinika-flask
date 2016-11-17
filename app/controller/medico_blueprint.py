# -*- coding: utf-8 -*-
import json
from flask import (Blueprint, render_template, request, redirect, url_for, flash, 
    jsonify, render_template, Response)
from app import auth_require
from app.db import db, medicos as _table, tupla_status, tupla_estado, tupla_area

medico_blueprint = Blueprint('medico', __name__)

@medico_blueprint.route('/')
@auth_require()
def index():
    contexto = {}
    _nome = request.args.get('nome', '')
    _id_especialidade = request.args.get('id_especialidade', '')
    contexto['tupla_status'] = tupla_status
    contexto['tupla_area'] = tupla_area
    contexto['model'] = {
        'nome':_nome,
        'id_especialidade':_id_especialidade
    }
    return render_template('medico/consulta.html', **contexto)

@medico_blueprint.route('/form/', defaults={'pk':None}, methods = ['post', 'get'])
@medico_blueprint.route('/form/<pk>', methods = ['post', 'get'])
@auth_require()
def form(pk):
    #Pega os dados dos campos na tela
    contexto = {}
    contexto['model'] = {}
    contexto['tupla_status'] = tupla_status
    contexto['tupla_estado'] = tupla_estado
    contexto['tupla_area'] = tupla_area
    if request.method == 'POST':
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")
        crm = request.form.get("crm")
        status = request.form.get("status")
        especialidade = request.form.get("id_especialidade")
        area = request.form.get("area")
        numero = request.form.get("numero")
        rua = request.form.get("numero")
        bairro = request.form.get("bairro")
        cidade = request.form.get("cidade")
        estado = request.form.get("estado")
        telefone = request.form.get("telefone")

        dicionario = {
            "nome": nome,
            "cpf": cpf,
            "crm": crm,
            "status": status,
            "id_especialidade": especialidade,
            "area": area,
            "numero": numero,
            "rua": rua,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "telefone": telefone
        }
        mensagem = None
        try:
            contexto['tipo_mensagem'] = 'success'
            if pk:
                dicionario['id'] = pk
                id_cadastro = _table.update(dicionario,['id'])
                flash( u'Médico {0} atualizado com sucesso'.format(id_cadastro), 'success')
            else:
                id_cadastro = _table.insert(dicionario,['id'])
                flash( u'Médico {0} cadastrado com sucesso'.format(id_cadastro), 'success')
            return redirect(url_for('medico.index'))
        except:
            contexto['mensagem'] = u'Erro ao cadastrar médico'
            contexto['tipo_mensagem'] = 'danger'
    elif pk:
        data = _table.find_one(id=pk)
        contexto['model'] = dict(data)
    return render_template('medico/cadastro.html', **contexto)


@medico_blueprint.route('/delete/<pk>', methods = ['post'])
@auth_require()
def delete(pk):
    data = _table.find_one(id=pk)
    if data:
        if _table.delete(id=pk):
            return '', 200
    return '',404

@medico_blueprint.route('/ajax', methods = ['get'])
@auth_require()
def ajax():
    _limit = int(request.args.get('limit','10'))
    _offset = int(request.args.get('offset','0'))
    _nome = request.args.get('nome', '')
    _id_especialidade = request.args.get('id_especialidade', '')
    items = []
    params = {}
    sql = 'SELECT * FROM {0} WHERE 1 = 1 '.format(_table.table.name)
    if _nome:
        params['nome'] = '%'+_nome+'%'
        sql += ' AND nome like :nome '
    if _id_especialidade:
        params['id_especialidade'] = int(_id_especialidade)
        sql += ' AND id_especialidade = :id_especialidade '
    
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

@medico_blueprint.route('/count', methods = ['get'])
@auth_require()
def count():
    _nome = request.args.get('nome', '')
    _id_especialidade = request.args.get('id_especialidade', '')
    items = []
    params = {}
    sql = 'SELECT COUNT(1) as count FROM {0} WHERE 1 = 1 '.format(_table.table.name)
    if _nome:
        params['nome'] = '%'+_nome+'%'
        sql += ' AND nome like :nome '
    if _id_especialidade:
        params['id_especialidade'] = int(_id_especialidade)
        sql += ' AND id_especialidade = :id_especialidade '
    try:
        fetch = db.engine.execute(sql, params)
        colunas = fetch.keys()
        for dado in fetch:
            item = dict(zip(colunas, dado))
            items.append( item )
    except Exception as ex:
        print(ex)
    return Response(response=json.dumps( items[0] ), status=200, mimetype="application/json")

@medico_blueprint.route('/ajax/<pk>', methods = ['get'])
@auth_require()
def ajax_by_id(pk):
    data = _table.find_one(id=pk)
    if data:
        return Response(response=json.dumps( data ), status=200, mimetype="application/json")
    return '',404
