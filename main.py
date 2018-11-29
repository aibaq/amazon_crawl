import validators
import requests

from bs4 import BeautifulSoup


class Crawler():
    words = ['virtue', 'signalling', 'is', 'society\'s', 'version', 'proof', 'of', 'stake']
    found_words = set()
    domain = 'amazon.com'
    url = 'https://amazon.com'
    urls = ['https://amazon.com']
    visited = set()
    session = requests.Session()
    attempt = 0

    def run(self):
        while not self.finished() and len(self.urls) > 0:
            url = self.urls.pop(0)
            self.parse(url)
            self.print()

    def parse(self, url):
        self.attempt += 1
        self.visited.add(url)
        self.session.headers = {'User-Agent': 'Mozilla/5.0'}
        html = self.session.get(url).text
        self.search(html)
        self.parse_urls(html)

    def parse_urls(self, html):
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all(['a', 'link'])
        for element in links:
            link = element.get('href')
            if not link:
                continue
            if link.startswith('/'):
                link = self.url + link
            if link not in self.visited:
                try:
                    if validators.url(link) is True and self.domain in link:
                        self.urls.append(link)
                except:
                    # Invalid link
                    pass

    def search(self, text):
        text = text.lower()
        for word in self.words:
            if not word in self.found_words:
                if word in text:
                    self.found_words.add(word)
                    print('Found a new words:', word)

    def finished(self):
        if len(self.found_words) != len(self.words):
            return False
        print('All words were found')
        return True

    def print(self):
        print('ATTEMPT:', self.attempt,
              'URLS:', len(self.urls),
              'VISITED:', len(self.visited),
              'FOUND:', self.found_words)


if __name__ == '__main__':
    c = Crawler()
    c.run()
