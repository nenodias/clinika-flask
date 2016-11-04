# -*- coding: utf-8 -*-
from flask import (Blueprint, render_template, request, redirect, url_for, flash, 
    jsonify, render_template)
from app import db

medico_blueprint = Blueprint('medico', __name__)

@medico_blueprint.route('/')
def index():
    return u'Olá Mundo'