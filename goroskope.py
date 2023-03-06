import requests
from bs4 import BeautifulSoup as b

URL = 'https://https://www.astrostar.ru/'
HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = b(html, 'html.parser')
    items = soup.find_all('div', class_='col-md-1 col-sm-2 col-xs-3')
    cards = []

    for item in items:
        link = 'https://www.astrostar.ru'
        cards.append(
            {
             'Sign': item.find().get_text(),
             'link': link+item.find('a').get('href')
            }
        )
    return cards


html = get_html(URL)
cards = get_content(html.text)
my_sign = ('телец')


def get_url_sign(sign):
    for sign in cards:
        if my_sign.lower() == sign['Sign'].lower():
            url = str(sign['link'])
            return url
        else:
            pass


url_sign = (get_url_sign(my_sign))
html_sign = get_html(url_sign)


def parser(html):
    soup = b(html.text, 'html.parser')
    tags_p = soup.find_all('p')
    tags_headers = soup.find_all('div', class_='horoscopes-single-title')
    descriptions = []
    names = []
    for tag_elem in tags_p:
        descriptions.append(tag_elem)
    for tag_elem in tags_headers:
        names.append(tag_elem.text.strip())
    goroscope = {
                names[0]: descriptions[0].text,
                names[1]: descriptions[1].text,
                names[2]: descriptions[2].text
                }

    return f'{names[0]}:\n{descriptions[0].text}\n'\
           f'\n{names[1]}:\n{descriptions[1].text}\n'\
           f'\n{names[2]}:\n{descriptions[2].text}'


def main():
    html = get_html(URL)
    cards = get_content(html.text)
    my_sign = ('овен')

    def get_url_sign(sign):
        for sign in cards:
            if my_sign.lower() == sign['Sign'].lower():
                url = str(sign['link'])
                return url
            else:
                pass

    url_sign = (get_url_sign(my_sign))
    html_sign = get_html(url_sign)
    print(parser(html_sign))


if __name__ == '__main__':
    main()


