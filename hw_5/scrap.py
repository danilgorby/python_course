import re
from urllib.request import urlopen
from typing import List, Tuple, Optional  # для аннотаци
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def _get_href(self, attrs: List[Tuple[str, str]]) -> Optional[str]:
        # использование метода не предполагается вне класса
        for attr in attrs:
            if attr[0] == 'href':
                return attr[1]
        return None

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        # print('attrs:', attrs)
        if tag == 'a':
            link = self._get_href(attrs)
            if link and re.match(r'/\d\d\d\d.*', link):
                self.links.append(link)

    # def handle_endtag(self, tag):
    #     print("Encountered an end tag :", tag)
    #
    # def handle_data(self, data):
    #     print("Encountered some data  :", data)


class MagazineLinkHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.magazine_link = None
        self.tag = None
        self.attrs = None

    def _get_href(self, attrs: List[Tuple[str, str]]) -> Optional[str]:
        # использование метода не предполагается вне класса
        for attr in attrs:
            if attr[0] == 'href':
                return attr[1]
        return None

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        # print('attrs:', attrs)
        self.tag = tag
        self.attrs = attrs

    # def handle_endtag(self, tag):
    #     print("Encountered an end tag :", tag)
    #
    def handle_data(self, data):
        # print("Encountered some data  :", data)
        if data == 'Загрузить весь журнал':
            # print('d', self.tag)
            # print('f', self.attrs)
            link = self._get_href(self.attrs)
            if link is not None:
                self.magazine_link = link



def download_html(link: str) -> str:
    response = urlopen(link)
    html = response.read()
    decoded_data = html.decode('Windows-1251')
    return decoded_data

parser = MyHTMLParser()
# parser.feed('<html><head><title>Test</title></head>'
#             '<body><a href=link><h1 attr_name=b></a>Parse me!</h1></body></html>')

URL = 'http://artculturestudies.sias.ru'

response = urlopen(URL)
html = response.read()
# print(response.getheaders())
headers = response.headers
# print(html.decode('Windows-1251'))

parser.feed(html.decode('Windows-1251'))
# print(*parser.links, sep='\n')

pdf_page_links = []
for link in parser.links:
    pdf_page_links.append(URL + link)



# print(download_html(pdf_page_links[0]))
# print(pdf_page_links[0])

pdf_page_html = download_html(pdf_page_links[1])
pdf_parser = MagazineLinkHTMLParser()
pdf_parser.feed(pdf_page_html)

# print(URL + pdf_parser.magazine_link)
response = urlopen(URL + pdf_parser.magazine_link)
pdf = response.read()
with open('pdf1.pdf', 'wb') as f:
    f.write(pdf)

