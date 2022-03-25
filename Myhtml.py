from requests import get
from aiofiles import open as aopen
from lxml import etree
from pyquery import PyQuery as pq
from os import walk,listdir,rmdir


class html:
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.46'
    }

    def __init__(self, domain=None):
        self.domain = domain
        self.html_text = None

    def get_page(self):
        dt = html.get_text(self, self.domain)
        doc = etree.HTML(dt)
        page = doc.xpath('/html/body/div/div[3]/div/div[2]/div/div/main/div[2]/ul/li[6]/a/text()')[0]
        return page

    def add_page_arg(self):
        page = html.get_page(self)
        urls_with_page = (self.domain + f'/page/{i}' for i in range(1, int(page) + 1))
        return urls_with_page

    def get_text(self, url):
        resp = get(url=url, headers=html.headers)
        if resp.status_code == 200:
            self.html_text = resp.text
            return resp.text
        return None

    @staticmethod
    def remove_folders():
        for dirpath, dirnames, filenames in walk('D://绝对领域',topdown=False):
            if not listdir(dirpath):
                rmdir(dirpath)

    @staticmethod
    def parse_domain(text):
        doc = pq(text)
        tag_as = doc('h2.entry-title a').items()
        for a in tag_as:
            href = a.attr('href')
            title = a.attr('title')
            # ('愿望是能让自己每天开心', 'https://juedly.com/1891.html')
            yield title, href

    def episode_parse(self, url):
        text = html.get_text(self, url=url)
        doc = pq(text)
        article = doc('div.entry-wrapper article')
        imgs = article.find('img').items()
        return imgs

    @staticmethod
    async def one_download(session,url, title):
        name = url.split('/')[-1]
        async with session.get(url=url, headers=html.headers) as resp:
            async with aopen(f'D://绝对领域//{title}//{name}', mode='wb') as file:
                await file.write(await resp.content.read())
                print(f'{title}_{name}', '已就绪！')
