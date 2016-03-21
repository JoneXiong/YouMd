# coding=utf-8

import os
import codecs
import re
import datetime
import random
try:  
    import cPickle as pickle  
except ImportError:  
    import pickle  

import config
from model import Models
import config


class EntryService:
    """EntryService."""

    def __init__(self):
        self.entries = {}
        self.pages = {}
        self.urls = []
        self.by_tags = {}
        self.by_categories = {}
        self.by_months = {}
        self.models = Models()
        self.types = self.models.types()
        self.params = self.models.params()
        self.private_list = []
        self.all_urls = []
        self._init_entries()
        
    def add_private(self, path):
        self.private_list.append(path)
        self.save_private()
        
    def del_private(self, path):
        self.private_list.append(path)
        try:
            self.private_list.remove(path)
        except:pass
        self.save_private()
        
    def save_private(self):
        private_path = 'raw/' + config.private_store
        with open(private_path, "w") as _file:
            pickle.dump(self.private_list, _file)
            _file.close()

    def _init_entries(self):
        private_path = 'raw/' + config.private_store
        private_list = []
        if os.path.exists(private_path):
            with open(private_path, 'r') as _file:
                private_list = pickle.load(_file)
        self.private_list = private_list
        print 'private list',self.private_list
        for root, _, files in os.walk(config.entry_dir):
            for f in files:
                _path = root + '/' + f
                self.add_entry(False, _path, _path in private_list)
        for root, _, files in os.walk(config.page_dir):
            for f in files:
                self._add_page(root + '/' + f)
        self._init_miscellaneous(self.types.add, self.entries.values())

    def add_entry(self, inotified, path, private=False):
        entry = self._init_entry(self.types.entry, path, private)
        if not entry == None:
            self.entries[entry.url] = entry
            if inotified:
                self._init_miscellaneous(self.types.add, [entry])
            else:
                self.update_urls()

    def delete_entry(self, path):
        for entry in self.entries.values():
            if path == entry.path:
                self.entries.pop(entry.url)
                self._init_miscellaneous(self.types.delete, [entry])

    def _add_page(self, path):
        page = self._init_entry(self.types.page, path)
        if not page == None:
            self.pages[page.url] = page

    def _init_entry(self, entry_type, path, private=False):
        '''
        read infomation from md file
        '''
        url, raw_url, name, date, time, content =  self._init_file(path, entry_type)
        if not url == None:
            entry = self.models.entry(entry_type)
            entry.path = path
            entry.name = name
            entry.url = url
            entry.raw_url = config.raw_url + raw_url
            entry.update_url = config.update_url + raw_url
            entry.date = date
            entry.time = time
            entry.private = private
            #header, title, categories, tags = extract.parse(entry)
            print 'parse',entry.path
            with open(entry.path, 'r') as f:
                start = f.readline()
                if '---' in start.strip():
                    layout_raw = f.readline()
                    title_raw = f.readline()
                    category_raw = f.readline()
                    tags_raw = f.readline()
                    #author_raw = f.readline()
                    end = f.readline()
                    content = f.read().strip()
                    #print layout_raw,title_raw,category_raw,tags_raw
                    title = title_raw.split(':')[1].strip()
                    categories_str = category_raw.split(':')[1].strip()
                    categories = categories_str and categories_str.split(',') or []
                    tags_str = tags_raw.split(':')[1].strip()[1:-1]
                    tags = tags_str and tags_str.split(',') or []
                    header = ''.join([start, layout_raw, title_raw, category_raw, tags_raw, end])
                else:
                    title, categories, tags, header = '', [], [], ''
                
            if title:
                entry.name = title
            #content = content.replace(header.decode('utf-8'), '')
            try:
                content = content.decode('utf-8')
            except:pass
            entry.content = content
            entry.header = header
            if config.backend_md:
                import markdown
                entry.html = markdown.markdown(content,extensions=['markdown.extensions.codehilite','markdown.extensions.toc','markdown.extensions.fenced_code','markdown.extensions.tables'])
            else:
                entry.html = ''
            entry.excerpt = content[:200] + ' ... ...'
            entry.categories = categories
            entry.tags = tags
            return entry
        return None

    def _init_file(self, file_path, entry_type):
        """
        #TODO: FIXME: how to determine the publish time of an entry
        """
        content, nones = None, [None for _ in xrange(6)]
        try:
            content = codecs.open(file_path, mode='r', encoding='utf-8').read()
        except:
            return nones
        if content == None or len(content.strip()) == 0:
            return nones
        date, mtime = None, None
        name, _ = os.path.splitext(os.path.basename(file_path))
        chars = ['_' ,'-', '~']
        pattern = r'\d{4}-\d{1,2}-\d{1,2}'
        match = re.search(pattern, name)
        if match:
            y, m, d = match.group().split('-')
            try:
                date = datetime.date(int(y), int(m), int(d))
            except:
                pass
            name = name[len(match.group()):]
            for c in chars:
                if name.startswith(c):
                    name = name[1:]
        stat = os.stat(file_path)
        mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
        if date == None:
            date = mtime
        prefix, url_prefix, raw_prefix = date.strftime(config.url_date_fmt), '', ''
        if entry_type == self.types.entry:
            url_prefix = config.entry_url + '/' + prefix + '/'
            raw_prefix = '/' + prefix + '/'
        if entry_type == self.types.page:
            url_prefix = '/'
            raw_prefix = '/'
        date = date.strftime(config.date_fmt)
        time = date + mtime.strftime(config.time_fmt)[len('yyyy-mm-dd'):]
        url = url_prefix + name + config.url_suffix
        raw_url = raw_prefix + name + config.raw_suffix
        for c in chars:
            name = name.replace(c, ' ')
        return url, raw_url, name, date, time, content
    
    def update_urls(self):
        '''
        public url noupdate
        '''
        self.all_urls = sorted(self.entries.keys(), reverse=True)

    def _init_miscellaneous(self,init_type, entries):
        '''
        1. rebuild index data of the 'entries'
        2. refresh the url data
        3. refresh the right part of site page
        '''
        for entry in entries:
            self._init_tag(init_type, entry.url, entry.tags)
            self._init_category(init_type, entry.url, entry.categories)
            self._init_monthly_archive(init_type, entry.url)
        _list = []
        _pub_list = []
        for url, entry in self.entries.items():
            _list.append(url)
            if not entry.private:
                _pub_list.append(url)
        self.urls = sorted(_pub_list, reverse=True)
        self.all_urls = sorted(_list, reverse=True)
        self._init_params()

    def _init_subscribe(self):
        '''
        refresh the subscribe last update time
        '''
        time = None
        if self.urls == []:
            time = datetime.datetime.now().strftime(config.time_fmt)
        else:
            time = self.entries[self.urls[0]].time
        return self.models.subscribe(time)

    def _init_tag(self,init_type, url, tags):
        for tag in tags:
            if tag not in self.by_tags:
                if init_type == self.types.add:
                    self.by_tags[tag] = self.models.tag(tag, url)
                if init_type == self.types.delete:
                    pass
            else:
                if init_type == self.types.add:
                    if url not in self.by_tags[tag].urls:
                        self.by_tags[tag].urls.insert(0, url)
                        self.by_tags[tag].count += 1
                if init_type == self.types.delete:
                    self.by_tags[tag].count -= 1
                    self.by_tags[tag].urls.remove(url)
                    if self.by_tags[tag].count == 0:
                        self.by_tags.pop(tag)

    def _init_category(self, init_type, url, categories):
        for category in categories:
            if category not in self.by_categories:
                if init_type == self.types.add:
                    self.by_categories[category] = \
                    self.models.category(category, url)
                if init_type == self.types.delete:
                    pass
            else:
                m_category = self.by_categories[category]
                if init_type == self.types.add:
                    if url not in m_category.urls:
                        m_category.urls.insert(0, url)
                        m_category.count += 1
                if init_type == self.types.delete:
                    m_category.count -= 1
                    m_category.urls.remove(url)
                    if m_category.count == 0:
                        self.by_categories.pop(category)

    def _init_monthly_archive(self,init_type, url):
        start = len(config.entry_url) + 1
        end = start + len('/yyyy/mm')
        month = url[start:end]
        if month not in self.by_months:
            if init_type == self.types.add:
                self.by_months[month] = \
                self.models.monthly_archive(self.types.entry, month, url)
            if init_type == self.types.delete:
                pass
        else:
            if init_type == self.types.add:
                if url not in self.by_months[month].urls:
                    self.by_months[month].urls.insert(0, url)
                    self.by_months[month].count += 1
            else:
                self.by_months[month].count -= 1
                self.by_months[month].urls.remove(url)
                if self.by_months[month].count == 0:
                    self.by_months.pop(month)

    def _init_params(self):
        '''
        refresh the right part of site page
        '''
        self.params.subscribe = self._init_subscribe()
        self.params.primary.tags = self._init_tags_widget()
        self.params.primary.recently_entries = self._init_recently_entries_widget()
        self.params.secondary.categories = self._init_categories_widget()
        self.params.secondary.calendar = self._init_calendar_widget()
        self.params.secondary.archive = self._init_archive_widget()

    def _init_related_entries(self, url):
        """
        #TODO: FIXME: related entries
        """
        urls, index = [], 0
        try:
            index = self.urls.index(url)
        except:
            return None
        urls = self.urls[:index]
        urls.extend(self.urls[index + 1:])
        urls = random.sample(urls, min(len(urls), 10))
        return [self.entries.get(url) for url in sorted(urls, reverse=True)]

    def _init_abouts_widget(self, about_types=[], url=None):
        abouts = []
        for about_type in about_types:
            about = self.models.about(about_type)
            if about_type == self.types.entry and not url == None:
                try:
                    i = self.urls.index(url)
                    p, n = i + 1, i - 1
                except:
                    p, n = 999999999, -1
                if p < len(self.urls):
                    url = self.urls[p]
                    about.prev_url = url
                    about.prev_name = self.entries[url].name
                if n >= 0:
                    url = self.urls[n]
                    about.next_url = url
                    about.next_name = self.entries[url].name
            if about_type == self.types.archive:
                about.prev_url = '/'
                about.prev_name = 'main index'
            if about_type == self.types.blog:
                about.prev_url = '/'
                about.prev_name = 'main  index'
                about.next_url = config.archive_url
                about.next_name = 'archives'
            abouts.append(about)
        return abouts

    def _init_tags_widget(self):
        """
        #TODO: FIXME: calculate tags' rank
        """
        tags = sorted(self.by_tags.values(), key=lambda v:v.count, reverse=True)
        ranks = config.ranks
        div, mod = divmod(len(tags), ranks)
        if div == 0:
            ranks, div = mod, 1
        for r in range(ranks):
            s, e = r * div, (r + 1) * div
            for tag in tags[s:e]:
                tag.rank = r + 1
        return tags

    def _init_recently_entries_widget(self):
        return [self.entries[url] for url in self.urls[:config.recently]]

    def _init_calendar_widget(self):
        date = datetime.datetime.today().strftime(config.date_fmt)
        if len(self.urls)> 0:
            date = self.entries[self.urls[0]].date
        calendar = self.models.calendar(date)
        y, m = calendar.month.split('-')
        for url in self.urls:
            _, _, _, _, d, _ = url.split('/')
            prefix = config.entry_url + '/' +  y + '/' + m + '/' + d
            d = int(d)
            if url.startswith(prefix):
                calendar.counts[d] += 1
                if calendar.counts[d] > 1:
                    start = len(config.entry_url)
                    end = start + len('/yyyy/mm/dd')
                    calendar.urls[d] = config.archive_url + url[start:end]
                else:
                    calendar.urls[d] = url
            else:
                break
        return calendar

    def _init_categories_widget(self):
        return sorted(self.by_categories.values(), key=lambda c:c.name)

    def _init_archive_widget(self):
        return sorted(self.by_months.values(), key=lambda m:m.url, reverse=True)

    def _find_by_query(self, query, start, limit):
        """
        #TODO: FIXME: how to search in the content of entries
        """
        queries = [q.decode('utf-8') for q  in query.split(' ')]
        urls = []
        for query in queries:
            for entry in self.entries.values():
                if entry.private:
                    continue
                try:
                    entry.content.index(query)
                    urls.append(entry.url)
                except:
                    pass
        return self._find_by_page(sorted(urls), start, limit)

    def _find_by_page(self, urls, start, limit):
        if urls == None or start < 0 or limit <= 0:
            return [], 0
        total = len(urls)
        urls = sorted(urls, reverse=True)
        s, e = (start - 1) * limit, start * limit
        if s > total or s < 0:
            return [], 0
        return [self.entries[url] for url in urls[s:e]], total

    def _paginate(self, pager_type, value, total, start, limit):
        if limit <= 0:
            return self.models.pager(pager_type, value, total, 0, start, limit)
        pages, mod = divmod(total,limit)
        if mod > 0:
            pages += 1
        return self.models.pager(pager_type, value, total, pages, start, limit)

    def find_by_url(self, entry_type, url):
        entry, abouts = None, [self.types.blog]
        if entry_type == self.types.entry:
            entry = self.entries.get(url)
            abouts.insert(0, self.types.entry)
        if entry_type == self.types.page:
            entry = self.pages.get(url)
        self.params.entry = entry
        self.params.entries = self._init_related_entries(url)
        self.params.error = self.models.error(url=url)
        self.params.primary.abouts = self._init_abouts_widget(abouts, url)
        return self.params

    def find_raw(self, raw_url):
        page_url = raw_url.replace(config.raw_url, '').replace(config.raw_suffix, config.url_suffix)
        page = self.find_by_url(self.types.page, page_url).entry
        if not page== None and page.raw_url == raw_url:
            return page.content
        entry_url = raw_url.replace(config.raw_url, config.entry_url).replace(config.raw_suffix, config.url_suffix)
        entry = self.find_by_url(self.types.entry, entry_url).entry
        if not entry == None and entry.raw_url == raw_url:
            return entry.content
        return None

    def archive(self, archive_type, url, start=1, limit=999999999, private=False):
        self.params.error = self.models.error(url=url)

        if archive_type == self.types.raw:
            url = url.replace(config.raw_url,config.archive_url)

        entries, count, = [], 0
        archive_url = url.replace(config.archive_url, '').strip('/')
        prefix =  url.replace(config.archive_url, config.entry_url)
        pattern = r'\d{4}/\d{2}/\d{2}|\d{4}/\d{2}|\d{4}'
        match = re.search(pattern, archive_url)
        if match and match.group() == archive_url or archive_url == '':
            _urls = self.urls if private==False else [ e for e in self.all_urls if e not in self.urls]
            urls = [url for url in _urls if url.startswith(prefix)]
            entries, _  =  self._find_by_page(urls, start, limit)
            count = len(entries)
        else:
            entries = None
        if archive_url == '':
            archive_url = self.types.all

        self.params.entries = entries
        self.params.archive = self.models.archive(archive_type, url, archive_url, url, count)
        self.params.primary.abouts = self._init_abouts_widget([self.types.archive])
        return self.params

    def search(self, search_type, url, value='', start=config.start, limit=config.limit):
        entries, total, abouts = None, 0, [self.types.blog]
        if  search_type == self.types.query:
            entries, total = self._find_by_query(value, start, limit)
        if search_type == self.types.tag:
            if self.by_tags.get(value) == None:
                entries = None
            else:
                entries, total = self._find_by_page(self.by_tags.get(value).urls, start, limit)
        if search_type == self.types.category:
            if self.by_categories.get(value) == None:
                entries = None
            else:
                entries, total = self._find_by_page(self.by_categories.get(value).urls, start, limit)
        if search_type == self.types.index:
            entries, total = self._find_by_page(self.urls, start, limit)
            abouts = []
        self.params.error = self.models.error(url=url)
        self.params.entries = entries
        self.params.search = self.models.search(search_type, value, total)
        self.params.pager = self._paginate(search_type, value, total, start, limit)
        self.params.primary.abouts = self._init_abouts_widget(abouts)
        self.params.start = start
        self.params.limit = limit
        return self.params

    def error(self, url):
        self.params.error = self.models.error(url=url)
        self.params.primary.abouts = self._init_abouts_widget([self.types.blog])
        return self.params


if __name__ == '__main__':
    import doctest
    doctest.testmod()
