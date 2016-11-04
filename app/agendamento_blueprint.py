# -*- coding: utf-8 -*-
from flask import (Blueprint, render_template, request, redirect, url_for, flash, 
    jsonify, render_template)
from app import db

agendamento_blueprint = Blueprint('agendamento', __name__)