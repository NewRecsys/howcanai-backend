# import faiss
import numpy as np
from sentence_transformers import SentenceTransformer, util

# def get_top_k_faiss(query: str,
#               corpus: list,
#               links: list,
#               top_k: int,
#               threshold: bool = False,
#               cosine = True,
#               ):

#     """
#     query와 비교하여 유사도가 가장 큰 corpus를 top_k 개 return 

#     Args:
#         query (str): 유저의 쿼리 또는 유저의 쿼리를 처리한 구글에 검색할 검색어
#         corpus (list): 구글 API로 받은 본문 데이터 또는 description 
#         top_k (int): 유사도 상위 k개 선택
#         threshold (bool): threshold를 설정하여 cos_scores가 threshold 이상인 경우에만 return
#     """
#     top_sentences = []
#     result_links = []
#     # 임베딩 모델: ko-sroberta-multitask
#     embedder = SentenceTransformer("jhgan/ko-sroberta-multitask")
#     query_embedding = embedder.encode(query, convert_to_tensor=False)
#     corpus_embeddings = embedder.encode(corpus, convert_to_tensor=False)

#     if cosine: # L2 정규화를 사용하여 벡터를 전처리합니다.
#         faiss.normalize_L2(query_embedding.reshape(1, -1))
#         faiss.normalize_L2(corpus_embeddings)
#     # FAISS index 생성 및 추가
#     d = len(query_embedding)
#     index = faiss.IndexFlatIP(d)
#     corpus_embeddings_matrix = np.vstack(corpus_embeddings)
#     index.add(corpus_embeddings_matrix)
    
#     #유사도 계산.
#     top_k_search_results = index.search(np.array([query_embedding]), top_k)
    
#     # top k 추출 (cos_scores 가장 높은 인덱스 저장)
#     top_results = top_k_search_results

#     # 출력
#     print(f"Query: \n{query}\n")
#     print(f"Top {top_k} most similar sentences in corpus:")
#     for i, idx in enumerate(top_results[1][0]):
#         score = top_k_search_results[0][0][i]
#         if score < threshold:
#             break
#         top_sentences.append(corpus[idx].strip())
#         result_links.append(links[idx])
#         print("[Score: %.4f]" % (score), corpus[idx].strip())

#     # return
#     # TODO: URL, index 등 우리 task 에 맞게 수정하기 (지금은 단순히 top_k 의 str을 그대로 return)
#     return top_sentences, result_links


def get_top_k(query: str,
              corpus: list,
              links: list,
              top_k: int,
              threshold: bool = False):

    """
    query와 비교하여 유사도가 가장 큰 corpus를 top_k 개 return 

    Args:
        query (str): 유저의 쿼리 또는 유저의 쿼리를 처리한 구글에 검색할 검색어
        corpus (list): 구글 API로 받은 본문 데이터 또는 description 
        top_k (int): 유사도 상위 k개 선택
        threshold (bool): threshold를 설정하여 cos_scores가 threshold 이상인 경우에만 return
    """
    top_sentences = []
    result_links = []
    
    # 임베딩 모델: ko-sroberta-multitask
    embedder = SentenceTransformer("jhgan/ko-sroberta-multitask")
    query_embedding = embedder.encode(query, convert_to_tensor=True)
    corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

    # 유사도 계산
    cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
    cos_scores = cos_scores.cpu()

    # top k 추출 (cos_scores 가장 높은 인덱스 저장)
    top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]

    # print
    print(f"Query: \n{query}\n")
    print(f"Top {top_k} most similar sentences in corpus:")
    for idx in top_results[0:top_k]:
        if cos_scores[idx] < threshold:
            break
        top_sentences.append(corpus[idx].strip())
        result_links.append(links[idx])
        print("[Score: %.4f]" % (cos_scores[idx]), corpus[idx].strip())

    # return
    # TODO: URL, index 등 우리 task 에 맞게 수정하기 (지금은 단순히 top_k 의 str을 그대로 return)
    return top_sentences, result_links