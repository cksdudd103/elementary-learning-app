import random


def _make(prompt, answer, topic, options=None, question_type=None, explanation=None, image_url=None, max_points=10):
    return {
        "prompt": prompt,
        "answer": str(answer),
        "topic": topic,
        "explanation": explanation or f"정답: {answer}",
        "question_type": question_type or ("choice" if options else "write"),
        "options": options or [],
        "image_url": image_url,
        "max_points": max_points,
    }


def _choice_options(answer, distractors, shuffle=True):
    answer_str = str(answer)
    opts = [answer_str]
    for d in distractors:
        ds = str(d)
        if ds != answer_str and ds not in opts:
            opts.append(ds)
    if shuffle:
        random.shuffle(opts)
    return opts


def _topic_for(grade, fallback):
    try:
        from ..models import CurriculumUnit
        units = CurriculumUnit.query.filter_by(subject="social", grade_level=grade).order_by(CurriculumUnit.unit_order).all()
        if units:
            return random.choice([u.unit_name for u in units])
    except Exception:
        pass
    return random.choice(fallback)


# ============================================================
# 1학년: 안전, 나와 가족, 우리 반/학교
# ============================================================
def _s1_safety():
    topic = _topic_for(1, ["안전", "교통안전"])
    prompt = "길을 걷거나 걸어갈 때 반드시 지켜야 하는 것은?"
    answer = "횡단보도를 이용하고 신호를 지킨다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "차가 오는 길을 뛰어 걷는다",
        "무단횡단을 한다",
        "핸드폰을 본 채 걷는다",
    ]))


def _s1_family():
    topic = _topic_for(1, ["나와 가족", "가족"])
    prompt = "가족은 서로 어떤 마음으로 지내야 하나요?"
    answer = "사랑하고 존중한다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "사랑하고 존중한다",
        "시합에서 이기려 한다",
        "서로 비교한다",
        "자기 것만 챙긴다",
    ]))


def _s1_school():
    topic = _topic_for(1, ["우리 반", "학교 생활"])
    prompt = "학교에서 친구들과 함께 지낼 때 가장 중요한 것은?"
    answer = "서로 배려하고 도운다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "서로 배려하고 도운다",
        "혼자 노는 것",
        "싸우는 것",
        "남의 것을 가져오는 것",
    ]))


def _s1_community():
    topic = _topic_for(1, ["우리 동네", "지역 사회"])
    prompt = "우리 동네를 깨끗하게 유지하려면 어떻게 해야 하나요?"
    answer = "쓰레기를 분리배출한다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "쓰레기를 분리배출한다",
        "길에 쓰레기를 버린다",
        "남의 집에 들어간다",
        "소리를 크게 낸다",
    ]))


# ============================================================
# 2학년: 공동체, 환경, 전통, 안전
# ============================================================
def _s2_community():
    topic = _topic_for(2, ["공동체", "지역 사회"])
    prompt = "마을 사람들이 함께 해야 할 일은 무엇인가요?"
    answer = "서로 돕고 공동체를 지킨다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "서로 돕고 공동체를 지킨다",
        "각자만 산다",
        "다른 사람을 외면한다",
        "규칙을 어긴다",
    ]))


def _s2_environment():
    topic = _topic_for(2, ["환경", "자연"])
    prompt = "깨끗한 환경을 위해 우리가 실천할 수 있는 것은?"
    answer = "일회용품을 줄이고 분리배출한다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "일회용품을 줄이고 분리배출한다",
        "나무를 마음대로 자른다",
        "물을 낭비한다",
        "동물을 괴롭힌다",
    ]))


def _s2_tradition():
    topic = _topic_for(2, ["전통", "문화"])
    prompt = "우리나라의 대표적인 전통 음식은 무엇인가요?"
    answer = "김치"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["피자", "초밥", "김치", "햄버거"]))


def _s2_safety():
    topic = _topic_for(2, ["안전", "생활 안전"])
    prompt = "불이 났을 때 가장 먼저 해야 할 것은?"
    answer = "침착하게 119에 신고한다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "침착하게 119에 신고한다",
        "집 안에 계속 있는다",
        "물건을 챙기다가 나간다",
        "엘리베이터를 탄다",
    ]))


# ============================================================
# 3학년: 고장/지역, 교통·통신, 옛 생활, 지도
# ============================================================
def _s3_local():
    topic = _topic_for(3, ["고장", "지역"])
    prompt = "우리 고장의 대표적인 명소나 특산물을 아는 대로 쓰세요."
    answer = "지역에 따라 다름"
    return _make(prompt, answer, topic, question_type="write", explanation="자신이 사는 지역의 특징을 쓰면 됩니다.")


def _s3_transport():
    topic = _topic_for(3, ["교통", "통신"])
    prompt = "과거와 현재의 교통수단 차이로 알맞은 것은?"
    answer = "과거에는 말을 타고 다녔고, 지금은 자동차와 기차를 탄다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "과거에는 말을 타고 다녔고, 지금은 자동차와 기차를 탄다",
        "과거와 지금이 똑같다",
        "과거에 비행기가 많았다",
        "지금은 말을 주로 탄다",
    ]))


def _s3_old_life():
    topic = _topic_for(3, ["옛 생활", "역사"])
    prompt = "옛날 사람들의 생활 모습으로 알맞은 것은?"
    answer = "농사를 짓고 직접 만든 도구를 사용했다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "농사를 짓고 직접 만든 도구를 사용했다",
        "컴퓨터로 공부했다",
        "자동차를 타고 다녔다",
        "스마트폰으로 통화했다",
    ]))


def _s3_map():
    topic = _topic_for(3, ["지도", "지리"])
    prompt = "지도에서 위쪽은 보통 어느 방향을 나타낼까요?"
    answer = "북쪽"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["남쪽", "동쪽", "서쪽", "북쪽"]))


# ============================================================
# 4학년: 자연환경, 인문환경, 지속가능한 세계, 지역사
# ============================================================
def _s4_nature():
    topic = _topic_for(4, ["자연환경", "지리"])
    prompt = "강이나 산과 같은 자연환경이 사람 생활에 미치는 영향은?"
    answer = "농사, 교통, 생활에 영향을 준다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "농사, 교통, 생활에 영향을 준다",
        "아무 영향이 없다",
        "사람을 위험하게만 한다",
        "오직 관광용으로만 쓰인다",
    ]))


def _s4_culture():
    topic = _topic_for(4, ["인문환경", "사회·문화"])
    prompt = "우리나라의 전통 문화유산으로 알맞은 것은?"
    answer = "경복궁"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["에펠탑", "자유의 여신상", "경복궁", "피사의 사탑"]))


def _s4_sustainable():
    topic = _topic_for(4, ["지속가능한 세계", "환경"])
    prompt = "지속가능한 사회를 만들기 위해 가장 필요한 것은?"
    answer = "자원을 아끼고 환경을 보호한다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "자원을 아끼고 환경을 보호한다",
        "많이 쓰고 많이 버린다",
        "자연을 모두 개발한다",
        "다른 나라만 책임진다",
    ]))


def _s4_local_history():
    topic = _topic_for(4, ["지역사", "역사"])
    prompt = "우리 지역의 역사를 알 수 있는 방법은?"
    answer = "유적지나 박물관을 찾아본다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "유적지나 박물관을 찾아본다",
        "게임을 한다",
        "무조건 외운다",
        "신문 광고만 본다",
    ]))


# ============================================================
# 5학년: 한국사(고조선~통일신라), 정치·법, 경제 기초
# ============================================================
def _s5_history():
    topic = _topic_for(5, ["역사", "한국사"])
    prompt = "우리나라 최초의 국가로 알려진 것은?"
    answer = "고조선"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["고려", "조선", "고조선", "백제"]))


def _s5_politics():
    topic = _topic_for(5, ["정치", "시민성"])
    prompt = "민주주의 국가에서 국민이 가져야 할 중요한 자세는?"
    answer = "서로의 의견을 존중한다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "서로의 의견을 존중한다",
        "힘센 사람의 말만 따른다",
        "법을 어겨도 된다",
        "선거에 참여하지 않는다",
    ]))


def _s5_economy():
    topic = _topic_for(5, ["경제", "시장"])
    prompt = "물건의 가격이 오르면 같은 돈으로 살 수 있는 양은?"
    answer = "줄어든다"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["줄어든다", "늘어난다", "그대로이다", "두 배가 된다"]))


def _s5_law():
    topic = _topic_for(5, ["법", "권리와 의무"])
    prompt = "다른 사람의 물건을 훔치는 행위는 어떤 문제가 되나요?"
    answer = "범죄가 되어 처벌받는다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "범죄가 되어 처벌받는다",
        "아무 문제가 없다",
        "칭찬받는다",
        "학교에서 상을 받는다",
    ]))


# ============================================================
# 6학년: 한국사(고려~현대), 경제, 세계, 인권/다문화
# ============================================================
def _s6_history():
    topic = _topic_for(6, ["역사", "한국사"])
    prompt = "세종대왕이 만든 우리나라 글자는?"
    answer = "훈민정음"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["한문", "훈민정음", "라틴어", "영어"]))


def _s6_modern():
    topic = _topic_for(6, ["근현대사", "한국사"])
    prompt = "대한민국이 수립된 해는?"
    answer = "1948년"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["1910년", "1945년", "1948년", "1950년"]))


def _s6_world():
    topic = _topic_for(6, ["세계", "국제"])
    prompt = "세계 여러 나라와 평화롭게 지내기 위해 필요한 것은?"
    answer = "서로의 문화를 존중하고 대화한다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "서로의 문화를 존중하고 대화한다",
        "전쟁으로 해결한다",
        "자기 나라만 중요하게 여긴다",
        "다른 나라를 무시한다",
    ]))


def _s6_human_rights():
    topic = _topic_for(6, ["인권", "다문화"])
    prompt = "다문화 사회에서 서로 다른 사람을 대하는 바람직한 태도는?"
    answer = "차이를 존중하고 함께 어울린다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "차이를 존중하고 함께 어울린다",
        "놀리고 따돌린다",
        "자기와 똑같아야 한다고 강요한다",
        "다른 사람의 말을 무시한다",
    ]))


# ============================================================
# 중학년 (7~9): 기존 수준 유지
# ============================================================
def _s7_constitution():
    topic = _topic_for(7, ["정치", "헌법"])
    prompt = "대한민국의 국민이 누려야 할 기본권은?"
    answer = "인권"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["특권", "면제권", "인권", "사유권"]))


def _s7_economy_price():
    topic = _topic_for(7, ["경제", "시장"])
    prompt = "수요가 많고 공급이 적으면 가격은 어떻게 되나요?"
    answer = "오른다"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["내린다", "오른다", "그대로다", "없어진다"]))


def _s8_geography():
    topic = _topic_for(8, ["지리", "세계"])
    prompt = "한반도의 위치로 알맞은 것은?"
    answer = "동아시아에 위치한다"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["유럽에 있다", "동아시아에 위치한다", "아프리카에 있다", "남아메리카에 있다"]))


def _s9_citizen():
    topic = _topic_for(9, ["시민성", "민주주의"])
    prompt = "민주주의 사회의 핵심 가치는?"
    answer = "자유와 평등"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["강제와 복종", "자유와 평등", "차별과 배제", "독점과 억압"]))



def _s1_polite():
    topic = _topic_for(1, ["바른 생활", "예의"])
    prompt = "친구와 대화할 때 바른 태도는 무엇인가요?"
    answer = "상대방의 말을 끝까지 듣는다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "끊고 자기 말만 한다",
        "소리를 지르며 말한다",
        "등을 돌린 채 말한다",
    ]))


def _s1_traffic_sign():
    topic = _topic_for(1, ["교통안전", "안전"])
    prompt = "빨간불이 켜진 횡단보도에서 해야 할 것은?"
    answer = "멈춰서 신호가 바뀔 때까지 기다린다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "빨리 뛰어 걷는다",
        "차가 없으면 그냥 걷는다",
        "친구를 밀고 먼저 걷는다",
    ]))


def _s2_recycle():
    topic = _topic_for(2, ["환경", "자원 절약"])
    prompt = "다음 중 올바른 분리배출 방법은?"
    answer = "플라스틱은 깨끗이 씻어서 배출한다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "음식물이 묻은 용기를 그대로 버린다",
        "유리와 플라스틱을 함께 넣는다",
        "모든 쓰레기를 한 종류로 버린다",
    ]))


def _s2_map_symbol():
    topic = _topic_for(2, ["지도", "지리"])
    prompt = "지도에서 ㅇㅇ 모양으로 나타내는 것은?"
    answer = "학교"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["산", "강", "병원", "학교"]))


def _s3_communication():
    topic = _topic_for(3, ["통신", "과거와 현재"])
    prompt = "과거 사람들이 먼 곳에 소식을 전할 때 사용한 것은?"
    answer = "편지"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["휴대전화", "이메일", "비디오 통화", "편지"]))


def _s3_food():
    topic = _topic_for(3, ["지역", "문화"])
    prompt = "전라도 지역의 대표적인 음식은 무엇인가요?"
    answer = "비빔밥"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["냉면", "비빔밥", "핫도그", "초밥"]))


def _s4_climate():
    topic = _topic_for(4, ["기후", "지리"])
    prompt = "우리나라의 여름철 날씨 특징은?"
    answer = "덥고 비가 많이 온다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "춥고 눈이 많이 온다",
        "바람이 강하게 분다",
        "건조하고 안개가 짙다",
    ]))


def _s4_job():
    topic = _topic_for(4, ["직업", "경제"])
    prompt = "우리 지역에서 사람들의 안전을 지키는 직업은?"
    answer = "경찰관"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["화가", "경찰관", "운동선수", "요리사"]))


def _s5_invention():
    topic = _topic_for(5, ["과학문화", "역사"])
    prompt = "세종대왕이 백성들을 위해 만든 것은?"
    answer = "훈민정음"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["삼국사기", "훈민정음", "동의보감", "직지심체요절"]))


def _s5_geography():
    topic = _topic_for(5, ["지리", "한국"])
    prompt = "우리나라에서 가장 높은 산은?"
    answer = "한라산"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["한라산", "지리산", "북한산", "금강산"]))


def _s6_election():
    topic = _topic_for(6, ["선거", "민주주의"])
    prompt = "민주주의 국가에서 국민이 직접 뽑는 대표는?"
    answer = "대통령"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["대통령", "판사", "공무원", "경찰관"]))


def _s6_culture():
    topic = _topic_for(6, ["세계", "문화"])
    prompt = "다른 나라의 문화를 존중하는 이유는?"
    answer = "모든 사람은 존중받을 가치가 있기 때문이다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "우리 문화가 더 우수하기 때문이다",
        "다른 나라를 무시하면 싸움이 나기 때문이다",
        "관광객을 많이 받기 때문이다",
    ]))

PROBLEM_GENERATORS = {
    1: [_s1_safety, _s1_family, _s1_school, _s1_community, _s1_polite, _s1_traffic_sign],
    2: [_s2_community, _s2_environment, _s2_tradition, _s2_safety, _s2_recycle, _s2_map_symbol],
    3: [_s3_local, _s3_transport, _s3_old_life, _s3_map, _s3_communication, _s3_food],
    4: [_s4_nature, _s4_culture, _s4_sustainable, _s4_local_history, _s4_climate, _s4_job],
    5: [_s5_history, _s5_politics, _s5_economy, _s5_law, _s5_invention, _s5_geography],
    6: [_s6_history, _s6_modern, _s6_world, _s6_human_rights, _s6_election, _s6_culture],
    7: [_s7_constitution, _s7_economy_price],
    8: [_s8_geography, _s7_constitution],
    9: [_s9_citizen, _s7_economy_price],
}


def generate_social_set(grade, count=10):
    generators = PROBLEM_GENERATORS.get(grade, PROBLEM_GENERATORS[9])
    questions = []
    seen = set()
    attempts = 0
    while len(questions) < count and attempts < count * 30:
        q = random.choice(generators)()
        key = (q["prompt"], q["question_type"])
        if key not in seen:
            seen.add(key)
            questions.append(q)
        attempts += 1
    while len(questions) < count:
        questions.append(random.choice(generators)())
    random.shuffle(questions)
    return questions
