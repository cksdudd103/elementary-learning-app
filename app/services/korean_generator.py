import random


def _make(prompt, answer, topic, options=None, question_type=None, explanation=None, max_points=10):
    return {
        "prompt": prompt,
        "answer": str(answer),
        "topic": topic,
        "explanation": explanation or f"정답: {answer}",
        "question_type": question_type or ("choice" if options else "write"),
        "options": options or [],
        "max_points": max_points,
    }


def _topic_for(grade, fallback):
    try:
        from ..models import CurriculumUnit
        units = CurriculumUnit.query.filter_by(subject="korean", grade_level=grade).order_by(CurriculumUnit.unit_order).all()
        if units:
            return random.choice([u.unit_name for u in units])
    except Exception:
        pass
    return random.choice(fallback)


# ============================================================
# 1학년: 글자 읽기, 낱말, 문장 부호, 반대말
# ============================================================
def _k1_consonant_vowel():
    consonants = ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
    vowels = ["ㅏ", "ㅑ", "ㅓ", "ㅕ", "ㅗ", "ㅛ", "ㅜ", "ㅠ", "ㅡ", "ㅣ"]
    c, v = random.choice(consonants), random.choice(vowels)
    topic = _topic_for(1, ["자음과 모음", "낱말 읽기"])
    prompt = f"'{c}'와 '{v}'를 합치면 무엇이 되나요?"
    answer = f"{c}{v}"
    return _make(prompt, answer, topic, options=_choice_options(answer, [f"{v}{c}", c, v]))


def _k1_word_reading():
    words = [
        ("나무", "식물"), ("바다", "자연"), ("학교", "장소"),
        ("친구", "사람"), ("가방", "물건"), ("구름", "자연"),
        ("고양이", "동물"), ("책", "물건"),
    ]
    word, meaning = random.choice(words)
    topic = _topic_for(1, ["낱말 읽기", "어휘"])
    prompt = f"'{word}'는 다음 중 무엇에 해당하나요?"
    distractors = list({m for _, m in words if m != meaning})
    return _make(prompt, meaning, topic, options=_choice_options(meaning, random.sample(distractors, min(3, len(distractors)))), explanation=f"'{word}'는 {meaning}에 해당합니다.")


def _k1_opposite():
    pairs = [("크다", "작다"), ("높다", "낮다"), ("빠르다", "느리다"), ("많다", "적다"), ("밝다", "어둡다")]
    a, b = random.choice(pairs)
    topic = _topic_for(1, ["반대말", "어휘"])
    word, answer = random.choice([(a, b), (b, a)])
    prompt = f"'{word}'의 반대말은 무엇인가요?"
    return _make(prompt, answer, topic, options=_choice_options(answer, [a, b, word]))


def _k1_sentence_punct():
    sentences = [
        ("나는 사과를 좋아한다", "."),
        ("학교에 갔니", "?"),
        ("정말 멋지다", "!"),
    ]
    sentence, answer = random.choice(sentences)
    topic = _topic_for(1, ["문장과 문단", "문장 부호"])
    prompt = f"'{sentence}' 끝에 올 문장 부호는?"
    return _make(prompt, answer, topic, options=_choice_options(answer, [",", ";", ":"]))


# ============================================================
# 2학년: 비슷한말, 주어/서술어, 짧은 문장 이해, 문장 부호
# ============================================================
def _k2_similar():
    groups = [
        ("행복하다", ["기쁘다", "즐겁다", "신나다"]),
        ("아름답다", ["예쁘다", "멋지다", "곱다"]),
        ("빠르다", ["신속하다", "빨리", "재빠르다"]),
    ]
    word, similars = random.choice(groups)
    answer = random.choice(similars)
    topic = _topic_for(2, ["비슷한말", "어휘"])
    prompt = f"'{word}'와 비슷한 말은 무엇인가요?"
    distractors = [s for g in groups for s in g[1] if s != answer]
    return _make(prompt, answer, topic, options=_choice_options(answer, random.sample(distractors, 3)))


def _k2_sentence_subject():
    subjects = ["나", "친구", "엄마", "선생님", "강아지"]
    predicates = ["책을 읽는다", "학교에 간다", "노래를 부른다", "공을 던진다"]
    s, p = random.choice(subjects), random.choice(predicates)
    answer = s
    topic = _topic_for(2, ["문장의 주어와 서술어"])
    prompt = f"'{s}가/이 {p}'에서 주어는 무엇인가요?"
    return _make(prompt, answer, topic, options=_choice_options(answer, random.sample([x for x in subjects if x != s], 3)))


def _k2_sentence_punct():
    sentences = [
        ("오늘은 날씨가 좋다", "."),
        ("지금 몇 시니", "?"),
        ("얼마나 맛있는지 몰라", "!"),
    ]
    sentence, answer = random.choice(sentences)
    topic = _topic_for(2, ["문장과 문단", "문장 부호"])
    prompt = f"'{sentence}' 끝에 올 문장 부호는?"
    return _make(prompt, answer, topic, options=_choice_options(answer, [",", ";", ":"]))


def _k2_opposite():
    pairs = [("덥다", "춥다"), ("길다", "짧다"), ("무겁다", "가볍다"), ("깨끗하다", "더럽다")]
    a, b = random.choice(pairs)
    topic = _topic_for(2, ["반대말", "어휘"])
    word, answer = random.choice([(a, b), (b, a)])
    prompt = f"'{word}'의 반대말은 무엇인가요?"
    return _make(prompt, answer, topic, options=_choice_options(answer, [a, b, word]))


# ============================================================
# 3학년: 사전, 문단 중심, 존칭/높임, 짧은 글 이해
# ============================================================
def _k3_dictionary():
    words = [
        ("행복", "기쁘고 만족스러운 상태"),
        ("노력", "어떤 목표를 위해 힘쓰는 것"),
        ("약속", "미리 정해진 일이나 언약"),
    ]
    word, meaning = random.choice(words)
    topic = _topic_for(3, ["사전 찾아보기", "어휘"])
    prompt = f"'{word}'의 뜻으로 알맞은 것은?"
    distractors = [m for _, m in random.sample(words, 2) if m != meaning]
    return _make(prompt, meaning, topic, options=_choice_options(answer=meaning, distractors=distractors + [word]))


def _k3_paragraph_main():
    passages = [
        ("민수는 매일 아침 일찍 일어나 책을 읽는다. 책을 읽으면 새로운 것을 많이 배울 수 있기 때문이다.", "민수는 매일 책을 읽는다"),
        ("우리 반은 친구들이 서로 도와준다. 어려운 일이 있을 때 함께 해결하기 때문이다.", "우리 반은 서로 돕는다"),
    ]
    passage, answer = random.choice(passages)
    topic = _topic_for(3, ["문단의 중심 생각", "독해"])
    prompt = f"다음 글의 중심 생각을 고르세요.\n{passage}"
    distractors = [a for _, a in passages if a != answer]
    return _make(prompt, answer, topic, options=_choice_options(answer, distractors))


def _k3_honorific():
    pairs = [("먹다", "드시다"), ("있다", "계시다"), ("주다", "드리다"), ("말하다", "말씀하시다")]
    plain, honorific = random.choice(pairs)
    topic = _topic_for(3, ["존칭과 높임", "문법"])
    word, answer = random.choice([(plain, honorific), (honorific, plain)])
    prompt = f"'{word}'의 반대 표현(높임/평어)은 무엇인가요?"
    return _make(prompt, answer, topic, options=_choice_options(answer, [plain, honorific, "감사하다"]))


def _k3_word_meaning():
    words = [("정성", "진심을 다함"), ("소중하다", "매우 귀여움"), ("꾸준하다", "끊임없이 계속됨")]
    word, answer = random.choice(words)
    topic = _topic_for(3, ["낱말의 뜻", "어휘"])
    prompt = f"'{word}'의 뜻은 무엇인가요?"
    distractors = [m for _, m in random.sample(words, 2) if m != answer]
    return _make(prompt, answer, topic, options=_choice_options(answer, distractors + [word]))


# ============================================================
# 4학년: 비유/직유, 사실/의견 구분, 짧은 글 요약
# ============================================================
def _k4_metaphor():
    items = [
        ("바다", "푸른 보석", "바다가 푸르고 아름답다"),
        ("달", "은접시", "달이 둥글고 반짝인다"),
        ("꽃", "미소", "꽃이 아름답게 피었다"),
    ]
    target, answer, literal = random.choice(items)
    topic = _topic_for(4, ["비유와 직유", "문학"])
    prompt = f"'{target}은 {answer}이다'는 어떤 표현인가요?"
    return _make(prompt, "비유", topic, options=_choice_options("비유", ["사실", "의견", "직설"]))


def _k4_fact_opinion():
    sentences = [
        ("오늘은 비가 온다.", "사실"),
        ("비 오는 날은 좋다.", "의견"),
        ("1학년은 3월에 개학한다.", "사실"),
    ]
    sentence, answer = random.choice(sentences)
    topic = _topic_for(4, ["사실과 의견", "독해"])
    prompt = f"'{sentence}'는 사실인가요, 의견인가요?"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["사실", "의견", "상상"]))


def _k4_summary():
    passages = [
        ("철수는 매일 운전을 한다. 처음에는 힘들었지만 꾸준히 하니 이제는 잘한다.", "철수는 꾸준히 운전 연습을 해서 잘하게 되었다."),
        ("영희는 책을 좋아한다. 도서관에 자주 가서 다양한 책을 읽는다.", "영희는 책을 좋아해서 도서관에 자주 간다."),
    ]
    passage, answer = random.choice(passages)
    topic = _topic_for(4, ["글 요약", "독해"])
    prompt = f"다음 글을 한 문장으로 요약하면?\n{passage}"
    distractors = [a for _, a in passages if a != answer]
    return _make(prompt, answer, topic, options=_choice_options(answer, distractors))


def _k4_sentence_part():
    topic = _topic_for(4, ["문장 성분", "문법"])
    prompt = "'새가 하늘을 날았다'에서 '하늘을'은 무슨 성분인가요?"
    return _make(prompt, "목적어", topic, options=_choice_options("목적어", ["주어", "서술어", "보어"]))


# ============================================================
# 5학년: 논술/의견 쓰기, 문학 요소, 속담, 미디어 자료
# ============================================================
def _k5_argument():
    topic = _topic_for(5, ["의견 쓰기", "논술"])
    prompt = "학교 급식에 채소를 더 넣어야 하는지 찬성/반대 의견과 근거를 한 문장으로 쓰세요."
    answer = "찬성한다. 채소를 먹으면 비타민을 섭취할 수 있고 건강을 지킬 수 있다."
    return _make(prompt, answer, topic, question_type="write", explanation="자신의 의견과 근거를 명확히 제시하면 됩니다.")


def _k5_literary_element():
    topic = _topic_for(5, ["문학", "문학 요소"])
    prompt = "글에서 '바람이 나무를 흔들었다'는 어떤 표현인가요?"
    answer = "의인화"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["비유", "직유", "반복"]))


def _k5_proverb():
    proverbs = [
        ("가는 말이 고와야 오는 말이 곱다", "예의 바르게 말해야 한다"),
        ("등잔 밑이 어둡다", "가까운 곳을 잘 살피지 못한다"),
        ("늦더라도 안 하느니보다 낫다", "시작하면 늦지 않다"),
    ]
    proverb, answer = random.choice(proverbs)
    topic = _topic_for(5, ["속담", "어휘"])
    prompt = f"'{proverb}'의 뜻은 무엇인가요?"
    distractors = [m for _, m in random.sample(proverbs, 2) if m != answer]
    return _make(prompt, answer, topic, options=_choice_options(answer, distractors + [proverb]))


def _k5_media():
    topic = _topic_for(5, ["미디어", "정보 활용"])
    prompt = "뉴스 기사를 볼 때 가장 먼저 확인해야 할 것은?"
    answer = "출처와 작성 날짜"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["사진의 크기", "기사의 길이", "댓글 수"]))


# ============================================================
# 6학년: 문학 비평, 비교/대조, 인물 분석, 글 고치기
# ============================================================
def _k6_character():
    topic = _topic_for(6, ["문학", "인물 분석"])
    prompt = "주인공이 어려운 상황에서도 포기하지 않은 것은 어떤 성격을 보여주나요?"
    answer = "끈기와 책임감"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["게으름과 소심함", "용기와 호기심", "집착과 이기심"]))


def _k6_compare_contrast():
    topic = _topic_for(6, ["비교와 대조", "독해"])
    prompt = "봄과 가을의 공통점과 차이점을 한 문장으로 쓰세요."
    answer = "봄과 가을 모두 온화한 계절이지만, 봄은 싹이 트고 가을은 열 맺는다."
    return _make(prompt, answer, topic, question_type="write", explanation="공통점과 차이점을 명확히 제시하면 됩니다.")


def _k6_writing_revision():
    topic = _topic_for(6, ["글 고치기", "쓰기"])
    prompt = "'친구하고 놀아서 재미었다'에서 틀린 맞춤법을 고치세요."
    answer = "재미있었다"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["재미웠다", "재미었다", "재미했었다"]))


def _k6_argument_claim():
    topic = _topic_for(6, ["논술", "주장과 근거"])
    prompt = "'학교 운영위원회에 학생 의견을 반영해야 한다'는 주장의 근거로 가장 적절한 것은?"
    answer = "학교 생활의 주체는 학생이기 때문이다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "선생님이 바쁘시기 때문이다",
        "학부모가 원하기 때문이다",
        "학교가 커지고 있기 때문이다",
    ]))


# ============================================================
# 중학년 (7~9): 기존 수준 유지
# ============================================================
def _k7_morpheme():
    topic = _topic_for(7, ["형태소", "문법"])
    prompt = "'바다'는 몇 개의 형태소로 이루어져 있나요?"
    return _make(prompt, 1, topic, options=_choice_options(1, [2, 3, 4]))


def _k7_speaker():
    topic = _topic_for(7, ["화자", "문학"])
    prompt = "시에서 '나'는 보통 무엇을 의미하나요?"
    answer = "시를 쓴 사람의 마음"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["독자", "주인공", "역사적 인물"]))


def _k7_argument_essay():
    topic = _topic_for(7, ["논술", "주장 글쓰기"])
    prompt = "'청소년에게 스마트폰 사용 시간을 제한해야 한다'는 주장에 대한 자신의 의견을 한 문장으로 쓰세요."
    answer = "찬성한다. 과도한 스마트폰 사용은 수면과 학업에 부정적인 영향을 미칠 수 있다."
    return _make(prompt, answer, topic, question_type="write")


def _k8_novel_element():
    topic = _topic_for(8, ["소설", "문학 요소"])
    prompt = "소설에서 사건이 전개되는 곳을 무엇이라 하나요?"
    answer = "배경"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["주제", "서사", "인물"]))


def _k8_voice():
    topic = _topic_for(8, ["문체", "문학"])
    prompt = "작품에 작가의 감정과 태도가 드러나는 말투를 무엇이라 하나요?"
    answer = "어조"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["리듬", "운율", "구절"]))


def _k8_debate():
    topic = _topic_for(8, ["토론", "의사소통"])
    prompt = "상대방 의견을 반박할 때 가장 중요한 것은?"
    answer = "근거를 제시하는 것"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["목소리를 높이는 것", "말을 빨리 하는 것", "감정적으로 호소하는 것"]))


def _k9_literary_value():
    topic = _topic_for(9, ["문학", "문학의 가치"])
    prompt = "고전 문학을 읽는 가장 큰 의미는 무엇인가요?"
    answer = "우리 문화와 정서를 이해할 수 있다"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["시험에 잘 볼 수 있다", "외국어를 배울 수 있다", "신조어를 많이 알 수 있다"]))


def _k9_phonological_change():
    topic = _topic_for(9, ["음운", "국어의 특성"])
    prompt = "'불+빛'이 '불빛'으로 발음되는 현상은?"
    answer = "음운 규칙"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["어원", "사전적 의미", "방언"]))


def _k9_argument_claim():
    topic = _topic_for(9, ["논술", "논증"])
    prompt = "'민주주의 사회에서 표현의 자유는 제한되어야 한다'는 주장에 대해 찬반 의견과 근거를 한 문장으로 쓰세요."
    answer = "반대한다. 표현의 자유는 민주주의의 핵심 가치이지만 타인의 권리를 침해해서는 안 된다."
    return _make(prompt, answer, topic, question_type="write")


SOLUTION_BANKS = {
    1: [
        ("'가족'에 대해 한 문장으로 느낌을 써 보세요.", "가족은 서로 사랑하고 돕는 사람들이다.", "자유 표현"),
    ],
    2: [
        ("친구에게 책을 빌려 달라고 부탁하는 문장을 써 보세요.", "친구야, 내일까지 이 책 좀 빌려 줄 수 있어?", "바른 표현"),
    ],
    3: [
        ("'독서'의 좋은 점을 두 가지 이상 써 보세요.", "독서는 지식을 넓히고 상상력을 키워 준다.", "설명 쓰기"),
    ],
    4: [
        ("'노력'의 의미를 예를 들어 설명해 보세요.", "노력은 목표를 위해 힘쓰는 것이다. 매일 연습해서 피아노를 잘 치게 된 것이 노력의 예이다.", "개념 설명"),
    ],
    5: [
        ("'독서는 마음의 양식이다.'라는 말의 뜻을 써 보세요.", "책을 읽으면 마음이 풍요로워지고 올바른 가치관을 갖게 된다.", "속담 이해"),
    ],
    6: [
        ("'환경 보호'를 위해 우리가 실천할 수 있는 일 두 가지를 써 보세요.", "분리배출을 하고, 사용하지 않는 전기를 끈다.", "의견 쓰기"),
    ],
    7: [
        ("'공부'가 중요한 이유를 두 가지 이상 써 보세요.", "공부는 지식을 쌓고 미래에 필요한 능력을 기르는 데 도움이 된다.", "의견 쓰기"),
    ],
    8: [
        ("'스마트폰 사용'에 대한 찬성/반대 의견과 근거를 써 보세요.", "적절히 사용하면 정보 검색과 소통에 도움이 되지만, 과하면 학업에 방해가 된다.", "논술"),
    ],
    9: [
        ("'인권'의 의미와 중요성을 써 보세요.", "인권은 사람으로서 누구나 갖는 기본 권리이다. 인권을 존중해야 평화로운 사회를 만들 수 있다.", "논술"),
    ],
}



def _k1_rhyme():
    items = [("바", "나", "ㅏ"), ("고", "토", "ㅗ"), ("우", "주", "ㅜ")]
    a, b, vowel = random.choice(items)
    topic = _topic_for(1, ["글자 익히기", "모음"])
    prompt = f"'{a}'와 '{b}'에 같은 모음이 들어 있나요?"
    answer = "예"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["아니오", "모름"]))


def _k1_picture_word():
    words = [("사과", "과일"), ("고양이", "동물"), ("책", "물건"), ("태양", "하늘")]
    word, category = random.choice(words)
    topic = _topic_for(1, ["낱말 익히기", "어휘"])
    prompt = f"'{word}'는 어떤 그룹에 속하나요?"
    distractors = [c for _, c in random.sample(words, 3) if c != category]
    return _make(prompt, category, topic, options=_choice_options(category, distractors), explanation=f"'{word}'는 {category}에 속합니다.")


def _k2_word_order():
    topic = _topic_for(2, ["문장의 순서", "글쓰기"])
    prompt = "다음 문장을 바른 순서로 배열하면?\\n① 책을 읽는다 ② 도서관에 간다 ③ 책을 고른다"
    answer = "② → ③ → ①"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "① → ② → ③",
        "③ → ② → ①",
        "② → ① → ③",
    ]))


def _k2_spelling():
    topic = _topic_for(2, ["맞춤법", "글쓰기"])
    prompt = "다음 중 맞춤법이 올바른 문장은?"
    answer = "친구와 함께 학교에 갔다."
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "친구와 함께 학교에 갓다.",
        "친구와 함께 학교에 갔따.",
        "친구와 함께 학교에 갓따.",
    ]))


def _k3_idiom():
    idioms = [
        ("발이 넓다", "아는 사람이 많다"),
        ("귀가 밝다", "소리를 잘 듣는다"),
        ("손이 크다", "쓰는 것이 크다"),
    ]
    idiom, answer = random.choice(idioms)
    topic = _topic_for(3, ["관용 표현", "어휘"])
    prompt = f"'{idiom}'의 뜻은 무엇인가요?"
    distractors = [m for _, m in random.sample(idioms, 2) if m != answer]
    return _make(prompt, answer, topic, options=_choice_options(answer, distractors + [idiom]))


def _k3_sentence_part():
    topic = _topic_for(3, ["문장 성분", "문법"])
    prompt = "'민수가 공을 던진다'에서 '공을'은 무슨 성분인가요?"
    answer = "목적어"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["주어", "서술어", "보어"]))


def _k4_cause_effect():
    topic = _topic_for(4, ["인과 관계", "독해"])
    prompt = "'비가 많이 왔다. 길이 미끄러웠다.'에서 '비가 많이 왔다'는 무엇인가요?"
    answer = "원인"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["결과", "방법", "의견"]))


def _k4_paragraph_topic():
    topic = _topic_for(4, ["문단의 주제", "독해"])
    prompt = "다음 글의 주제로 알맞은 것은?\n우리 학교에는 다양한 동아리가 있다. 합창부, 축구부, 과학부 등 많은 학생들이 자신의 재능을 키우고 있다."
    answer = "학교 동아리 활동"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "학교 급식",
        "체육 대회",
        "방과 후 수업",
    ]))


def _k5_outline():
    topic = _topic_for(5, ["글의 구조", "쓰기"])
    prompt = "글을 쓸 때 본론 다음에 오는 부분은?"
    answer = "결론"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["도입", "서론", "줄거리"]))


def _k5_debate():
    topic = _topic_for(5, ["토론", "의사소통"])
    prompt = "상대방 의견에 반대할 때 가장 먼저 해야 할 것은?"
    answer = "상대 의견을 정확히 파악한다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "목소리를 높인다",
        "상대를 비난한다",
        "자신만의 예시를 든다",
    ]))


def _k6_emotion():
    topic = _topic_for(6, ["인물의 감정", "문학"])
    prompt = "주인공이 떨리는 손으로 편지를 열었다. 이때 주인공의 감정으로 가장 알맞은 것은?"
    answer = "기대와 설렘"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "분노와 후회",
        "지루함과 싫증",
        "피곤함과 졸음",
    ]))


def _k6_topic_sentence():
    topic = _topic_for(6, ["주제문", "독해"])
    prompt = "다음 문단에서 주제문을 고르세요.\n(1) 우리 반은 환경 보호를 실천하고 있다. (2) 분리배출을 꼼꼼히 하고 종이를 아껴 쓴다. (3) 또한 텃밭에서 채소를 기른다."
    answer = "(1)"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["(2)", "(3)", "(1)과 (2)"]))


def _k5_poem_element():
    topic = _topic_for(5, ["시", "문학"])
    prompt = "시에서 '꽃이 웃는다'와 같이 사람처럼 표현하는 방법은?"
    answer = "의인화"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["비유", "의인화", "반복", "대조"]))


def _k5_news_title():
    topic = _topic_for(5, ["미디어", "정보"])
    prompt = "뉴스 기사 제목을 지을 때 가장 중요한 것은?"
    answer = "기사의 핵심 내용을 짧게 전달한다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "재미있는 농담을 넣는다",
        "기사의 핵심 내용을 짧게 전달한다",
        "독자의 실수를 지적한다",
        "길고 어려운 단어를 많이 쓴다",
    ]))


def _k5_sentence_connect():
    topic = _topic_for(5, ["글쓰기", "문장"])
    prompt = "문단에서 문장과 문장을 자연스럽게 이어 주는 것은?"
    answer = "접속어"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["주어", "접속어", "맞춤법", "띄어쓰기"]))


def _k5_audience():
    topic = _topic_for(5, ["글쓰기", "독자"])
    prompt = "글을 쓸 때 누구에게 쓰는지 미리 정하는 것은?"
    answer = "독자 설정"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["주제 선정", "독자 설정", "자료 조사", "퇴고"]))


def _k6_theme():
    topic = _topic_for(6, ["문학", "주제"])
    prompt = "글쓴이가 작품을 통해 전하고 싶은 메시지를 무엇이라 하나요?"
    answer = "주제"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["배경", "주제", "인물", "사건"]))


def _k6_evidence():
    topic = _topic_for(6, ["논술", "근거"])
    prompt = "주장을 뒷받침하기 위해 드는 구체적인 사례는?"
    answer = "근거"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["의견", "근거", "반론", "결론"]))


def _k6_purpose():
    topic = _topic_for(6, ["독해", "글의 목적"])
    prompt = "광고 글의 주된 목적은 무엇인가요?"
    answer = "상품이나 서비스를 알리고 권유한다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "독자의 비밀을 알린다",
        "상품이나 서비스를 알리고 권유한다",
        "역사적 사실만 전달한다",
        "시를 감상하게 한다",
    ]))


def _k6_revision2():
    topic = _topic_for(6, ["글 고치기", "쓰기"])
    prompt = "'오늘은 정말 재미없는 날이다'보다 구체적으로 쓴 문장은?"
    answer = "오늘은 친구들과 놀이공원에 가서 신나게 놀았다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "오늘은 매우 지루했다",
        "오늘은 친구들과 놀이공원에 가서 신나게 놀았다",
        "오늘은 별일 없었다",
        "오늘은 정말 재미없는 날이다",
    ]))


def _k7_metaphor():
    topic = _topic_for(7, ["문학", "비유"])
    prompt = "'세상은 물결과 같다'에서 '물결'은 무엇을 나타낼까요?"
    answer = "변화하는 세상"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "실제 바다",
        "변화하는 세상",
        "작가의 고향",
        "친구와의 우정",
    ]))


def _k7_text_type():
    topic = _topic_for(7, ["문법", "문장"])
    prompt = "상대에게 부탁하거나 제안할 때 쓰는 문장은?"
    answer = "청유문"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["평서문", "의문문", "청유문", "감탄문"]))


def _k7_classical():
    topic = _topic_for(7, ["고전", "문학"])
    prompt = "고전 소설에서 주인공이 어려움을 극복하는 이야기를 통해 전하는 바람직한 삶은?"
    answer = "정의와 인정"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["정의와 인정", "부와 명예", "힘과 권력", "복수와 원망"]))


def _k7_media_bias():
    topic = _topic_for(7, ["미디어", "정보"])
    prompt = "신문 기사를 읽을 때 객관성을 판단하는 기준은?"
    answer = "사실과 의견이 구분되어 있는지"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "사실과 의견이 구분되어 있는지",
        "사진이 많은지",
        "기자의 이름이 있는지",
        "기사가 짧은지",
    ]))


def _k8_modern_novel():
    topic = _topic_for(8, ["소설", "문학"])
    prompt = "근대 소설에서 자주 나타나는 주제는?"
    answer = "개인의 삶과 사회 문제"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "신화적 영웅의 모험",
        "개인의 삶과 사회 문제",
        "외계 생물의 이야기",
        "역사적 전쟁의 승패",
    ]))


def _k8_text_structure():
    topic = _topic_for(8, ["글쓰기", "구조"])
    prompt = "논설문에서 자신의 주장을 뒷받침하는 부분은?"
    answer = "본론"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["도입", "본론", "결론", "서론"]))


def _k8_hangul_history():
    topic = _topic_for(8, ["국어", "역사"])
    prompt = "훈민정음이 창제된 시기는?"
    answer = "조선 세종대"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["고조선", "삼국 시대", "조선 세종대", "근대"]))


def _k8_debate_ethics():
    topic = _topic_for(8, ["토론", "의사소통"])
    prompt = "토론에서 상대방의 인격이 아닌 의견을 반박해야 하는 이유는?"
    answer = "건설적인 토론을 위해서이다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "상대를 화나게 하기 위해서이다",
        "건설적인 토론을 위해서이다",
        "자신만의 의견을 강요하기 위해서이다",
        "토론을 빨리 끝내기 위해서이다",
    ]))


def _k9_modern_poetry():
    topic = _topic_for(9, ["현대시", "문학"])
    prompt = "현대 시에서 '비'가 자주 상징하는 것은?"
    answer = "슬픔이나 정화"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "농사의 풍년",
        "슬픔이나 정화",
        "전쟁의 시작",
        "여행의 즐거움",
    ]))


def _k9_criticism():
    topic = _topic_for(9, ["비평", "문학"])
    prompt = "작품 비평에서 가장 중요한 것은?"
    answer = "작품의 내용과 형식을 근거로 평가한다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "작가의 사생활을 논한다",
        "작품의 내용과 형식을 근거로 평가한다",
        "개인의 취향만 말한다",
        "줄거리를 길게 요약한다",
    ]))


def _k9_speech():
    topic = _topic_for(9, ["화법", "국어"])
    prompt = "듣는 사람의 마음을 헤아려 공손하게 말하는 화법은?"
    answer = "경어체"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["해체", "경어체", "비격식체", "방언"]))


def _k9_media_literacy():
    topic = _topic_for(9, ["미디어", "정보"])
    prompt = "SNS 정보를 공유하기 전에 가장 먼저 확인해야 할 것은?"
    answer = "정보의 출처와 사실 여부"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "정보의 출처와 사실 여부",
        "좋아요 수",
        "친구들의 반응",
        "업로드 시간",
    ]))


def _k7_summary():
    topic = _topic_for(7, ["독해", "요약"])
    prompt = "다음 글의 중심 내용을 고르세요.\n책을 읽으면 다양한 세계를 경험할 수 있다. 독서는 지식을 넓히고 공감 능력을 키워 준다."
    answer = "독서는 지식과 공감 능력을 키워 준다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "책은 비싸다",
        "독서는 지식과 공감 능력을 키워 준다",
        "모든 책을 읽어야 한다",
        "독서는 재미없는 활동이다",
    ]))


def _k7_word_class():
    topic = _topic_for(7, ["문법", "품사"])
    prompt = "'빠르게'의 품사는?"
    answer = "부사"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["형용사", "부사", "명사", "동사"]))


def _k7_sentence_type():
    topic = _topic_for(7, ["문법", "문장"])
    prompt = "'오늘 날씨가 참 좋구나!'는 어떤 문장인가요?"
    answer = "감탄문"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["의문문", "감탄문", "명령문", "청유문"]))


def _k8_character2():
    topic = _topic_for(8, ["소설", "인물"])
    prompt = "소설 인물의 말과 행동을 통해 알 수 있는 것은?"
    answer = "인물의 성격과 심리"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "저자의 출신지",
        "인물의 성격과 심리",
        "책의 판매 부수",
        "인쇄한 날짜",
    ]))


def _k8_novel_setting():
    topic = _topic_for(8, ["소설", "문학 요소"])
    prompt = "소설에서 인물이 살아가는 시대와 장소를 무엇이라 하나요?"
    answer = "배경"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["주제", "배경", "서사", "화자"]))


def _k8_argument_type():
    topic = _topic_for(8, ["논술", "주장"])
    prompt = "상대방의 주장을 부정하는 글을 무엇이라 하나요?"
    answer = "반론문"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["설명문", "반론문", "서신문", "보고문"]))


def _k9_modern_poet():
    topic = _topic_for(9, ["현대시", "문학"])
    prompt = "현대 시에서 작가의 감정을 압축하여 나타내는 것은?"
    answer = "심상"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["리듬", "심상", "운율", "구절"]))


def _k9_grammar():
    topic = _topic_for(9, ["문법", "국어"])
    prompt = "'책을 읽는 학생'에서 '읽는'의 문법적 기능은?"
    answer = "관형어"
    return _make(prompt, answer, topic, options=_choice_options(answer, ["주어", "관형어", "부사어", "서술어"]))


def _k9_classic_value():
    topic = _topic_for(9, ["고전", "문학"])
    prompt = "고전 문학을 읽는 가장 큰 의미는?"
    answer = "우리의 전통과 정서를 이해할 수 있다"
    return _make(prompt, answer, topic, options=_choice_options(answer, [
        "시험 문제를 맞힐 수 있다",
        "우리의 전통과 정서를 이해할 수 있다",
        "최신 유행어를 배울 수 있다",
        "외국어 실력을 키울 수 있다",
    ]))

GENERATORS = {
    1: [_k1_consonant_vowel, _k1_word_reading, _k1_opposite, _k1_sentence_punct, _k1_rhyme, _k1_picture_word],
    2: [_k2_similar, _k2_sentence_subject, _k2_sentence_punct, _k2_opposite, _k2_word_order, _k2_spelling],
    3: [_k3_dictionary, _k3_paragraph_main, _k3_honorific, _k3_word_meaning, _k3_idiom, _k3_sentence_part],
    4: [_k4_metaphor, _k4_fact_opinion, _k4_summary, _k4_sentence_part, _k4_cause_effect, _k4_paragraph_topic],
    5: [_k5_argument, _k5_literary_element, _k5_proverb, _k5_media, _k5_outline, _k5_debate, _k5_poem_element, _k5_news_title, _k5_sentence_connect, _k5_audience],
    6: [_k6_character, _k6_compare_contrast, _k6_writing_revision, _k6_argument_claim, _k6_emotion, _k6_topic_sentence, _k6_theme, _k6_evidence, _k6_purpose, _k6_revision2],
    7: [_k7_morpheme, _k7_speaker, _k7_argument_essay, _k7_metaphor, _k7_text_type, _k7_classical, _k7_media_bias, _k7_summary, _k7_word_class, _k7_sentence_type],
    8: [_k8_novel_element, _k8_voice, _k8_debate, _k8_modern_novel, _k8_text_structure, _k8_hangul_history, _k8_debate_ethics, _k8_character2, _k8_novel_setting, _k8_argument_type],
    9: [_k9_literary_value, _k9_phonological_change, _k9_argument_claim, _k9_modern_poetry, _k9_criticism, _k9_speech, _k9_media_literacy, _k9_modern_poet, _k9_grammar, _k9_classic_value],
}


def _transform_question(prompt, answer, options, topic):
    if options:
        question_type = random.choice(["choice", "choice", "write"])
        if question_type == "write":
            return _make(f"{prompt} (정답을 직접 쓰세요)", answer, topic, question_type="write")
        return _make(prompt, answer, topic, options=options)
    question_type = random.choice(["write", "solution"])
    if question_type == "solution":
        return _make(prompt, answer, topic, question_type="solution", explanation=f"정답 예시: {answer}", max_points=15)
    return _make(prompt, answer, topic)


def generate_korean_set(grade, count=10):
    generators = GENERATORS.get(grade, GENERATORS[9])
    selected = []
    seen = set()
    attempts = 0
    target = count - min(2, len(SOLUTION_BANKS.get(grade, SOLUTION_BANKS[9])))
    while len(selected) < target and attempts < count * 50:
        g = random.choice(generators)
        q = g()
        # 같은 문항(프롬프트+유형)이 중복되어 출제되지 않도록 관리합니다.
        key = (q["prompt"], q.get("question_type", "choice"))
        if key not in seen:
            seen.add(key)
            selected.append((q["prompt"], q["answer"], q.get("options", []), q["topic"]))
        attempts += 1
    # 유일한 문항이 부족하면 기존 문항을 허용하며 채웁니다.
    while len(selected) < target:
        g = random.choice(generators)
        q = g()
        selected.append((q["prompt"], q["answer"], q.get("options", []), q["topic"]))
    solution_bank = SOLUTION_BANKS.get(grade, SOLUTION_BANKS[9])
    solution_count = min(2, len(solution_bank), count - len(selected))
    selected += [(prompt, answer, [], topic) for prompt, answer, topic in random.sample(solution_bank, solution_count)]
    random.shuffle(selected)
    selected = selected[:count]
    questions = []
    for prompt, answer, options, topic in selected:
        questions.append(_transform_question(prompt, answer, options, topic))
    return questions


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
