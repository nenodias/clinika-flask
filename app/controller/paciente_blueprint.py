# -*- coding: utf-8 -*-
import json
from pdb import set_trace
from flask import (Blueprint, render_template, request, redirect, url_for, flash, 
    jsonify, render_template, Response)
from app.db import db, pacientes as _table

paciente_blueprint = Blueprint('paciente', __name__)

@paciente_blueprint.route('/')
def index():
    contexto = {}
    _nome = request.args.get('nome', '')
    _cpf = request.args.get('cpf', '')
    contexto['model'] = {
        'nome':_nome,
        'cpf':_cpf
    }
    return render_template('paciente/consulta.html', **contexto)

@paciente_blueprint.route('/form/', defaults={'pk':None}, methods = ['post', 'get'])
@paciente_blueprint.route('/form/<pk>', methods = ['post', 'get'])
def form(pk):
    #Pega os dados dos campos na tela
    contexto = {}
    contexto['model'] = {}
    contexto['tupla_plano'] = ( 
        ('', 'Selecionar'),
        ('SEM_COBERTURA', 'Sem Cobertura'),
        ('COBERTURA_PARCIAL', 'Cobertura parcial')
        ('COBERTURA_TOTAL', 'Cobertura total')
    )
    if request.method == 'POST':
        #Pega os dados dos campos na tela
        nome = request.form.get("nome")
        cpf = int(request.form.get("cpf"))
        telefone = request.form.get("telefone")
        plano = request.form.get("plano")
        rua = request.form.get("rua")
        numero = request.form.get("numero")
        bairro = request.form.get("bairro")
        cidade = request.form.get("cidade")
        estado = request.form.get("estado")
      
        #Criar dicionário com os dados
        dicionario = {
            "nome":nome,
            "cpf":cpf,
            "telefone": telefone,
            "plano": plano,
            "rua": rua,
            "numero": numero,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado
        }
        mensagem = None
        try:
            if pk:
                dicionario['id'] = pk
                id_cadastro = _table.update(dicionario,['id'])
                contexto['mensagem'] = u'Paciente {0} atualizado com sucesso'
            else:
                id_cadastro = _table.insert(dicionario,['id'])
                contexto['mensagem'] = u'Paciente {0} cadastrado com sucesso'
        except:
            contexto['mensagem'] = u'Erro ao cadastrar paciente'
    elif pk:
        data = _table.find_one(id=pk)
        contexto['model'] = dict(data)
    return render_template('paciente/cadastro.html', **contexto)


@paciente_blueprint.route('/delete/<pk>', methods = ['post'])
def delete(pk):
    data = _table.find_one(id=pk)
    if data:
        if _table.delete(id=pk):
            return '', 200
    return '',404

@paciente_blueprint.route('/ajax', methods = ['get'])
def ajax():
    _limit = int(request.args.get('limit','10'))
    _offset = int(request.args.get('offset','0'))
    _nome = request.args.get('nome', '')
    _cpf = request.args.get('cpf', '')
    items = []
    params = {}
    sql = 'SELECT * FROM {0} WHERE 1 = 1 '.format(_table.table.name)
    if _nome:
        params['nome'] = '%'+_nome+'%'
        sql += ' AND nome like :nome '
    if _cpf:
        params['cpf'] = int(_cpf)
        sql += ' AND cpf = :cpf '
    
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

@paciente_blueprint.route('/count', methods = ['get'])
def count():
    _nome = request.args.get('nome', '')
    _cpf = request.args.get('cpf', '')
    items = []
    params = {}
    sql = 'SELECT COUNT(1) as count FROM {0} WHERE 1 = 1 '.format(_table.table.name)
    if _nome:
        params['nome'] = '%'+_nome+'%'
        sql += ' AND nome like :nome '
    if _cpf:
        params['cpf'] = int(_cpf)
        sql += ' AND cpf = :cpf '
    try:
        fetch = db.engine.execute(sql, params)
        colunas = fetch.keys()
        for dado in fetch:
            item = dict(zip(colunas, dado))
            items.append( item )
    except Exception as ex:
        print(ex)
    return Response(response=json.dumps( items[0] ), status=200, mimetype="application/json")

@paciente_blueprint.route('/ajax/<pk>', methods = ['get'])
def ajax_by_id(pk):
    data = _table.find_one(id=pk)
    if data:
        return Response(response=json.dumps( data ), status=200, mimetype="application/json")
    return '',404
