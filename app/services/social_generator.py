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


# ============================================================
# 추가 보충 문제 (교육청 기반)
# ============================================================
def _s1_house_safety():
    topic = _topic_for(1, ["안전", "생활 안전"])
    prompt = "집에서 화재가 났을 때 가장 먼저 해야 할 일은?"
    answer = "침착하게 119에 신고하고 대피한다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "물건을 챙긴다",
        "엘리베이터를 탄다",
        "창문을 닫고 숨는다",
    ]))


def _s1_school_rule():
    topic = _topic_for(1, ["학교 생활", "규칙"])
    prompt = "학교에서 친구와 함께 지낼 때 가장 중요한 것은?"
    answer = "서로의 차례를 기다리고 배려한다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "먼저 자기 차례를 만든다",
        "친구의 의견을 무시한다",
        "혼자서 모든 것을 결정한다",
    ]))


def _s1_family_role():
    topic = _topic_for(1, ["가족", "나와 가족"])
    prompt = "가족들이 함께 집안일을 하는 이유는?"
    answer = "모두가 편안하게 생활할 수 있기 때문이다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "한 사람만 일하게 하기 때문이다",
        "집안일이 재미있기 때문이다",
        "학교 숙제를 하기 때문이다",
    ]))


def _s1_neighbor():
    topic = _topic_for(1, ["우리 동네", "지역 사회"])
    prompt = "이웃과 좋은 관계를 유지하려면 어떻게 해야 하나요?"
    answer = "서로 인사하고 필요할 때 도와준다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "시끄럽게 뛰어다닌다",
        "이웃의 사생활을 무시한다",
        "쓰레기를 남의 집 앞에 버린다",
    ]))


def _s2_water_save():
    topic = _topic_for(2, ["환경", "자원 절약"])
    prompt = "물을 절약하는 생활 습관은 무엇인가요?"
    answer = "양치할 때 컵에 물을 담아 사용한다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "수도꼭지를 켜놓고 칫솔을 짠다",
        "물을 마시고 남은 것을 그냥 버린다",
        "샤워 시간을 길게 한다",
    ]))


def _s2_tradition_clothes():
    topic = _topic_for(2, ["전통", "문화"])
    prompt = "우리나라의 대표적인 전통 옷은 무엇인가요?"
    answer = "한복"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["양복", "기모노", "한복", "치파오"]))


def _s2_public_place():
    topic = _topic_for(2, ["공공장소", "공동체"])
    prompt = "공공장소에서 지켜야 할 예절은?"
    answer = "줄을 서서 차례를 기다린다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "큰 소리로 떠든다",
        "바닥에 쓰레기를 버린다",
        "원하는 곳에 바로 뛰어든다",
    ]))


def _s2_friendship():
    topic = _topic_for(2, ["친구", "공동체"])
    prompt = "친구가 어려움을 겪을 때 바른 행동은?"
    answer = "친구의 마음을 이해하고 도와준다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "혼자 해결하라고 한다",
        "다른 친구에게 말한다",
        "친구를 놀린다",
    ]))


def _s3_product():
    topic = _topic_for(3, ["경제", "생산과 소비"])
    prompt = "농부가 밭에서 쌀을 생산하면 우리는 이것을 무엇이라 하나요?"
    answer = "농산물"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["공산품", "농산물", "수산물", "임산물"]))


def _s3_transport_modern():
    topic = _topic_for(3, ["교통", "통신"])
    prompt = "현재 우리가 멀리 있는 친구와 빠르게 소식을 주고받을 수 있는 것은?"
    answer = "스마트폰"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["편지", "우편", "전보", "스마트폰"]))


def _s3_historic_site():
    topic = _topic_for(3, ["문화유산", "역사"])
    prompt = "우리나라의 문화유산을 보존하는 이유는?"
    answer = "역사와 문화를 후대에 전하기 위해서이다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "관광객을 많이 모으기 위해서이다",
        "건물을 허물기 위해서이다",
        "옛날 생활을 잊기 위해서이다",
    ]))


def _s3_direction():
    topic = _topic_for(3, ["지도", "지리"])
    prompt = "지도에서 '→' 모양 화살표는 보통 무엇을 나타낼까요?"
    answer = "동쪽"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["서쪽", "남쪽", "동쪽", "북쪽"]))


def _s4_map():
    topic = _topic_for(4, ["지도", "지리"])
    prompt = "지도의 축척이 크면 나타내는 범위는?"
    answer = "좁은 지역을 자세히 나타낸다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "넓은 지역을 간략히 나타낸다",
        "좁은 지역을 자세히 나타낸다",
        "세계 전체를 나타낸다",
        "바다만 나타낸다",
    ]))


def _s4_industry():
    topic = _topic_for(4, ["경제", "지역"])
    prompt = "공장에서 물건을 많이 만들어 판매하는 활동은?"
    answer = "제조업"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["농업", "어업", "제조업", "임업"]))


def _s4_energy():
    topic = _topic_for(4, ["에너지", "환경"])
    prompt = "다음 중 재생 가능한 에너지는?"
    answer = "태양광"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["석유", "석탄", "태양광", "천연가스"]))


def _s4_local_gov():
    topic = _topic_for(4, ["지역 행정", "시민성"])
    prompt = "우리 동네의 쓰레기 수거와 도로 관리를 담당하는 기관은?"
    answer = "지방자치단체"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "국회",
        "지방자치단체",
        "대법원",
        "중앙은행",
    ]))


def _s5_science():
    topic = _topic_for(5, ["과학문화", "역사"])
    prompt = "조선 시대 천문과 관측을 위해 만든 기구는?"
    answer = "혼천의"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["혼천의", "거중기", "자격루", "쇠뇌"]))


def _s5_trade():
    topic = _topic_for(5, ["경제", "무역"])
    prompt = "우리나라가 다른 나라에 물건을 파는 것은?"
    answer = "수출"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["수입", "수출", "저축", "투자"]))


def _s5_tax():
    topic = _topic_for(5, ["시민성", "경제"])
    prompt = "국민이 납부하는 세금은 주로 어디에 사용되나요?"
    answer = "학교, 병원, 도로 등 공공시설에 사용된다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "정치인의 개인 재산으로 사용된다",
        "학교, 병원, 도로 등 공공시설에 사용된다",
        "다른 나라에 나누어 준다",
        "은행에만 보관된다",
    ]))


def _s5_heritage():
    topic = _topic_for(5, ["문화유산", "역사"])
    prompt = "유네스코 세계문화유산으로 등재된 우리나라 고궁은?"
    answer = "창덕궁"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["경복궁", "창덕궁", "덕수궁", "경희궁"]))


def _s6_un():
    topic = _topic_for(6, ["국제", "세계"])
    prompt = "세계의 평화와 협력을 위해 설립된 국제기구는?"
    answer = "국제연합(UN)"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "세계은행",
        "국제연합(UN)",
        "국제올림픽위원회",
        "세계무역기구",
    ]))


def _s6_economy_bank():
    topic = _topic_for(6, ["경제", "금융"])
    prompt = "우리나라의 화폐를 발행하는 기관은?"
    answer = "한국은행"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["한국은행", "국세청", "금융감독원", "서울시"]))


def _s6_independence():
    topic = _topic_for(6, ["근현대사", "한국사"])
    prompt = "1945년 일제의 식민 지배가 끝나고 우리나라가 항복한 것은?"
    answer = "광복"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["개항", "광복", "건국", "통일"]))


def _s6_media():
    topic = _topic_for(6, ["미디어", "정보"])
    prompt = "뉴스를 볼 때 출처와 작성 날짜를 확인하는 이유는?"
    answer = "신뢰할 수 있는 정보인지 판단하기 위해서이다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "기사를 외우기 위해서이다",
        "신뢰할 수 있는 정보인지 판단하기 위해서이다",
        "댓글을 많이 달기 위해서이다",
        "사진을 저장하기 위해서이다",
    ]))


def _s7_history():
    topic = _topic_for(7, ["역사", "한국사"])
    prompt = "고려 시대 목판 인쇄술로 인쇄된 세계 최고의 금속활자본은?"
    answer = "직지심체요절"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["삼국사기", "직지심체요절", "동의보감", "훈민정음"]))


def _s7_geography():
    topic = _topic_for(7, ["지리", "자연"])
    prompt = "우리나라 여름에 많은 비를 가져오는 기단은?"
    answer = "장마전선"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["시베리아 고기압", "장마전선", "태풍", "북태평양 고기압"]))


def _s7_culture():
    topic = _topic_for(7, ["사회문화", "문화"])
    prompt = "다른 문화를 자신의 문화 기준으로 평가하지 않는 태도는?"
    answer = "문화 상대주의"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["문화 우월주의", "문화 상대주의", "문화 절대주의", "문화 차별"]))


def _s7_rights():
    topic = _topic_for(7, ["인권", "시민성"])
    prompt = "헌법에 보장된 국민의 기본권으로 알맞지 않은 것은?"
    answer = "남을 해칠 자유"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "언론의 자유",
        "남을 해칠 자유",
        "교육을 받을 권리",
        "선거권",
    ]))


def _s8_history():
    topic = _topic_for(8, ["세계사", "근대"])
    prompt = "18세기 프랑스에서 일어나 시민 혁명의 원칙이 된 것은?"
    answer = "자유, 평등, 박애"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "신분, 특권, 절대왕정",
        "자유, 평등, 박애",
        "군주, 교회, 귀족",
        "식민, 전쟁, 무역",
    ]))


def _s8_economy():
    topic = _topic_for(8, ["경제", "시장"])
    prompt = "시장 경제에서 가격은 주로 무엇에 의해 결정되나요?"
    answer = "수요와 공급"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["정부 명령", "수요와 공급", "기업 광고", "소비자 연령"]))


def _s8_geography2():
    topic = _topic_for(8, ["지리", "세계"])
    prompt = "인구가 많이 몰려 대도시가 형성되는 지형은?"
    answer = "평야"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["산맥", "평야", "사막", "빙하"]))


def _s8_media():
    topic = _topic_for(8, ["미디어", "정보"])
    prompt = "인터넷 정보를 사용할 때 가장 먼저 확인해야 할 것은?"
    answer = "출처의 신뢰성"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "출처의 신뢰성",
        "글자 수",
        "이미지 크기",
        "광고 포함 여부",
    ]))


def _s9_history():
    topic = _topic_for(9, ["한국사", "근현대"])
    prompt = "1919년 일제에 맞서 민족의 자주독립을 외친 대규모 독립운동은?"
    answer = "3·1 운동"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["6·10 만세운동", "3·1 운동", "광복절", "임시정부 수립"]))


def _s9_economy2():
    topic = _topic_for(9, ["경제", "거시"])
    prompt = "물가가 지속적으로 오르는 경제 현상은?"
    answer = "인플레이션"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["디플레이션", "인플레이션", "경기 침체", "실업"]))


def _s9_world():
    topic = _topic_for(9, ["국제", "세계"])
    prompt = "국제 분쟁을 평화적으로 해결하기 위한 국제연합 주요 기구는?"
    answer = "국제사법재판소"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "국제사법재판소",
        "세계은행",
        "국제통화기금",
        "유네스코",
    ]))


def _s9_ethics():
    topic = _topic_for(9, ["윤리", "시민성"])
    prompt = "다양한 사람들이 함께 살아가는 사회에서 가장 중요한 가치는?"
    answer = "존중과 포용"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "경쟁과 승리",
        "존중과 포용",
        "차별과 배제",
        "무시와 편견",
    ]))


def _s7_government():
    topic = _topic_for(7, ["정치", "국가"])
    prompt = "대한민국 정부의 권력은 몇 갈래로 나뉘어 있나요?"
    answer = "3갈래"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["2갈래", "3갈래", "4갈래", "5갈래"]))


def _s7_economy_trade():
    topic = _topic_for(7, ["경제", "무역"])
    prompt = "다른 나라에서 물건을 사 들이는 것은?"
    answer = "수입"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["수출", "수입", "생산", "분배"]))


def _s7_religion():
    topic = _topic_for(7, ["역사", "문화"])
    prompt = "고려 시대 불교 문화의 대표적인 유산은?"
    answer = "팔만대장경"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["팔만대장경", "직지심체요절", "훈민정음", "삼국사기"]))


def _s7_population():
    topic = _topic_for(7, ["지리", "인구"])
    prompt = "인구가 많이 모여 사는 지역을 무엇이라 하나요?"
    answer = "도시"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["농촌", "도시", "어촌", "임촌"]))


def _s8_colonial():
    topic = _topic_for(8, ["한국사", "근현대"])
    prompt = "일제강점기 우리 민족의 독립 의지를 보여준 사건은?"
    answer = "3·1 운동"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["갑오개혁", "3·1 운동", "을사늑약", "경부선 개통"]))


def _s8_market():
    topic = _topic_for(8, ["경제", "시장"])
    prompt = "시장에서 소비자의 구매 의향을 무엇이라 하나요?"
    answer = "수요"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["수요", "공급", "생산", "유통"]))


def _s8_climate():
    topic = _topic_for(8, ["지리", "기후"])
    prompt = "적도 부근의 기후 특징은?"
    answer = "연중 덥고 비가 많다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "사계절이 뚜렷하다",
        "연중 덥고 비가 많다",
        "건조하고 일교차가 크다",
        "연중 추운 편이다",
    ]))


def _s8_society():
    topic = _topic_for(8, ["사회문화", "변화"])
    prompt = "산업 혁명 이후 사회에 가장 큰 변화는?"
    answer = "공장이 생기고 도시가 발전했다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "농업이 더욱 중요해졌다",
        "공장이 생기고 도시가 발전했다",
        "인구가 농촌으로 돌아갔다",
        "왕의 권력이 강화되었다",
    ]))


def _s9_constitution():
    topic = _topic_for(9, ["정치", "헌법"])
    prompt = "대한민국의 주권은 누구에게 있다고 헌법에 규정되어 있나요?"
    answer = "국민"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["국민", "대통령", "국회", "정부"]))


def _s9_coldwar():
    topic = _topic_for(9, ["세계사", "국제"])
    prompt = "냉전 시대 서방 진영의 대표적인 군사 동맹은?"
    answer = "NATO"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["유엔", "NATO", "바르샤바 조약기구", "유럽연합"]))


def _s9_environment():
    topic = _topic_for(9, ["환경", "지속가능"])
    prompt = "지속 가능한 발전을 위해서 가장 중요한 것은?"
    answer = "현재 세대의 욕구를 충족하면서 미래 세대의 가능성을 해치지 않는 것"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "자원을 최대한 많이 사용하는 것",
        "현재 세대의 욕구를 충족하면서 미래 세대의 가능성을 해치지 않는 것",
        "환경 보호만 우선하는 것",
        "경제 성장을 멈추는 것",
    ]))


def _s9_labor():
    topic = _topic_for(9, ["경제", "노동"])
    prompt = "근로자의 권리를 보호하기 위해 마련된 기준은?"
    answer = "최저임금"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["최저임금", "시장가격", "물가상승률", "환율"]))

PROBLEM_GENERATORS = {
    1: [_s1_safety, _s1_family, _s1_school, _s1_community, _s1_polite, _s1_traffic_sign, _s1_house_safety, _s1_school_rule, _s1_family_role, _s1_neighbor],
    2: [_s2_community, _s2_environment, _s2_tradition, _s2_safety, _s2_recycle, _s2_map_symbol, _s2_water_save, _s2_tradition_clothes, _s2_public_place, _s2_friendship],
    3: [_s3_local, _s3_transport, _s3_old_life, _s3_map, _s3_communication, _s3_food, _s3_product, _s3_transport_modern, _s3_historic_site, _s3_direction],
    4: [_s4_nature, _s4_culture, _s4_sustainable, _s4_local_history, _s4_climate, _s4_job, _s4_map, _s4_industry, _s4_energy, _s4_local_gov],
    5: [_s5_history, _s5_politics, _s5_economy, _s5_law, _s5_invention, _s5_geography, _s5_science, _s5_trade, _s5_tax, _s5_heritage],
    6: [_s6_history, _s6_modern, _s6_world, _s6_human_rights, _s6_election, _s6_culture, _s6_un, _s6_economy_bank, _s6_independence, _s6_media],
    7: [_s7_constitution, _s7_economy_price, _s7_history, _s7_geography, _s7_culture, _s7_rights, _s7_government, _s7_economy_trade, _s7_religion, _s7_population],
    8: [_s8_geography, _s7_constitution, _s8_history, _s8_economy, _s8_geography2, _s8_media, _s8_colonial, _s8_market, _s8_climate, _s8_society],
    9: [_s9_citizen, _s7_economy_price, _s9_history, _s9_economy2, _s9_world, _s9_ethics, _s9_constitution, _s9_coldwar, _s9_environment, _s9_labor],
}


def generate_social_set(grade, count=10):
    generators = PROBLEM_GENERATORS.get(grade, PROBLEM_GENERATORS[9])
    questions = []
    seen = set()
    attempts = 0
    while len(questions) < count and attempts < count * 50:
        q = random.choice(generators)()
        key = (q["prompt"], q["question_type"])
        if key not in seen:
            seen.add(key)
            questions.append(q)
        attempts += 1
    # 유일한 문항 풀이 부족할 때만 중복 허용
    while len(questions) < count:
        q = random.choice(generators)()
        questions.append(q)
    random.shuffle(questions)
    return questions
