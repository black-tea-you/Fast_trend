import re
from konlpy.tag import Okt
from collections import Counter

# Okt 형태소 분석기 초기화
okt = Okt()
# 한글과 공백만 남기는 정규식
pattern = re.compile(r'[^가-힣\s]')

# 기술 뉴스용 불용어 세트
stopwords = set([
    # 조사
    '은','는','이','가','을','를','에','의','도','으로','에서','와','과',
    # 일반 불용어
    '한','하다','했다','하기','한다','등','때','또','또한','중','관련','내용','기자','보도',
    # 시간/위치
    '오늘','내일','이번','지난','올해','내년','과거','현재','한국','서울','현장','지역','국내','해외',
    # 기술 뉴스 특화
    '기술','서비스','제품','출시','업데이트','제공','강화','확대','성장','적용','도입',
    '개선','진출','공개','지원','모델','기능','버전','솔루션','활용','검토','가능','계획','예정',
])

def extract_keywords(titles: list[str], top_k: int = 10) -> list[str]:
    """
    주어진 뉴스 제목 리스트에서 불용어 제거 후 Okt로 명사 추출하고,
    상위 top_k 개 키워드를 반환합니다.
    """
    all_nouns = []
    for title in titles:
        clean = pattern.sub('', title)
        nouns = okt.nouns(clean)
        filtered = [n for n in nouns if n not in stopwords and len(n) > 1]
        all_nouns.extend(filtered)

    # 빈도 기반 Top K 반환
    return [word for word, _ in Counter(all_nouns).most_common(top_k)]