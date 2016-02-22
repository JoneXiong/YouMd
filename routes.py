# coding=utf-8
import os
import datetime

from mole import route, run, static_file, error,get, post, put, delete
from mole.template import template
from mole import request
from mole import response
from mole.mole import json_dumps
from mole import redirect
from mole.sessions import get_current_session, authenticator

import config
from __init__ import entryService

media_prefix = 'static'
auth_required = authenticator(login_url = '/auth/login')

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
@auth_required()
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

@route('/private_raw:url#.*#')
@auth_required()
def PrivateRaw(url):
    url = config.raw_url + url
    raw = entryService.find_raw(url)
    if not raw == None:
        response.headers['Content-Type'] = 'text/plain'
        response.headers['Content-Encoding'] = 'utf-8'
        return raw.strip()
    params = entryService.archive(entryService.types.raw, url, private=True)
    if params.entries  == None:
        return template('error', params=params, config=config)
    return template('private', params=params, config=config)


@route('/update:url#.*#')
@auth_required()
def Update(url):
    url = config.raw_url + url
    return template('update', raw_url=url)


@route('/update_save', method='POST')
# @auth_required()
def UpdateSave():
    session = get_current_session()
    username = session.get('username','')
    if not username:
        return {'code': -2, 'msg': '未登录'}
    
    raw_url = request.POST.get("raw_url",'')
    content = request.POST.get("content",'').strip()
    
    entry_url = raw_url.replace(config.raw_url, config.entry_url).replace(config.raw_suffix, config.url_suffix)
    entry = entryService.find_by_url(entryService.types.entry, entry_url).entry
    if not entry:
        page_url = raw_url.replace(config.raw_url, '').replace(config.raw_suffix, config.url_suffix)
        entry = entryService.find_by_url(entryService.types.page, page_url).entry
    
    m_file = open(entry.path, 'w')
    m_file.write('%s\n%s'%(entry.header,content) )
    m_file.close()
    entryService.add_entry(False, entry.path, entry.private)
    return {'code': 0, 'msg': '更新成功'}

@route('/delete_post', method='POST')
def DeletePost():
    session = get_current_session()
    username = session.get('username','')
    if not username:
        return {'code': -2, 'msg': '未登录'}
    
    raw_url = request.POST.get("raw_url",'')
    entry_url = raw_url.replace(config.raw_url, config.entry_url).replace(config.raw_suffix, config.url_suffix)
    entry = entryService.find_by_url(entryService.types.entry, entry_url).entry
    entryService.delete_entry(entry.path)
    os.remove(entry.path)
    
    if entry.private:
        try:
            print 'deeeee',entry.path
            entryService.private_list.remove(entry.path)
        except:pass
        entryService.save_private()
    
    return {'code': 0, 'msg': '删除成功'}


@route('/publish', method='POST')
@auth_required()
def publish():
    name = request.POST.get("name",None)
    title = request.POST.get("title",None)
    cat = request.POST.get("cat",'')
    tag = request.POST.get("tag",'')
    private = request.POST.get("private",'')
    print '---------',private,type(private)

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
    path = 'raw/entry/%s-%s.md'%(m_date, name)
    m_file = open(path, 'w+')
    m_file.write('%s\n%s'%(head,content) )
    m_file.close()
    if private:
        entryService.add_entry(False, path, True)
        entryService.update_urls()
        entryService.private_list.append(path)
        entryService.save_private()
    else:
        entryService.add_entry(True, path)
    return {'code': 0, 'msg': '发布成功'}

@route('/auth/login', method=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.POST.get("username",'')
        password = request.POST.get("password",'')
        if password!=config.admin_pwd or username!=config.admin_user:
            return {'code': -1, 'msg': '用户名或密码错误'}
        else:
            session = get_current_session()
            session['username'] = config.admin_user
            return {'code': 0, 'msg': 'OK'}
    else:
        return template('auth/login.html', config=config)

@route('/auth/logout')
def logout():
    session = get_current_session()
    del session['username']
    return redirect(request.params.get('next') or '/')

@route('/robots.txt')
def robots():
    response.headers['Content-Type'] = 'text/plain'
    return template('robots.html', config=config)

@route('/sitemap.xml')
def sitemap():
    params =  entryService.search(entryService.types.index, config.subscribe_url, limit=10000)
    response.headers['Content-Type'] = 'text/xml'
    return template('sitemap.html', params=params, config=config)


if not os.path.exists(config.upload_path):
    os.makedirs(config.upload_path)
    
@route('%s/:file#.*#'%config.file_url)
def getfile(file):
    return static_file(file, root=config.upload_path)

@route('/upload', method='POST')
def upload():
    session = get_current_session()
    username = session.get('username','')
    if not username:
        return {'success': 0, 'message': '请先登录', 'url':''}
    
    uploadfile=request.files.get('editormd-image-file')
    
    tnow=datetime.datetime.now()
    parent_path = os.path.join(config.upload_path, tnow.strftime('%Y%m'))
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)
    
    m_f=("000"+str(tnow.microsecond/1000))[-3:]
    filename= tnow.strftime("%d%H%M%S")+m_f+"_" + uploadfile.filename
    upload_path = os.path.join(parent_path, filename)
    with open(upload_path, 'w+b') as f:
        f.write(uploadfile.file.read())
    url = '%s/%s/%s'%(config.file_url, tnow.strftime('%Y%m'), filename)
    return {'success': 1, 'message': '上传成功', 'url': url}