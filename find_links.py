from html.parser import HTMLParser
from urllib import parse


# use the HTMLParser module
class FindsLinks(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    # handle_starttag is a method in HTMLParser.
    # When we call HTMLParser feed() this function is called when it encounters an opening tag <a>.The tag <a>
    # defines a hyperlink.feed() is a method in HTMLParser
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':  # the href attribute specifies the links destination
                    url = parse.urljoin(self.base_url, value)  # Construct a full (“absolute”) URL by combining a
                    # “base URL” (base) with another URL (url).
                    self.links.add(url)

    def get_links(self):
        return self.links

    # when you see an error nothing happens and continue
    def error(self, message):
        pass
