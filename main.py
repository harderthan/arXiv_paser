from bs4 import BeautifulSoup
import requests
import urllib.request
from urllib.request import urlopen
import sys

class Paper:
    def __init__(self, arxivid):
        self.arxivid = arxivid
        url = "https://arxiv.org/abs/{}".format(arxivid)
        html = requests.get(url)
        if html.status_code != 200:
            return ValueError

        html = BeautifulSoup(html.text, 'html.parser')
        paper_title = str(list(html.find("h1", "title mathjax"))[1])[0:]
        paper_authors = [name.text for name in html.find("div", "authors").find_all("a")]
        paper_abstract = str(list(html.find("blockquote", "abstract mathjax"))[1])

        self.title = paper_title
        self.authors = paper_authors
        self.abstract = paper_abstract

    def download(self):
        # reporthook func for urlretrieve func
        def reporthook(blocknum, blocksize, totalsize):
            readsofar = blocknum * blocksize
            if totalsize > 0: # not yes finished
                percent = readsofar * 1e2 / totalsize
                s = "\r%5.1f%% %*d / %d \t%s" % (
                    percent, len(str(totalsize)), readsofar, totalsize, self.title)
                sys.stderr.write(s)
                if readsofar >= totalsize: # near the end
                    s = "\r%5.1f%% %*d / %d \t%s [done]" % (
                        percent, len(str(totalsize)), readsofar, totalsize, self.title)
                    sys.stderr.write(s)
            else: # total size is unknown
                sys.stderr.write("read %d\n" % (readsofar,))

        # download .pdf from arXiv
        url = "https://arxiv.org/pdf/{}.pdf".format(self.arxivid)
        output_name = "{}.pdf".format(self.title).replace(' ', '_').replace(':', '')
        urllib.request.urlretrieve(url, "{}".format(output_name), reporthook=reporthook)

# paper = Paper(1901.08585)
# paper.download()

url = 'http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=1'
with urlopen(url) as url:
    s = url.read()
print(s)
