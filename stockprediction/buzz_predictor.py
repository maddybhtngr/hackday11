from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import sentiment_analyzer





def get_prediction(stock: str):
    req = Request('https://www.google.com/search?q='+stock, headers={'User-Agent': 'Mozilla/5.0'})
    web_url = urlopen(req)
    data = web_url.read()

    data_links = []
    sentiments = []

    def find_all_urls(website):
        max_data_links = 20
        while max_data_links > 0:
            sentiments.append(sentiment_analyzer.document_sentiment(str(website)))
            soup = BeautifulSoup(website, 'html.parser')

            for link in soup.find_all('a'):
                href_link = link.get('href')
                if '/search?' in href_link:
                    data_links.append('https://www.google.com' + href_link)

            nested_request = Request(data_links[0], headers={'User-Agent': 'Mozilla/5.0'})
            nested_url = urlopen(nested_request)
            website = nested_url.read()
            del data_links[0]
            max_data_links = max_data_links - 1

    find_all_urls(data)

    average_sentiment = sum(sentiments)/len(sentiments)
    return average_sentiment * 0.4
