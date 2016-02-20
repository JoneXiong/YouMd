# coding=utf-8

name = u'MarkDown Doc'
home = 'https://github.com/JoneXiong/YouMd'
author = 'YouMd'
disqus = '"webpymdblog=="'
template_dir = 'template'
entry_dir = 'raw/entry'
page_dir = 'raw/page'
tweet_dir = 'raw/tweet'
static_dir = './static'
url_suffix = '.html'
raw_suffix = '.md'
index_url = '/'
entry_url = '/blog'
tweet_url = '/tweet'
archive_url = '/archive'
about_url = '/about.html'
subscribe_url = '/atom.xml'
error_url = '/error.html'
favicon_url = '/favicon.ico'
search_url = '/search'

static_url = '/static'

raw_url = '/raw'
update_url = '/update'
other_url = '(.+)'
start = 1
limit = 5
pagination = 15
search_holder = 'search all site'
time_fmt = '%Y-%m-%d %H:%M:%S'
date_fmt = '%Y-%m-%d'
url_fmt = 'yyyy/mm/dd'
url_date_fmt = '%Y/%m/%d'
recently = 10
ranks = 10
subscribe = 10
cache = False
debug = True

use_comment = False
backend_md = False
admin_pwd = 'youmd'
admin_user = 'admin'

def cur_user():
    from mole.sessions import get_current_session
    session = get_current_session()
    return session.get('username','')

private_store = 'private.data'
private_url = '/private_raw'

upload_path = './upload'
file_url = '/files'