import requests
from lxml import html
from glob import glob
import csv
from collections import Counter
import time
import os
from dotenv import load_dotenv


from mecab_wrapper import mecab_parse

load_dotenv()

HEADERS = {'User-Agent': os.environ.get('USER_AGENT')}
CSV_DIR = os.environ.get('CSV_DIR', '.')
URL_COLNUM = int(os.environ.get('URL_COLNUM'))
TITLE_COLNUM = int(os.environ.get('TITLE_COLNUM'))

def extract_body(url):
    page = requests.get(url, headers=HEADERS)
    time.sleep(4)
    if page.status_code == 200:
        tree = html.fromstring(page.content)
        return ''.join(tree.xpath('//*[@id="novel_honbun"]/p/text()'))
    else:
        print('error, response status is not 200')
        return ''

def title_word_counter(title, body):
    fuzokugo_filter = lambda x: (
        x['pos'] == '名詞' and x['pos1'] != '接尾' or
        x['pos'] == '動詞' and x['base'] != 'する' and x['base'] != 'れる' and x['pos'] != '*' or
        x['pos'] == '形容詞'
        )
    subtitle_items = filter(fuzokugo_filter, mecab_parse(title))
    subtitle_items = list(map(lambda x: x['base'] if x['base'] != '*' else x['surface'], subtitle_items))
    result = Counter()

    if body == '':
        return Counter()
    else:
        body_items = filter(fuzokugo_filter, mecab_parse(body))
        body_items = list(map(lambda x: x['base'], body_items))
        body_counter = Counter(body_items)
        for word in subtitle_items:
            result[word] += (body_counter[word] > 0)
        return round(sum(result.values()) / len(set(subtitle_items)), 3)

if __name__ == '__main__':
    result = []
    for csv_file in glob(CSV_DIR + '/*.csv'):
        print('read: ', csv_file)
        with open(csv_file, 'r') as rf:
            csv_reader = csv.reader(rf)
            
            for idx, row in enumerate(csv_reader):
                print('process', row)
                url = row[URL_COLNUM]
                body = extract_body(url)
                score = title_word_counter(row[TITLE_COLNUM], body)
                result.append([score, row[TITLE_COLNUM], url])

    result.sort(reverse=True)
    with open('output.csv', 'a') as wf:
        csv_writer = csv.writer(wf)
        csv_writer.writerows(result)