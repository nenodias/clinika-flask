# -*- coding: utf-8 -*-
from flask import (Blueprint, render_template, request, redirect, url_for, flash, 
    jsonify, render_template)
from app import db

agendamento_blueprint = Blueprint('agendamento', __name__)

@agendamento_blueprint.route('/')
def ajax_list():
    _limit = int(request.args.get('limit','10'))
    _offset = int(request.args.get('offset','0'))
    _criteria = request.args.get('search', '')
    _value = request.args.get('value', '')
    _table = db.agendamentos
    
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

@agendamento_blueprint.route('/', methods=['POST'])
def ajax_post():
    _table = db.agendamentos
    data = request.form.to_dict()
    if 'id' in data:
        operation = _table.update(data,['id'])
    else:
        operation = _table.insert(update,['id'])
    if operation:
        data = _table.find_one(id=id)
        return jsonify(data), 200
    return '',404

@agendamento_blueprint.route('/<id>', methods=['GET'])
def ajax_get(id):
    _table = db.agendamentos
    data = _table.find_one(id=id)
    if data:
        return jsonify(data), 200
    return '',404

@agendamento_blueprint.route('/<id>', methods=['PUT'])
def ajax_put(id):
    _table = db.agendamentos
    data = _table.find_one(id=id)
    update = request.form.to_dict()
    update['id'] = id
    if data:
        _table.update(update,['id'])
        data = _table.find_one(id=id)
        return jsonify(data), 200
    return '',404

@agendamento_blueprint.route('/<id>', methods=['DELETE'])
def ajax_delete(id):
    _table = db.agendamentos
    data = _table.find_one(id=id)
    if data:
        if _table.delete(id=id):
            return '', 200
    return '',404