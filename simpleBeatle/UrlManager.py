# coding:utf-8
# python 爬虫 初级阶段
__author__ = '小蚂蚁cc'

import re
import codecs
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


class UrlManager:
    def __int__(self):
        self.new_urls = set()  # 未爬取的url集合
        self.old_urls = set()  # 已爬取的url集合

    def has_new_url(self):
        return self.new_url_size != 0

    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def new_url_size(self):
        return len(self.new_urls)

    def old_url_size(self):
        return len(self.old_urls)


class HtmlDownloader:
    def download(self, url):
        if url is None:
            return None
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        return None


class HtmlParser:
    def parser(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all('a', href=re.compile(r'/vies/\d+\.htm'))
        for link in links:
            new_url = link('href')
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        data = {}
        data['url'] = page_url
        title = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
        data['title'] = title.get_text()
        summary =soup.find('div', class_='lemma-summary')
        data['summary'] = summary.get_text()
        return data


class DataOutput:
    def __init__(self):
        self.datas = []

    def store_data_(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        fout = codecs.open('baike.html', 'w', encoding='utf-8')
        fout.write('<html>')
        fout.write('<body>')
        fout.write('<table>')
        for data in self.datas:
            fout.write('<tr>')
            fout.write('<td>%s</td>' %data['url'])
            fout.write('<td>%s</td>' %data['title'])
            fout.write('<td>%s</td>' %data['summary'])
            fout.write('</tr>')
            self.datas.remove(data)
        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')
        fout.close()


class SpiderMan:
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self, root_url):
        self.manager.add_new_url(root_url)
        while(self.manager.has_new_url() and self.manager.old_url_size()<100):
            try:
                new_url = self.manager.get_new_url()
                html = self.downloader.download(new_url)
                new_urls, data = self.parser.parser(new_url, html)
                self.manager.add_new_url(new_urls)
                self.output.store_data(data)
                print('已经抓取%s个链接' %self.manager.old_url_size())
            except Exception as e:
                print('crawl failed')
        self.output.output_html()


if __name__ == "__main__":
    spider_man = SpiderMan()
    spider_man.crawl('http://baike.baidu.com/view/284853.html')








