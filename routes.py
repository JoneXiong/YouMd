# coding=utf-8

from mole import route, run, static_file, error,get, post, put, delete
from mole.template import template
from mole import request
from mole import response
from mole.mole import json_dumps

import config
from __init__ import entryService

media_prefix = 'static'
@route('/%s/:file#.*#'%media_prefix)
def media(file):
    return static_file(file, root='./static')

@route('/new')
def editor():
    return template('editor')

@route('/')
def Index():
    limit = int(request.GET.get('limit', 10))
    start = int(request.GET.get('start', 1))
    params = entryService.search(entryService.types.index, config.index_url, '', start, limit)
    return template('index', params=params, config=config)

@route('/blog:url#.*#')
def Entry(url):
    if not url in ['', '/']:
        url = config.entry_url + url
        params = entryService.find_by_url(entryService.types.entry, url)
        if params.entry == None:
            return template('error', params=params, config=config)
        else:
            return template('entry', params=params, config=config)
    params = entryService.search(entryService.types.index, url)
    return template('index', params=params, config=config)

@route('/archive:url#.*#')
def Archive(url):
    url= config.archive_url + url
    params = entryService.archive(entryService.types.entry, url)
    if params.entries == None:
        return template('error', params=params, config=config)
    return template('archive', params=params, config=config)

 
@route('/about.html')
def About():
    url = config.about_url
    params = entryService.find_by_url(entryService.types.page, url)
    if params.entry == None:
        return template('error', params=params, config=config)
    return template('entry', params=params, config=config)


@route('/atom.xml')
def Subscribe():
    params =  entryService.search(entryService.types.index, config.subscribe_url)
    response.headers['Content-Type'] = 'text/xml'
    return template('atom', params=params, config=config)


@route('/search')
def Search():
    type = request.GET.get('type', entryService.types.query)
    value = request.GET.get('value', '')
    limit = int(request.GET.get('limit', config.limit))
    start = int(request.GET.get('start', config.start))
    
    url = '%s/?type=%s&value=%s&start=%d&limit=%d' % (config.search_url, type, value, start, limit)
    params = entryService.search(type, url, value, start, limit)
    if not params.entries == None:
        return template('search', params=params, config=config)
    return template('error', params=params, config=config)


@route('/raw:url#.*#')
def Raw(url):
    url = config.raw_url + url
    raw = entryService.find_raw(url)
    if not raw == None:
        response.headers['Content-Type'] = 'text/plain'
        response.headers['Content-Encoding'] = 'utf-8'
        return raw.strip()
    params = entryService.archive(entryService.types.raw, url)
    if params.entries  == None:
        return template('error', params=params, config=config)
    return template('archive', params=params, config=config)


@route('/update:url#.*#')
def Update(url):
    url = config.raw_url + url
    return template('update', raw_url=url)

@route('/update_save', method='POST')
def UpdateSave():
    raw_url = request.POST.get("raw_url",'')
    password = request.POST.get("password",'')
    if password!=config.admin_pwd:
        return {'code': -1, 'msg': '密码错误'}
    content = request.POST.get("content",'').strip()
    
    entry_url = raw_url.replace(config.raw_url, config.entry_url).replace(config.raw_suffix, config.url_suffix)
    entry = entryService.find_by_url(entryService.types.entry, entry_url).entry
    if not entry:
        page_url = raw_url.replace(config.raw_url, '').replace(config.raw_suffix, config.url_suffix)
        entry = entryService.find_by_url(entryService.types.page, page_url).entry
    
    m_file = open(entry.path, 'w')
    m_file.write('%s\n%s'%(entry.header,content) )
    m_file.close()
    entryService.add_entry(True, entry.path)
    return {'code': 0, 'msg': '更新成功'}

@route('/publish', method='POST')
def publish():
    name = request.POST.get("name",None)
    title = request.POST.get("title",None)
    cat = request.POST.get("cat",'')
    tag = request.POST.get("tag",'')
    password = request.POST.get("password",'')
    if password!=config.admin_pwd:
        return {'code': -1, 'msg': '密码错误'}
    content = request.POST.get("content",'').strip()
    
    head = '''---
layout: post
title: %s
category: %s
tags: [%s]
---
    '''%(title, cat, tag)
    import datetime
    m_date = datetime.datetime.now().strftime('%Y-%m-%d')
    path = './raw/entry/%s-%s.md'%(m_date, name)
    m_file = open(path, 'w+')
    m_file.write('%s\n%s'%(head,content) )
    m_file.close()
    entryService.add_entry(True, path)
    return {'code': 0, 'msg': '发布成功'}
