import requests
import bs4

def get_url(url):
    r=requests.get(url)
    return r
def parse_task(html):
    bs=bs4.BeautifulSoup(html,'lxml')
    return bs
def main():
    req = get_url('https://quotes.toscrape.com/')
    soup = parse_task(req.text)
    authors = [tag.text for tag in soup.select('.author')]
    quotes = [tag.text for tag in soup.select('.text')]
    #item = [tag.text ]
    #print("Authors:", authors)
    #print("Quotes:", quotes)
    # for item in soup.select('.tag-item'):
    #     print("Tags:", item.text)
    valid_page = True
    authors = set()
    page=1
    while valid_page:
        url = f'https://quotes.toscrape.com/page/{page}/'
        req = get_url(url)
        if 'No quotes found!' in req.text:
            valid_page = False
        soup = parse_task(req.text)
        for tag in soup.select('.author'):
            authors.add(tag.text)
        page += 1
    print("Authors:", sorted(authors))
    print("total pages:", page-1)
if __name__ == '__main__':
    main()
