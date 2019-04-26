import requests
from bs4 import BeautifulSoup
import time
import csv


def update_date(d):
    d_split = d.split(' ')
    if ':' in d_split[0]:
        return '26 апреля'
    elif d_split[0] == 'вчера':
        return '25 апреля'
    else:
        return d_split[0] + ' ' + d_split[1]


def clean_and_update_data(path):
     with open(path, 'r', encoding='utf-8') as f:
          reader = csv.reader(f)
          data = [row for row in reader]
          new_data = []
          for row in data:
              if row not in new_data:
                  row[2] = row[2].replace(' в', '')
                  new_data.append(row)
          return new_data, data


news = []
for i in range(0, 83):
    r = requests.get('https://news.yandex.ru/yandsearch?text=%D0%B0%D0%B2%D1%82%D0%BE%D0%BD%D0%BE%D0%BC%D0%BD%D1%8B%D0%B9%20%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D0%BD%D0%B5%D1%82&rpt=nnews2&rel=tm&p='+str(i))
    soup = BeautifulSoup(r.text)
    docs = soup.select('.document.i-bem')

    for doc in docs:
        provider = doc.select('.document__provider-name')[0].text
        doc_time = doc.select('.document__time')[0].text.replace('\xa0', ' ')
        title = doc.select('.document__title a')[0].text
        link = doc.select('.document__title a')[0]['href']
        desc = doc.select('.document__snippet')[0].text
        time_date = update_date(doc_time)
        print(title)
        news.append([provider, doc_time, time_date, title, link, desc])

        time.sleep(10)


with open('yandex.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['provider', 'doc_time', 'time_date', 'title', 'link', 'desc'])
    for row in news:
        writer.writerow(row)
