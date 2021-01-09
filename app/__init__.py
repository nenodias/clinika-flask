# -*- coding: utf-8 -*-
from flask import (Flask, request, redirect, url_for, flash, 
    jsonify,render_template, Blueprint, session)
from app.db import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'projeto-luiz'

from app.authentication import auth_require
from app import controller