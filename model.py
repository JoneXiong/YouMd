# coding=utf-8

import calendar
from datetime import datetime
import config
from tool import Dict2Object


class Models:
    """
    Models
    """
    def params(self):
        """
        parameters model for rendering templates

        reference:
            template/*/*
        """
        model ={
            'entries':None,
            'entry':None,
            'pager':None,
            'archive':None,
            'search':None,
            'subscribe':None,
            'error':None,
            'primary':{
                'abouts':None,
                'tags':None,
                'recently_entries':None,
            },
            'secondary':{
                'categories':None,
                'archive':None
            }
        }
        return Dict2Object(model)

    def entry(self, entry_type):
        """
        entry model for both entry and page

        args:
            entry_type: entry or page
                        entry is the one you'll post usually
                        page is just the one fulfills other parts of the blog, such as /about.html page

        reference:
            tempate/entry.html, templage/modules/entry.html
        """
        model = {
                 'author':{
                        'name':config.author,
                        'url':config.home
                           },
                 'path':'the path of the entry',
                 'name':'the displayed name of the entry',
                 'raw_url':'the url of the raw format of this entey',
                 'update_url':'the url of the raw update',
                 'header':'the header of the raw',
                 'url':'the url of the entry in this blog',
                 'type':entry_type,
                 'status':'published',
                 'time':None,
                 'date':None,
                 'excerpt':'the excerpt of the entry',
                 'content':'the content of the entry',
                 'html':'the html content of the entry',
                 'tags':[],
                 'categories':[],
                 'count':0,
                 'raw_count':0,
                 'private': False
        }
        return Dict2Object(model)

    def search(self, search_type, value, total):
        """
        search model for queriery

        args:
            serach_type: seach by tag, category, keyword, and or just main index of the blog
            value: the keyword to be searched
            total: the number of result matching this search

        reference:
            template/search.html
        """
        model = {
            'type':search_type,
            'value':value,
            'title': '"' + value + '" 相关的信息如下，共 ' + str(total) + '条'
            #'title':str(total)+ ' ' + self.plurals('result', total) + ' matching "' + value + '" of ' + search_type
        }
        return  Dict2Object(model)

    def pager(self, pager_type, value, total=0, pages=1, start=config.start, limit=config.limit):
        """
        pager model for pagerbar

        args:
            pager_type: the type of this pagerbar, serach or main index
            value: current search value
            total: the number of total results
            pages: the number of pages
            start: current start page number
            limit: current page size, that is how many results displayed in one page

        reference:
            template/index.html, template/search.html
        """
        model ={
            'type':pager_type,
            'value':value,
            'total':total,
            'pages':pages,
            'start':start,
            'limit':limit,
            'pagination':[i for i in xrange(1, pages + 1)]
        }
        return Dict2Object(model)

    def archive(self, archive_type, archive_url, display, url, count=1):
        """
        archve model

        args:
            archive_type: the type of this archive, entry or raw
            archive_url: the url of this archive
            display: the title displayed
            url: current url of the archived item
            count: the number of archived items

        reference:
            template/archive.html, template/modules/archive.html
        """
        title = display + ' 共' + str(count) + '篇'
        #title = 'Archive ' + str(count) + ' '  +  self.plurals(archive_type, count) + ' of ' + display
        model = {
            'type':archive_type,
            'url':archive_url,
            'display':display,
            'title':title,
            'urls':[url],
            'count':count
        }
        return  Dict2Object(model)

    def subscribe(self, time):
        """
        subscribe model

        args:
            time: the last updated time of this blog

        reference:
            template/atom.xml
        """
        model = {
            'updated': time
        }
        return Dict2Object(model)

    def error(self, code='404', url=''):
        """
        error model

        args:
            code: error code
            url: the requested url brings out this error

        reference:
            template/error.html, template/modules/error.html
        """
        model = {
            'title': code + ' Not Found',
            'url':url,
            'statusCode':code,
            'message':'Oops! The requested url "' + url + '" could not be found...'
        }
        return Dict2Object(model)

    def about(self, about_type, prev_url=None, prev_name=None, next_url=None, next_name=None):
        """
        about model

        args:
            about_type: the type of this about, entry, or archive
            prev_url: the previous url
            prev_name: the name of previous url
            next_url: the next url
            next_name: the name of next url

        reference:
            template/widgets/about.html
        """
        model = {
            'type':about_type,
            'display':about_type.title(),
            'prev_url':prev_url,
            'prev_name':prev_name,
            'next_url':next_url,
            'next_name':next_name
        }
        return Dict2Object(model)

    def tag(self, tag, url):
        """
        tag model

        args:
            tag: the tag
            url: the entry url tagged by this tag

        reference:
            template/modules/tag.html, template/widgets/tag.html
        """
        model = {
            'name':tag,
            'count':1,
            'rank':config.ranks,
            'urls':[url]
        }
        return  Dict2Object(model)

    def category(self, category, url):
        """
        category model

        args:
            category: the category
            url: the entry url in this category

        reference:
            template/modules/category.html, template/widgets/category.html
        """
        model = {
            'name':category,
            'count':1,
            'rank':1,
            'subs':[],
            'urls':[url]
        }
        return  Dict2Object(model)

    def calendar(self, date):
        """
        calendar widget

        args:
            date: the date of current calendar

        reference:
            template/widgets/calendar.html
        """
        calendar.setfirstweekday(calendar.SUNDAY)
        ym = date[:len('yyyy-mm')]
        y, m, _ = [int(i) for i in date.split('-')]
        _, n = calendar.monthrange(y, m)
        urls = [None for _ in range(0, n + 1)]
        urls[0] = ''
        model = {
            'month':ym,
            'display':datetime(int(y), int(m), 1).strftime('%B %Y'),
            'days':calendar.monthcalendar(y, m),
            'urls':urls,
            'counts':[0 for _ in range(0, n+1)]
        }
        return Dict2Object(model)

    def monthly_archive(self, archive_type, month, url):
        """
        monthly archive model

        args:
            archive_type: the type of this archive
            month: current archived month
            url: the entry url of the archived item

        reference:
            template/widgets/archive.html
        """
        y, m , _ = month.split('/')
        display = datetime(int(y), int(m), 1).strftime('%B %Y')
        archive_url = config.archive_url + '/' +  month
        return  self.archive(archive_type, archive_url, display, url, 1)

    def plurals(self, key, count=0):
        """
        words model for its plural or singular form

        args:
            key: singular word
            count: 0, 1 or any number bigger than 1
        """
        words = {
            'entry':'entries',
            'raw':'raws',
            'tag':'tags',
            'category':'categories',
            'result':'results'
        }
        if count > 1 and not words.get(key) == None:
            return words.get(key)
        return key

    def types(self):
        """
        types model for miscellanies
        """
        model = {
        'blog':'blog',
        'entry':'entry',
        'page':'page',
        'raw':'raw',
        'query':'query',
        'tag':'tag',
        'category':'category',
        'index':'index',
        'add':'add',
        'delete':'delete',
        'archive':'archive',
        'all':'全部'
        }
        return Dict2Object(model)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
