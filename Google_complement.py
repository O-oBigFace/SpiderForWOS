import requests
from bs4 import BeautifulSoup
import re
import time
import warnings
warnings.filterwarnings('ignore')
headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-us;q=0.5,en;q=0.3',
    'connection': 'keep-alive',
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}

url = 'https://www.google.com/search'
# proxies = {"http": "127.0.0.1:1080", "https": "127.0.0.1:1080"}
proxy_host = "proxy.crawlera.com"
proxy_port = "8010"
proxy_auth = "0b3d10012b61488aa0667b27c829d5de:"
proxies = {"https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
           "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}


# 爬取网页返回soup对象
def make_soup_google(payloads):
    content = ''
    try:
        html = requests.get(
            url,
            params=payloads,
            headers=headers,
            proxies=proxies,
            verify=False
        )
        html.encoding = "utf-8"
        content = html.text
    except Exception as e:
        print(e)

    if content is not None and len(content) > 0:
        return BeautifulSoup(content, 'lxml')
    else:
        return None


def get_email_and_phone(key_words):
    payloads = {
        "q": key_words + ' and email and phone',
    }

    soup = make_soup_google(payloads)
    if soup is None:
        return '', ''

    #  获取摘要
    tag_results = soup.select("span[class='st']")
    results = {str(tr)
               .replace(r"<em>", '')
               .replace(r"</em>", '')
               .replace(r"<wbr>", '')
               .replace(r"</wbr>", '') for tr in tag_results}

    emailRegex = re.compile(r"""([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,4}))""", re.VERBOSE)
    emailFilterRegex = re.compile(r"""^[Ee]-?mail""")

    phoneRegex = re.compile(r"""([Pp]hone|[Mm]obile)[,:]?\s*(\+\s?[\d]+\s?)?(\([\d\-. ]+\)\s{0,2})*(\d+[/.-]?\s?)*""", re.VERBOSE)
    phoneFilterRegex = re.compile(r"""([Pp]hone|[Mm]obile)[,:]?\s*""")

    email = str()
    phone = str()
    # 每一条摘要
    for r in results:
        pho = phoneRegex.search(r)
        pho_no = phoneFilterRegex.sub('', pho.group()).strip() if pho is not None else ''
        phone = pho_no if len(pho_no) > len(phone) else phone

        ems = [emailFilterRegex.sub('', e).strip() for a in emailRegex.findall(r) for e in a]
        for e in ems:
            email = e if len(e) > len(email) else email
    return email, phone


def get_address(affiliation):
    payloads = {
        "q": 'where is ' + affiliation.split(';')[0] + 'located?',
    }

    soup = make_soup_google(payloads)
    if soup is None:
        return ''
    tag_results = soup.select("div[class='Z0LcW']")
    address = tag_results[0].getText() if len(tag_results) > 0 else ''
    return address


def get_country(affiliation):
    payloads = {
        "q": 'what country is ' + affiliation.split(';')[0] + ' in?',
    }

    soup = make_soup_google(payloads)
    if soup is None:
        return ''
    tag_results = soup.select("div[class='Z0LcW']")
    country = tag_results[0].getText() if len(tag_results) > 0 else ''
    return country if country is not None else ''


def get_language(country):
    payloads = {
        "q": 'what language do they speak in ' + country + '?',
    }

    soup = make_soup_google(payloads)
    if soup is None:
        return ''
    tag_results = soup.select("div[class='Z0LcW']")
    language = tag_results[0].getText() if len(tag_results) > 0 else ''
    return language


def get_position(key_words):
    payloads = {
        "q": key_words + ' professor or researcher or scientist',
    }

    soup = make_soup_google(payloads)
    if soup is None:
        return ''
    tag_results = soup.select("span[class='st']")
    results = {str(tr)
               .replace(r"<em>", '')
               .replace(r"</em>", '')
               .replace(r"<wbr>", '')
               .replace(r"</wbr>", '') for tr in tag_results}

    associateProfessorRegex = re.compile('''[Aa]ssociate\s+[Pp]rofessor''')
    assistantProfessorRegex = re.compile('''[Aa]ssistant\s+[Pp]rofessor''')
    professorRegex = re.compile('''[Pp]rofessor''')
    researcherRegex = re.compile('''[Rr]esearcher''')
    scientistRegex = re.compile('''[Ss]cientist''')

    # position需要设置优先级
    for r in results:
        if associateProfessorRegex.search(r):
            return 'Associate Professor'

        if assistantProfessorRegex.search(r):
            return 'Assistant Professor'

        if professorRegex.search(r):
            return "Professor"

        if researcherRegex.search(r):
            return 'Researcher'

        if scientistRegex.search(r):
            return 'Scientist'

    return ' '


if __name__ == "__main__":
    print(get_country('stanford university'))