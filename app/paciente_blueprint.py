# -*- coding: utf-8 -*-
from flask import (Blueprint, render_template, request, redirect, url_for, flash, 
    jsonify, render_template)
from app import db

paciente_blueprint = Blueprint('paciente', __name__)