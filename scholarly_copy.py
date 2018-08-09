#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""scholarly.py"""

from __future__ import absolute_import, division, print_function, unicode_literals

from bs4 import BeautifulSoup
import hashlib
import pprint
import random
import re
import codecs
import requests
import time
from SpiderKit.agents import agents

_GOOGLEID = hashlib.md5(str(random.random()).encode('utf-8')).hexdigest()[:16]
_COOKIES = {'GSP': 'ID={0}:CF=4'.format(_GOOGLEID)}
_HEADERS = {
    'accept-language': 'en-US,en',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml'
    }
_HOST = 'https://scholar.google.com'
_AUTHSEARCH = '/citations?view_op=search_authors&hl=en&mauthors={0}'
_CITATIONAUTH = '/citations?user={0}&hl=en'
_CITATIONPUB = '/citations?view_op=view_citation&citation_for_view={0}'
_KEYWORDSEARCH = '/citations?view_op=search_authors&hl=en&mauthors=label:{0}'
_PUBSEARCH = '/scholar?q={0}'
_SCHOLARPUB = '/scholar?oi=bibs&hl=en&cites={0}'
_PROXIES = {"http": "127.0.0.1:1080", "https": "127.0.0.1:1080"}
_CITATIONAUTHRE = r'user=([\w-]*)'
_CITATIONPUBRE = r'citation_for_view=([\w-]*:[\w-]*)'
_SCHOLARCITERE = r'gs_ocit\(event,\'([\w-]*)\''
_SCHOLARPUBRE = r'cites=([\w-]*)'
_EMAILAUTHORRE = r'Verified email at '

_SESSION = requests.Session()
_PAGESIZE = 100


# 如果网络错误，则自动切换IP地址
def _get_page(pagerequest, proxy):
    """Return the data for a page on scholar.google.com"""
    _HEADERS['User-Agent'] = random.choice(agents)
    # Note that we include a sleep to avoid overloading the scholar server
    time.sleep(5 + random.uniform(0, 5))
    resp = _SESSION.get(pagerequest, headers=_HEADERS, cookies=_COOKIES, proxies={proxy['type']: proxy['type'] + "://" + proxy['ip'] + ':' + str(proxy['port'])})

    if resp.status_code == 200:
        return resp.text
    if resp.status_code == 503:
        # Inelegant way of dealing with the G captcha
        raise Exception('Error: {0} {1}'.format(resp.status_code, resp.reason))
    else:
        raise Exception('Error: {0} {1}'.format(resp.status_code, resp.reason))


def _get_soup(pagerequest, proxy):
    """Return the BeautifulSoup for a page on scholar.google.com"""
    html = _get_page(pagerequest, proxy)

    return BeautifulSoup(html, 'html.parser')


def _search_citation_soup(soup, proxy):
    """Generator that returns Author objects from the author search page"""
    while True:
        for row in soup.find_all('div', 'gsc_1usr'):
            yield Author(row)
        next_button = soup.find(class_='gs_btnPR gs_in_ib gs_btn_half gs_btn_lsb gs_btn_srt gsc_pgn_pnx')
        if next_button and 'disabled' not in next_button.attrs:
            url = next_button['onclick'][17:-1]
            url = codecs.getdecoder("unicode_escape")(url)[0]
            soup = _get_soup(_HOST+url, proxy)
        else:
            break


class Author(object):
    """Returns an object for a single author"""
    def __init__(self, __data):
        if isinstance(__data, str):
            self.id = __data
        else:
            self.id = re.findall(_CITATIONAUTHRE, __data('a')[0]['href'])[0]
            self.url_picture = __data('img')[0]['src']
            self.name = __data.find('h3', class_='gsc_oai_name').text
            affiliation = __data.find('div', class_='gsc_oai_aff')
            if affiliation:
                self.affiliation = affiliation.text
            else:
                self.affiliation = ''
            # email = __data.find('div', class_='gsc_oai_eml')
            # if email:
            #     self.email = re.sub(_EMAILAUTHORRE, r'@', email.text)
            # self.interests = [i.text.strip() for i in
            #                   __data.find_all('a', class_='gsc_oai_one_int')]
            citedby = __data.find('div', class_='gsc_oai_cby')
            if citedby and citedby.text != '':
                self.citedby = int(citedby.text[9:])
            else:
                self.citedby = 0
        self._filled = False

    def fill(self, proxy):
        """Populate the Author with information from their profile"""
        url_citations = _CITATIONAUTH.format(self.id)
        url = '{0}&pagesize={1}'.format(url_citations, _PAGESIZE)
        soup = _get_soup(_HOST+url, proxy)
        self.name = soup.find('div', id='gsc_prf_in').text
        self.affiliation = soup.find('div', class_='gsc_prf_il').text
        # self.interests = [i.text.strip() for i in soup.find_all('a', class_='gsc_prf_inta')]
        self.url_picture = soup.find('img')['src']

        # h-index, i10-index and h-index, i10-index in the last 5 years
        index = soup.find_all('td', class_='gsc_rsb_std')
        if index:
            self.hindex = int(index[2].text)
            self.hindex5y = int(index[3].text)
            self.i10index = int(index[4].text)
            self.i10index5y = int(index[5].text)
        else:
            self.hindex = self.hindex5y = self.i10index = self.i10index5y = 0

        # # number of citations per year
        # years = [int(y.text) for y in soup.find_all('span', class_='gsc_g_t')]
        # cites = [int(c.text) for c in soup.find_all('span', class_='gsc_g_al')]
        # self.cites_per_year = dict(zip(years, cites))
        # self._filled = True
        return self

    def __str__(self):
        return pprint.pformat(self.__dict__)


def search_author(name, proxy):
    """Search by author name and return a generator of Author objects"""
    url = _AUTHSEARCH.format(requests.utils.quote(name))
    soup = _get_soup(_HOST+url, proxy)
    return _search_citation_soup(soup, proxy)
