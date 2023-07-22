from chat.args import parse_args
from chat.topk import get_top_k # , get_top_k_faiss

from chat.crawling.google import google_search
from chat.crawling.naver import naver_search
from chat.crawling.extractor import MainTextExtractor
from chat.model import kobart
import openai
import datetime

import yaml
import requests
import asyncio
from bs4 import BeautifulSoup

def run_chat(args, query):
    with open('chat/API.yaml', 'r') as yaml_conf:
        conf = yaml.safe_load(yaml_conf)
        API = conf['API']
    
    args.query = query
    
    if API['google_search_engine_id'] is None or API['google_api_key'] is None:
        raise Exception('Insert your own Google Search API into args.py.')
    if API['naver_client_id'] is None or API['naver_client_secret'] is None:
        raise Exception('Insert your own NAVER Search API into args.py.')
    if args.query is None:
        raise Exception('--query is required.')
    corpus_list = []
    links = []
    if args.use_google:
        corpus_list, links = google_search(args, corpus_list, links)
    if args.use_naver: # 현재 미사용 설정
        corpus_list, links = naver_search(args, corpus_list, links)
        
    if not corpus_list:
        raise Exception('You must use at least one search engine.')
    
    # if args.use_faiss:
    #     top_sentence, result_links = get_top_k_faiss(args.query, list(set(corpus_list)), links, args.top_k)
    # else:
    #     top_sentence, result_links = get_top_k(args.query, list(set(corpus_list)), links, args.top_k)

    # TODO: 중복 제거를 제거했음 -> 설정하려면 corpusr_list, liks 쌍으로 제거해야 할 듯
    top_sentence, result_links = get_top_k(args.query, corpus_list, links, args.top_k)
    
    
###############################################################################################
    # TODO: 3개의 서버 주소를 리스트에 넣습니다.
    # TODO: args에서 top-k를 3으로 설정합니다.
    urls = ["http://115.85.181.95:30013/get_prediction/"] * len(result_links)
    print(f"result_links: \n {result_links}")
    print(f"urls: \n {urls}")
    summaries = []
    async def req(link, url):
        main_content = MainTextExtractor(link).extract_main_content().replace('\n', ' ')
        # bs_res = requests.get(link)
        # soup = BeautifulSoup(bs_res.content, 'html.parser')
        # main_content = soup.get_text()
        
        # if not main_content:
        #     print("bs 발동")
        #     bs_res = requests.get(link)
        #     soup = BeautifulSoup(bs_res.content, 'html.parser')
        #     main_content = soup.get_text()
        # else:
        #     print('not bs')
        #     print(f"AAA {main_content} BBB")
            
        print(f"main_content: \n {main_content}")
        
        response = requests.post(url, params={'input': main_content[:1000] if len(main_content) > 1000 else main_content})
        print(f"response (전처리 전): \n {response.json()['output']}")
        response = response.json()['output'].split('### 요약:')[1].split('<|endoftext|>')[0]
        print(f"response (전처리 후): \n {response}")
        return response
    
    # async def req_main(result_links, urls):
    #     res1 = asyncio.create_task(req(result_links[0], urls[0]))
    #     res2 = asyncio.create_task(req(result_links[1], urls[1]))
    #     res3 = asyncio.create_task(req(result_links[2], urls[2]))
    #     result_of_res1 = await res1
    #     result_of_res2 = await res2
    #     result_of_res3 = await res3
    #     return result_of_res1, result_of_res2, result_of_res3
    async def req_main(result_links, urls):
        tasks = [asyncio.create_task(req(link, url)) for link, url in zip(result_links, urls)]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses

    summaries = asyncio.run(req_main(result_links, urls))

    # None인 응답 (오류가 발생한 경우)을 필터링하고, summaries 리스트에 추가합니다.
    summaries = [summary for summary in summaries if summary is not None]
    
    # response1, response2, response3 = asyncio.run(req_main(result_links, urls))
    
    # summaries.extend([response1, response2, response3])
    
    
    # urls = ["http://115.85.181.95:30013/get_prediction/"] * len(result_links)
    # for link, url in zip(result_links, urls):
    #     main_content = MainTextExtractor(link).extract_main_content()
    #     print(f"main_content: \n {main_content}")
    #     response = requests.post(url, params={'input': main_content})
    #     print(f"response (전처리 전): \n {response}")
    #     response = response.json()['output'].split('### 요약:')[1].split('<|endoftext|>')[0]
    #     print(f"response (전처리 후): \n {response}")
    #     summaries.append(response)
    try:
        print('TRY')
        print(summaries)
        summaries = ' '.join(summaries)
    except:
        print('EXCEPT')
        print(summaries)
    
    ###############################################################################################


        
    openai.api_key = API['openai_api_key']
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": f"Question에 대한 답변을 Contents에서 찾아서 해줘. 너의 배경지식을 사용하지 말고, Contents에 있는 내용으로만 답변해줘."},
                {"role": "user", "content": f"Question: {args.query} \\n Contents: {summaries}"},

            ]
        )
    answer = completion["choices"][0]["message"]["content"]
    
    
    # result_links_prompt = '\n'.join(result_links)
    # openai.api_key = API['openai_api_key']
    # completion = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #             {"role": "system", "content": f"Generate a comprehensive and informative answer (but no more than 80 words) for a given question solely based on the provided URLs. You must only use information from the provided search results. Use an unbiased and journalistic tone. Use this current date and time: { datetime.datetime.now() } . Combine search results together into a coherent answer. Do not repeat text. Cite search results using [${{number}}] notation. Only cite the most relevant results that answer the question accurately. If different results refer to different entities with the same name, write separate answers for each entity. Answer in Korean."},
    #             {"role": "user", "content": f"Question: {args.query} \\n URL: {result_links_prompt}"},

    #         ]
    #     )
    # answer = completion["choices"][0]["message"]["content"]
    
    ###############################################################################################
    
    # TODO: 질문 -> Intent 분류
    # TODO: 답변 -> KoBART로 요약
    # TODO: Intent + 요약본 -> GPT 넣어서 추가 쿼리 도출
    # TODO: 추가 쿼리 -> list에 담고 리턴
    
    
    
    # return에 추가 쿼리 추가할 것
    return answer, result_links
    