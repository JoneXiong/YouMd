# coding=utf-8

from mole import route, run, static_file, error,get, post, put, delete
from mole.template import template
from mole import request
from mole import response
from mole.mole import json_dumps

media_prefix = 'static'
@route('/%s/:file#.*#'%media_prefix)
def media(file):
    return static_file(file, root='./static')

@route('/')
def index():
    return template('index')
