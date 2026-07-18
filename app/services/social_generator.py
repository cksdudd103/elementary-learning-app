import random


def _curriculum_topics(subject, grade, fallback):
    try:
        from ..models import CurriculumUnit
        units = CurriculumUnit.query.filter_by(subject=subject, grade_level=grade).order_by(CurriculumUnit.unit_order).all()
        if units:
            return [u.unit_name for u in units]
    except Exception:
        pass
    return fallback


def _topic_for(grade, fallback):
    return random.choice(_curriculum_topics("social", grade, fallback))


def _make(prompt, answer, topic, options=None, question_type=None, explanation=None, image_url=None, max_points=10):
    return {
        "prompt": prompt,
        "answer": str(answer),
        "topic": topic,
        "explanation": explanation or f"정답은 '{answer}'입니다.",
        "question_type": question_type or ("choice" if options else "write"),
        "options": options or [],
        "image_url": image_url,
        "max_points": max_points,
    }


# ───────────────────────────────
# 1~2학년: 학교·가족·동네·안전
# ───────────────────────────────

def _s1_school():
    topic = _topic_for(1, ["학교생활"])
    prompt = "학교에서 우리를 가르쳐 주시는 분은?"
    answer = "선생님"
    return _make(prompt, answer, topic, options=["선생님", "요리사", "운전사", "가수"])


def _s1_safety():
    topic = _topic_for(1, ["안전", "교통안전"])
    prompt = "길을 걷거나 건ize_process갈 때 반드시 지켜야 하는 것은?"
    answer = "횡단볏process도를 이용하고 신호를 지킨다"
    return _make(prompt, answer, topic, options=[
        "횡단볏process도를 이용하고 신호를 지킨다",
        "차가 오는 길을 뛰어 건process는다",
        "무단횡단을 한다",
        "핸드폰을 본process 채 걷는다",
    ])


def _s1_community():
    topic = _topic_for(1, ["우리 동네", "공공기관"])
    prompt = "아플 때 가야 하는 곳은?"
    answer = "병원"
    return _make(prompt, answer, topic, options=["병원", "도서관", "놀이터", "우체국"])


def _s2_map():
    topic = _topic_for(2, ["지도", "우리 동네"])
    prompt = "마을의 중요한 장소와 위치를 간단히 나타낸 그림은?"
    answer = "지도"
    return _make(prompt, answer, topic, options=["지도", "달력", "시계", "엽서"])


def _s2_environment():
    topic = _topic_for(2, ["환경"])
    prompt = "쓰레기를 줄이는 가장 바람직한 방법은?"
    answer = "재사용하고 분리배출한다"
    return _make(prompt, answer, topic, options=[
        "재사용하고 분리배출한다",
        "아무 데나 버린다",
        "모두 태운다",
        "강에 버린다",
    ])


def _s2_public_order():
    topic = _topic_for(2, ["공동생활"])
    prompt = "공공장소에서 다른 사람과 약속한 시간을 지키는 것은 무엇을 보여 주나요?"
    answer = "책임감"
    return _make(prompt, answer, topic, options=["책임감", "용기", "사랑", "호기심"])


# ───────────────────────────────
# 3~4학년: 지도·역사·경제·환경
# ───────────────────────────────

def _s3_map_direction():
    topic = _topic_for(3, ["지도"])
    prompt = "지도에서 동쪽의 반대 방향은?"
    answer = "서쪽"
    return _make(prompt, answer, topic, options=["서쪽", "남쪽", "북쪽", "위쪽"])


def _s3_scale():
    topic = _topic_for(3, ["지도", "축척"])
    prompt = "지도에서 실제 거리를 줄여 나타낸 정도를 무엇이라 하나요?"
    answer = "축척"
    return _make(prompt, answer, topic, options=["축척", "고도", "위도", "경도"])


def _s3_history_source():
    topic = _topic_for(3, ["역사", "역사 자료"])
    prompt = "과거의 사실을 알려 주는 흔적이나 기록은?"
    answer = "역사 자료"
    return _make(prompt, answer, topic, options=["역사 자료", "소설", "광고", "동화"])


def _s3_economy():
    topic = _topic_for(3, ["경제"])
    prompt = "생산한 물건을 사용하는 사람을 무엇이라 하나요?"
    answer = "소비자"
    return _make(prompt, answer, topic, options=["소비자", "생산자", "판매자", "노동자"])


def _s3_environment_human():
    topic = _topic_for(3, ["환경"])
    prompt = "사람들이 살아가며 만든 환경은?"
    answer = "인문환경"
    return _make(prompt, answer, topic, options=["인문환경", "자연환경", "기후", "지형"])


def _s4_capital():
    topic = _topic_for(4, ["대한민국"])
    prompt = "우리나라의 수도는?"
    answer = "서울"
    return _make(prompt, answer, topic, options=["서울", "부산", "인천", "대구"])


def _s4_jeju():
    topic = _topic_for(4, ["지리"])
    prompt = "우리나라에서 가장 큰 섬은?"
    answer = "제주도"
    return _make(prompt, answer, topic, options=["제주도", "울릉도", "독도", "거제도"])


def _s4_local_gov():
    topic = _topic_for(4, ["지역 행정"])
    prompt = "도의 행정을 맡아보는 기관은?"
    answer = "도청"
    return _make(prompt, answer, topic, options=["도청", "시청", "군청", "구청"])


def _s4_democracy():
    topic = _topic_for(4, ["민주주의"])
    prompt = "주민이 지역 대표를 직접 뽑는 것은?"
    answer = "지방 선거"
    return _make(prompt, answer, topic, options=["지방 선거", "재판", "세금", "법 제정"])


def _s4_cultural_heritage():
    topic = _topic_for(4, ["문화유산"])
    prompt = "문화유산 중 형태가 있는 것은?"
    answer = "유형 문화유산"
    return _make(prompt, answer, topic, options=["유형 문화유산", "무형 문화유산", "자연유산", "역사유산"])


# ───────────────────────────────
# 5~6학년: 역사·정치·경제·국제
# ───────────────────────────────

def _s5_asia():
    topic = _topic_for(5, ["국토"])
    prompt = "우리나라가 위치한 대륙은?"
    answer = "아시아"
    return _make(prompt, answer, topic, options=["아시아", "유럽", "아프리카", "북아메리카"])


def _s5_dangun():
    topic = _topic_for(5, ["고대사"])
    prompt = "고조선을 세운 인물로 전해지는 사람은?"
    answer = "단군왕검"
    return _make(prompt, answer, topic, options=["단군왕검", "왕건", "세종대왕", "이순신"])


def _s5_three_kingdoms():
    topic = _topic_for(5, ["고대사"])
    prompt = "삼국을 통일한 나라는?"
    answer = "신라"
    return _make(prompt, answer, topic, options=["신라", "고구려", "백제", "통일신라"])


def _s5_goryeo():
    topic = _topic_for(5, ["고려"])
    prompt = "고려를 세운 인물은?"
    answer = "왕건"
    return _make(prompt, answer, topic, options=["왕건", "단군왕검", "태조", "세종대왕"])


def _s5_sejong():
    topic = _topic_for(5, ["조선"])
    prompt = "훈민정음을 창제한 왕은?"
    answer = "세종대왕"
    return _make(prompt, answer, topic, options=["세종대왕", "태종", "성종", "영조"])


def _s5_constitution():
    topic = _topic_for(5, ["법", "헌법"])
    prompt = "국민의 기본권을 보장하는 국가의 최고 법은?"
    answer = "헌법"
    return _make(prompt, answer, topic, options=["헌법", "민법", "형법", "행정법"])


def _s6_government():
    topic = _topic_for(6, ["국가기관"])
    prompt = "행정부를 이끄는 사람은?"
    answer = "대통령"
    return _make(prompt, answer, topic, options=["대통령", "국회의장", "대법원장", "총리"])


def _s6_court():
    topic = _topic_for(6, ["국가기관"])
    prompt = "법에 따라 재판하는 국가기관은?"
    answer = "법원"
    return _make(prompt, answer, topic, options=["법원", "국회", "행정부", "선관위"])


def _s6_economy_price():
    topic = _topic_for(6, ["경제"])
    prompt = "물건의 가격이 오륍process면 같은 돈으로 살 수 있는 양은?"
    answer = "줄어든다"
    return _make(prompt, answer, topic, options=["줄어든다", "늘어난다", "그대로이다", "두 배가 된다"])


def _s6_korean_war():
    topic = _topic_for(6, ["현대사"])
    prompt = "6·25 전쟁이 시작된 해는?"
    answer = "1950"
    return _make(prompt, answer, topic, options=["1950", "1945", "1948", "1960"])


def _s6_un():
    topic = _topic_for(6, ["국제 사회"])
    prompt = "세계 평화와 협력을 위한 국제기구는?"
    answer = "국제 연합"
    return _make(prompt, answer, topic, options=["국제 연합", "국회", "대법원", "시청"])


# ───────────────────────────────
# 중학년: 지리·역사·정치·경제 심화
# ───────────────────────────────

def _s7_equator():
    topic = _topic_for(7, ["지리"])
    prompt = "위도 0도의 기준선은?"
    answer = "적도"
    return _make(prompt, answer, topic, options=["적도", "경도", "본초 자오선", "회귀선"])


def _s7_climate():
    topic = _topic_for(7, ["지리"])
    prompt = "한 지역의 오랜 기간 동안의 평균적인 날씨 상태는?"
    answer = "기후"
    return _make(prompt, answer, topic, options=["기후", "날씨", "계절", "풍향"])


def _s7_neolithic():
    topic = _topic_for(7, ["역사"])
    prompt = "인류가 농경과 목축을 시작한 시대는?"
    answer = "신석기 시대"
    return _make(prompt, answer, topic, options=["신석기 시대", "구석기 시대", "청동기 시대", "철기 시대"])


def _s7_demand_supply():
    topic = _topic_for(7, ["경제"])
    prompt = "수요가 늘고 공급이 같을 때 가격은 일반적으로?"
    answer = "오른다"
    return _make(prompt, answer, topic, options=["오른다", "내린다", "그대로이다", "변하지 않는다"])


def _s7_sovereignty():
    topic = _topic_for(7, ["정치"])
    prompt = "민주주의에서 국가의 주권을 가진 사람은?"
    answer = "국민"
    return _make(prompt, answer, topic, options=["국민", "대통령", "국회", "법원"])


def _s8_industrial_revolution():
    topic = _topic_for(8, ["세계사"])
    prompt = "산업 혁명이 처음 시작된 나라는?"
    answer = "영국"
    return _make(prompt, answer, topic, options=["영국", "프랑스", "미국", "독일"])


def _s8_separation_powers():
    topic = _topic_for(8, ["정치"])
    prompt = "삼권 분립의 세 권력은?"
    answer = "입법·행정·사법"
    return _make(prompt, answer, topic, options=["입법·행정·사법", "국가·사회·개인", "중앙·지방·국제", "행정·입법·재판"])


def _s8_market_price():
    topic = _topic_for(8, ["경제"])
    prompt = "시장에서 가격을 결정하는 두 힘은?"
    answer = "수요와 공급"
    return _make(prompt, answer, topic, options=["수요와 공급", "생산과 소비", "수출과 수입", "세금과 화폐"])


def _s8_global_warming():
    topic = _topic_for(8, ["환경"])
    prompt = "대기 중 온실가스 증가로 지구 평균 기온이 오르는 현상은?"
    answer = "지구 온난화"
    return _make(prompt, answer, topic, options=["지구 온난화", "오존층 파괴", "산성비", "황사"])


def _s8_human_rights_commission():
    topic = _topic_for(8, ["인권"])
    prompt = "인권 침해를 해결하기 위한 국가기구는?"
    answer = "국가인권위원회"
    return _make(prompt, answer, topic, options=["국가인권위원회", "국회", "대법원", "경찰청"])


def _s9_inflation():
    topic = _topic_for(9, ["경제"])
    prompt = "물가가 지속적으로 상승하는 현상은?"
    answer = "인플레이션"
    return _make(prompt, answer, topic, options=["인플레이션", "디플레이션", "경기 침체", "실업"])


def _s9_globalization():
    topic = _topic_for(9, ["사회"])
    prompt = "국가 간 상호 의존이 깊어지는 현상은?"
    answer = "세계화"
    return _make(prompt, answer, topic, options=["세계화", "도시화", "산업화", "민주화"])


def _s9_constitutional_court():
    topic = _topic_for(9, ["법"])
    prompt = "헌법에 어긋나는 법률인지 심판하는 기관은?"
    answer = "헌법재판소"
    return _make(prompt, answer, topic, options=["헌법재판소", "대법원", "국회", "행정안전부"])


def _s9_march_1st():
    topic = _topic_for(9, ["한국사"])
    prompt = "일제 강점기 3·1 운 동이 일어난 해는?"
    answer = "1919"
    return _make(prompt, answer, topic, options=["1919", "1905", "1945", "1920"])


def _s9_sustainable():
    topic = _topic_for(9, ["환경"])
    prompt = "지속 가능한 발전의 의미로 알맞은 것은?"
    answer = "미래 세대의 필요를 해치지 않으며 현재의 필요를 충족하는 발전"
    return _make(prompt, answer, topic, options=[
        "미래 세대의 필요를 해치지 않으며 현재의 필요를 충족하는 발전",
        "경제 성장만 추구하는 발전",
        "개발을 모두 중단하는 것",
        "자원을 최대한 빨리 쓰는 것",
    ])


GENERATORS = {
    1: [_s1_school, _s1_safety, _s1_community],
    2: [_s2_map, _s2_environment, _s2_public_order],
    3: [_s3_map_direction, _s3_scale, _s3_history_source, _s3_economy, _s3_environment_human],
    4: [_s4_capital, _s4_jeju, _s4_local_gov, _s4_democracy, _s4_cultural_heritage],
    5: [_s5_asia, _s5_dangun, _s5_three_kingdoms, _s5_goryeo, _s5_sejong, _s5_constitution],
    6: [_s6_government, _s6_court, _s6_economy_price, _s6_korean_war, _s6_un],
    7: [_s7_equator, _s7_climate, _s7_neolithic, _s7_demand_supply, _s7_sovereignty],
    8: [_s8_industrial_revolution, _s8_separation_powers, _s8_market_price, _s8_global_warming, _s8_human_rights_commission],
    9: [_s9_inflation, _s9_globalization, _s9_constitutional_court, _s9_march_1st, _s9_sustainable],
}


def _add_solution_questions(questions, grade, count):
    banks = {
        3: [
            ("지도의 축척이 1:10000일 때, 실제 거리 1km는 지도 위에서 몇 cm인가요?", "10", "지도"),
            ("우리 고장의 문화유산을 보호해야 하는 이유를 한 문장으로 쓰세요.", "역사와 문화를 다음 세대에 전달하기 위해", "문화유산"),
        ],
        4: [
            ("민주적 의사 결정에서 왜 소수 의견도 존중해야 하나요?", "모두의 의견을 반영해야 공동체가 화합할 수 있기 때문에", "민주주의"),
            ("지역 특산물이 지역 경제에 미치는 긍정적 영향을 한 가지 쓰세요.", "관광객을 끌어들여 지역 소득이 늘어난다", "지역 경제"),
        ],
        5: [
            ("왜 국민의 기본권을 헌법에 보장해야 하나요?", "국민의 자유와 권리를 국가가 침해하지 못하도록 하기 위해", "헌법"),
            ("다른 문화를 존중해야 하는 이유를 쓰세요.", "서로 다른 가치관과 전통을 인정해야 평화롭게 공존할 수 있다", "문화 다양성"),
        ],
        6: [
            ("인권이 왜 중요한가요?", "모든 사람이 존엄하게 살 기본 권리를 보장하기 위해", "인권"),
            ("세계 여러 나라가 기후 변화를 함께 해결해야 하는 이유는?", "기후 변화는 한 국가만의 문제가 아니라 지구 전체의 문제이기 때문에", "세계 문제"),
        ],
        7: [
            ("민주주의에서 국민이 주권을 가진다는 것의 의미를 쓰세요.", "국가의 중요한 일을 국민의 의사로 결정한다", "정치"),
            ("수요와 공급이 가격에 미치는 영향을 간단히 설명하세요.", "수요가 많고 공급이 적으면 가격이 오르고, 그 반대면 가격이 내린다", "경제"),
        ],
        8: [
            ("삼권 분립이 왜 필요한가요?", "권력이 한 곳에 집중되지 않도록 하여 국민의 자유를 지키기 위해", "정치"),
            ("지구 온난화를 줄이기 위해 우리가 할 수 있는 일을 두 가지 쓰세요.", "대중교통을 이용하고, 에너지 사용을 줄인다", "환경"),
        ],
        9: [
            ("세계화의 긍정적 측면과 부정적 측면을 각각 한 가지씩 쓰세요.", "정보와 물품 교환이 쉬워지지만, 국가 간 격차도 커질 수 있다", "세계화"),
            ("지속 가능한 발전을 위해 정부와 개인이 각각 해야 할 일을 한 가지씩 쓰세요.", "정부는 환경 법규를 만들고, 개인은 자원을 아껴 쓴다", "환경"),
        ],
    }
    bank = banks.get(grade, [])
    if not bank:
        return questions
    needed = min(count - len(questions), len(bank))
    for prompt, answer, topic in random.sample(bank, needed):
        questions.append(_make(prompt, answer, topic, question_type="solution", explanation=f"정답 예시: {answer}", max_points=15))
    return questions


def generate_social_set(grade, count=10):
    generators = GENERATORS.get(grade, GENERATORS[9])
    questions = []
    # 기본 문제 채우기
    while len(questions) < count - min(2, grade if grade >= 3 else 0):
        g = random.choice(generators)
        questions.append(g())
    # 3학년 이상은 풀이형 추가
    if grade >= 3:
        questions = _add_solution_questions(questions, grade, count)
    random.shuffle(questions)
    return questions[:count]
