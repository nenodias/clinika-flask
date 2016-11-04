# -*- coding: utf-8 -*-
from flask import (Flask, request, redirect, url_for, flash, 
    jsonify,render_template, Blueprint)
from app import db

app = Flask(__name__)

from app import controller