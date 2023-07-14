from .args import parse_args
from .topk import get_top_k # , get_top_k_faiss

from .crawling.google import google_search
from .crawling.naver import naver_search

import openai
import datetime

args = parse_args()

def run_chat(args):
    if args.google_search_engine_id is None or args.google_api_key is None:
        raise Exception('Insert your own Google Search API into args.py.')
    if args.naver_client_id is None or args.naver_client_secret is None:
        raise Exception('Insert your own NAVER Search API into args.py.')
    if args.query is None:
        raise Exception('--query is required.')

    corpus_list = []
    links = []
    if args.use_google:
        corpus_list, links = google_search(args, corpus_list, links)
    if args.use_naver:
        corpus_list, links = naver_search(args, corpus_list, links)
        
    if not corpus_list:
        raise Exception('You must use at least one search engine.')
    
    if args.use_faiss:
        top_sentence, result_links = get_top_k_faiss(args.query, list(set(corpus_list)), links, args.top_k)
    else:
        top_sentence, result_links = get_top_k(args.query, list(set(corpus_list)), links, args.top_k)

    result_links = '\n'.join(result_links)
    openai.api_key = args.openai_api_key
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": f"Generate a comprehensive and informative answer (but no more than 80 words) for a given question solely based on the provided URLs. You must only use information from the provided search results. Use an unbiased and journalistic tone. Use this current date and time: { datetime.datetime.now() } . Combine search results together into a coherent answer. Do not repeat text. Cite search results using [${{number}}] notation. Only cite the most relevant results that answer the question accurately. If different results refer to different entities with the same name, write separate answers for each entity. Answer in Korean."},
                {"role": "user", "content": f"Question: {args.query} \\n URL: {result_links}"},

            ]
        )
    answer = completion["choices"][0]["message"]["content"]
    print(answer)
    
    return answer

    
    
if __name__ == "__main__":
    run_chat(args)
    
    