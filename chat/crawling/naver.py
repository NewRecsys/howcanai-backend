import urllib.request
import urllib.parse
from .extractor import MainTextExtractor
from bs4 import BeautifulSoup
import json
import yaml

def naver_search(args, corpus_list, links):
    with open('chat/API.yaml', 'r') as yaml_conf:
        conf = yaml.safe_load(yaml_conf)
        API = conf['API']
        
    start = 1
    sort = 'sim'
    url = f"https://openapi.naver.com/v1/search/webkr?query={urllib.parse.quote(args.query)}&display={args.naver_display}&start={start}&sort={sort}"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",API['naver_client_id'])
    request.add_header("X-Naver-Client-Secret",API['naver_client_secret'])

    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if rescode == 200:
        response_body = response.read()
        result = json.loads(response_body.decode('utf-8'))
        items = result['items']

        for item in items:
            # HTML 태그 제거
            snippet = BeautifulSoup(item['description'], 'html.parser').get_text()                
            title = BeautifulSoup(item['title'], 'html.parser').get_text()
            
            if args.calculated_for == 'main_page':
                corpus_list.append(MainTextExtractor(item['link']).extract_main_content())
            elif args.calculated_for == 'snippet':
                corpus_list.append(snippet)
            elif args.calculated_for == 'title':
                corpus_list.append(title)
                
            links.append(item['link'])
    else:
        print("Error Code:", rescode)
    return corpus_list, links