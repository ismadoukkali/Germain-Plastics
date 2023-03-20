from bs4 import BeautifulSoup
import urllib.request as urllib2

class Page:

    def __init__(self, page_url):
        self.page_url = page_url
        self.page = urllib2.urlopen(self.page_url)
        self.soup = BeautifulSoup(self.page, 'html.parser')
    
    def get_HTML(self):
        return self.soup

def get_text(html):

    columns_main = html.find('div', {'class':'entry-content clear'})
    print(columns_main.text)



if __name__ == "__main__":
    urls = ['https://geosyn.com.au/geonets/', 'https://geosyn.com.au/geosynthetic-clay-liner-gcl/', 'https://geosyn.com.au/geogrid/', 'https://geosyn.com.au/hdpe-liners-geomembranes/', 'https://geosyn.com.au/hdpe-liner-lite-pond-applications/', 'https://geosyn.com.au/geotextile-underlay-drainage-fabric/', 'https://geosyn.com.au/hdpe-geocells-cellular-confinement-systems-css/']
    text = {}

    for url in urls:
        page = Page(url)
        html = Page.get_HTML(page)
        get_text(html)
