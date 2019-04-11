import codecs
from bs4 import BeautifulSoup as bs
import requests


def __main__():
    base = ['http://ux.getuploader.com/e2339999zp/', 'http://ux.getuploader.com/e2337650/', 'http://ux.getuploader.com/toukyuutoyoko9000/', 'http://ux.getuploader.com/e2351000/']
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
    all_links = []

    for b in base:
        print('===== SCRAPING BASE PAGE =====', b)
        for idx in range(1, 50):
            url = b + 'index/' + 'date/desc/' + str(idx)
            print('=== Sub Scrape ===', url)
            base_done = False
            try:
                r = requests.get(url, headers=headers)
                html = r.content
                soup = bs(html,'html.parser')
                rows = soup.find_all('table', class_='table table-small-font table-hover')[0].find_all('tr')[1:]
                
                if rows:
                    for row in rows:
                        link = row.a.get('href')

                        td_list = list(map(lambda x: x.contents[0], row.find_all('td')))

                        title = row.a.get('title').split('.zip')[0]
                        comment = td_list[1]
                        downloads = td_list[-2]
                        size_mb = td_list[3].split(' ')
                        size_mb[0] = float(size_mb[0])
                        if (size_mb[1] == 'KB'):
                            size_mb[0] /= 1000.0
                        size_mb = size_mb[0]
                        all_links.append('|'.join(map(str, [title, comment, downloads, size_mb, link])))
                        print(all_links[-1])
                else:
                    base_done = True
            except Exception as e:
                print(e)
                base_done = True
            if base_done:
                break

    with codecs.open('links.csv', 'w' ,'utf-8') as f:
        for l in all_links:
            f.write(l + '\n')

if __name__ == '__main__':
    __main__()
