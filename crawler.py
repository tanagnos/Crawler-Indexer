from urllib.request import urlopen

import urllib
from bs4 import BeautifulSoup

from Index import Index
from csv_handler import write_a_csv
from file_handler import create_proj_directory, create_files, file_to_set, set_to_file
from find_links import FindsLinks


class Crawler:
    project = ''
    base_url = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    # starts with project name and the homepage.Creates 'queue.txt' and 'crawled.txt'.Call 'startup()' and crawling()
    # methods.
    def __init__(self, project, base_url):
        Crawler.project = project
        Crawler.base_url = base_url
        Crawler.queue_file = Crawler.project + '/queue.txt'
        Crawler.crawled_file = Crawler.project + '/crawled.txt'
        self.start_up()
        self.crawling(self, Crawler.base_url)

    # Creates directory and files for project on first run and starts the crawler.Use the 'file_to_set()' method from
    # file_handler.py.
    @staticmethod
    def start_up():
        create_proj_directory(Crawler.project)
        create_files(Crawler.project, Crawler.base_url)
        Crawler.queue = file_to_set(Crawler.queue_file)
        Crawler.crawled = file_to_set(Crawler.crawled_file)

    # Call the add_links() and 'updates_files()' methods.
    @staticmethod
    def crawling(self, page_url):
        if page_url not in Crawler.crawled:
            Crawler.add_links(Crawler.collect_links(self, page_url))
            Crawler.queue.remove(page_url)  # crawled remove crawled page from queue
            Crawler.crawled.add(page_url)  # add it to crawled pages
            Crawler.update_files()

    # ask permission to read html from a website.Call save text for current page and return the rest links it found
    # with get links from find_links.
    @staticmethod
    def collect_links(self, page_url):
        html_string = ''
        try:  # try to open the URL.
            response = urlopen(page_url)  # open the URL.
            if 'text/html' in response.getheader('Content-Type'):  # if the Content type is text html read it and
                # decode it using utf-8.
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            link_finder = FindsLinks(Crawler.base_url, page_url)
            link_finder.feed(html_string)  # call the handle starttag from find_links class.
            self.save_text(page_url)
        except Exception as e:  # if you cant open the URL just print hte error.
            print(str(e))  # we print the error when we try to crawl the page in the output
            return set()
        return link_finder.get_links()

    # read all the text from a website using BeautifulSoup module and call write_a_csv() from csv_handler.py.
    @staticmethod
    def save_text(page_url):
        with urllib.request.urlopen(page_url) as url:
            s = url.read()
        soup = BeautifulSoup(s, "html.parser")
        for script in soup(["script", "style"]):  # kill all script and style elements
            script.extract()  # rip it out
        text = soup.get_text()  # get text
        lines = (line.strip() for line in text.splitlines())  # break into lines and remove leading and trailing space
        # on each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))  # break multi-headlines into a
        # line each
        text = '\n'.join(chunk for chunk in chunks if chunk)  # drop blank lines
        write_a_csv(Index(text, page_url))

    # Saves queue data to project files.if website is crawled or in queue continue to the next website.
    @staticmethod
    def add_links(links):
        for url in links:
            if (url in Crawler.queue) or (url in Crawler.crawled):
                continue
            Crawler.queue.add(url)

    # update files using set_to_file() method from file_handler.py.
    @staticmethod
    def update_files():
        set_to_file(Crawler.queue, Crawler.queue_file)
        set_to_file(Crawler.crawled, Crawler.crawled_file)
