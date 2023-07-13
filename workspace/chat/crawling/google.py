import requests
from .extractor import MainTextExtractor


def google_search(args, corpus_list, links):
    
    # 페이지당 최대 10개씩 추출
    for page in range(1, args.google_n_pages+1): 
        
        # google search URL
        url = f"https://www.googleapis.com/customsearch/v1?key={args.google_api_key}&cx={args.google_search_engine_id}&q={args.query}&start={page}"
        response = requests.get(url).json()
        
        for item in response.get("items"):
            if args.calculated_for == 'main_page':
                corpus_list.append(MainTextExtractor(item['link']).extract_main_content())
            else:
                corpus_list.append(item[getattr(args, 'calculated_for')])
            links.append(item['link'])
    
    return corpus_list, links