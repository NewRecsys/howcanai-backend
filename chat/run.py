from chat.args import parse_args
from chat.topk import get_top_k  # , get_top_k_faiss

from chat.crawling.google import google_search
from chat.crawling.naver import naver_search
from chat.crawling.extractor import MainTextExtractor
from chat.model import kobart
import openai
import datetime

import yaml
import requests
import asyncio
import aiohttp

from readability import Document
from bs4 import BeautifulSoup

from kiwipiepy import Kiwi


def run_chat(args, query):
    with open("chat/API.yaml", "r") as yaml_conf:
        conf = yaml.safe_load(yaml_conf)
        API = conf["API"]

    ## query 형태소 분석 (07/24)
    # args.query = query
    kiwi = Kiwi()
    tokens = kiwi.tokenize(query)
    args.query = " ".join(
        [token.form for token in tokens if token.tag in ["NNG", "NNP", "NR", "NP"]]
    )

    print(f"전처리 전 쿼리: {query}, 전처리 후 쿼리: {args.query}")

    if API["google_search_engine_id"] is None or API["google_api_key"] is None:
        raise Exception("Insert your own Google Search API into args.py.")
    if API["naver_client_id"] is None or API["naver_client_secret"] is None:
        raise Exception("Insert your own NAVER Search API into args.py.")
    if args.query is None:
        raise Exception("--query is required.")
    corpus_list = []
    links = []
    if args.use_google:
        corpus_list, links = google_search(args, corpus_list, links)
    if args.use_naver:  # 현재 미사용 설정
        corpus_list, links = naver_search(args, corpus_list, links)

    if not corpus_list:
        raise Exception("You must use at least one search engine.")

    ### 구글 상위 가져오기 (07/24)
    corpus_list, result_links = corpus_list[: args.top_k], links[: args.top_k]

    # if args.use_faiss:
    #     top_sentence, result_links = get_top_k_faiss(args.query, list(set(corpus_list)), links, args.top_k)
    # else:
    #     top_sentence, result_links = get_top_k(args.query, list(set(corpus_list)), links, args.top_k)

    ### top-k 제거 (07/24)
    # top_sentence, result_links = get_top_k(args.query, corpus_list, links, args.top_k)

    ###############################################################################################
    # TODO: 3개의 서버 주소를 리스트에 넣습니다.
    # urls = ["http://115.85.181.95:30013/get_prediction/", "http://49.50.172.150:40001/get_prediction/"]
    urls = ["http://115.85.181.95:30013/get_prediction/", "http://49.50.172.150:40001/get_prediction/"]
    print(f"result_links: \n {result_links}")
    summaries = []

    async def req(link, url):
        # main_content = MainTextExtractor(link).extract_main_content().replace('\n', ' ')

        doc = Document(requests.get(link).content)
        main_content = BeautifulSoup(doc.summary(), "lxml").text

        # main_content="펩시는 오랜 역사와 글로벌한 인지도를 가지고 있습니다. 많은 연도 동안 소비자들에게 익숙한 브랜드로 자리 잡아왔으며, 전 세계적으로 사랑받고 있는 음료수입니다. 뛰어난 맛과 상쾌한 탄산감은 많은 사람들에게 인기를 끌고 있습니다. 펩시는 시원하고 부드러운 맛으로 언제나 상쾌한 느낌을 선사해줍니다. 다양한 제품 라인업을 보유하고 있어서 소비자들의 다양한 취향과 욕구를 만족시켜줍니다. 레귤러, 다이어트, 제로 칼로리 등 다양한 옵션을 선택할 수 있습니다. 편리한 구매접근성을 제공합니다. 펩시는 거의 모든 슈퍼마켓, 편의점, 음식점 등에서 쉽게 구매할 수 있으며, 어디서나 접근성이 좋은 제품으로 알려져 있습니다."
        # bs_res = requests.get(link)
        # soup = BeautifulSoup(bs_res.content, 'html.parser')
        # main_content = soup.get_text()

        print(f"main_content: \n {main_content}")
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url,
                params={
                    "input": main_content[:1000]
                    if len(main_content) > 1000
                    else main_content
                },
            )
            data = await response.json()
            print('############### COMPLETE ###############')
            return data["output"].split("### 요약:")[1].split("<|endoftext|>")[0]

        # response = requests.post(url, params={'input': main_content[:1000] if len(main_content) > 1000 else main_content})
        # print(f"response (전처리 전): \n {response.json()['output']}")
        # response = response.json()['output'].split('### 요약:')[1].split('<|endoftext|>')[0]
        # print(f"response (전처리 후): \n {response}")
        # return response

    async def req_main(result_links, urls):
        tasks = [
            # 비동기로 실행할 작업을 생성하고, 해당 작업들을 테스크 리스트에 추가
            # req(link, url) 함수를 비동기적으로 실행하여 서버에 요청을 보내고 응답을 기다림
            asyncio.create_task(req(link, url))
            for link, url in zip(result_links, urls)
        ]
        # 생성한 task들을 asyncio.gather 함수로 실행하여 모든 작업들이 완료될 때까지 기다림
        # return_exceptions=True: 오류가 발생한 경우엗 결과를 기다리도록 함
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses

    summaries = asyncio.run(req_main(result_links, urls))

    # None인 응답 (오류가 발생한 경우)을 필터링하고, summaries 리스트에 추가합니다.
    summaries = [summary for summary in summaries if summary is not None]

    summaries_merge = ""
    try:
        print("TRY")
        for idx, summary in enumerate(summaries):
            summaries_merge += f"[{idx+1}] {summary} "
        print(summaries_merge)
        # summaries = ' '.join(summaries)
    except:
        print("EXCEPT")
        print(summaries)

    ###############################################################################################

    openai.api_key = API["openai_api_key"]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"Generate a comprehensive and informative answer (but no more than 80 words) for a given question solely based on the provided Contents. You must only use information from the provided search results. Use an unbiased and journalistic tone. Use this current date and time: { datetime.datetime.now() } . Combine search results together into a coherent answer. Do not repeat text. Cite search results using [${{number}}] notation. Only cite the most relevant results that answer the question accurately. If different results refer to different entities with the same name, write separate answers for each entity. Answer in Korean.",
            },
            {
                "role": "user",
                "content": f"Question: {query} \\n Contents: {summaries_merge}",
            },
        ],
    )
    answer = completion["choices"][0]["message"]["content"]

    # TODO: 질문 -> Intent 분류
    # TODO: 답변 -> KoBART로 요약
    # TODO: Intent + 요약본 -> GPT 넣어서 추가 쿼리 도출
    # TODO: 추가 쿼리 -> list에 담고 리턴

    # return에 추가 쿼리 추가할 것
    return answer, result_links
