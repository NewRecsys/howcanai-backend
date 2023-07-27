import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='howcan.ai arguments')

    parser.add_argument('--query', type=str, default=None)
    
    parser.add_argument('--use_google', type=int, default=1, help = 'True(1) or False(0)')
    parser.add_argument('--google_n_pages', type=int, default=1, help='Search for up to 10 items on a page.')
    parser.add_argument('--use_naver', type=int, default=0, help = 'True(1) or False(0)')
    parser.add_argument('--naver_display', type=int, default=20)
        
    parser.add_argument('--calculated_for', type=str, default='snippet', choices=['snippet', 'title', 'main_page'], help='유사도 비교되는 대상')
    parser.add_argument('--use_faiss', type=int, default=0, help = 'True(1) or False(0)')
    parser.add_argument('--top_k', type=int, default=3)
        
    args = parser.parse_args()

    return args