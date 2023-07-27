import openai
from chat.model import kobart, intent_inference


def run_add_query(answer, query, summaries_merge):
    answer_summary = kobart(answer)
    
    intent = intent_inference(query=query, model='klue/roberta-base', ckpt_path='/opt/ml/howcanai-backend/chat/ckpt/intent_v1.ckpt')
    
    completion2 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"""
                사람의 검색 의도가 {intent} 이고, 사용자의 검색어가 {query} 이고, 그에 대한 답변에 대한 요약이 {answer_summary} 일 때, 추가로 검색할만한 쿼리를 번호를 붙여서 2가지 추천해줘.
                [예시]
                검색 의도: 거래 의도 (Transactional Intent) - 음식 주문 및 배달 (Food Ordering and Delivery)
                검색어: 베이커리 메뉴 추천해줘.
                답변 요약: 크로와상, 부드럽고 바삭한 프랑스식 반죽의 대표적인 베이커리로, 버터 향과 겉바속촉이 매력적입니다. 
                일 때,
                1. 크로와상 맛집 추천해줘. 
                2. 크로와상과 잘 어울리는 다른 메뉴 추천해줘.
                """,
            },
            {
                "role": "user",
                "content": f"Question: {query} \\n Contents: {summaries_merge}",
            },
        ],
    )
    
    
    add_query = completion2["choices"][0]["message"]["content"]
    
    print(add_query)
    
    try:
        add_query = add_query.split('\n')
        nexts = []
        
        for i in add_query :
    
            if '.' in i :
                nexts.append(i.split('.')[1])
    except:
        nexts = ['na1', 'na2']
    
    return nexts
    