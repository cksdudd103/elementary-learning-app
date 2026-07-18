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
    return random.choice(_curriculum_topics("korean", grade, fallback))


def _make(prompt, answer, topic, options=None, question_type=None, explanation=None, max_points=10):
    return {
        "prompt": prompt,
        "answer": str(answer),
        "topic": topic,
        "explanation": explanation or f"정답은 '{answer}'입니다.",
        "question_type": question_type or ("choice" if options else "write"),
        "options": options or [],
        "image_url": None,
        "max_points": max_points,
    }


# ───────────────────────────────
# 1~2학년: 기초 문자·어휘·문장
# ───────────────────────────────

def _k1_consonant_vowel():
    topic = _topic_for(1, ["한글 자모", "낱말 읽기"])
    if random.choice([True, False]):
        prompt = "다음 중 자음은 무엇인가요?"
        answer = random.choice(["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"])
        distractors = random.sample(["ㅏ", "ㅑ", "ㅓ", "ㅕ", "ㅗ", "ㅛ", "ㅜ", "ㅠ", "ㅡ", "ㅣ"], 3)
    else:
        prompt = "다음 중 모음은 무엇인가요?"
        answer = random.choice(["ㅏ", "ㅑ", "ㅓ", "ㅕ", "ㅗ", "ㅛ", "ㅜ", "ㅠ", "ㅡ", "ㅣ"])
        distractors = random.sample(["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", "ㅇ", "ㅈ", "ㅊ"], 3)
    return _make(prompt, answer, topic, options=[answer] + distractors)


def _k1_word_reading():
    words = [("나무", "나무", "식물"), ("바다", "바다", "자연"), ("학교", "학교", "장소"), ("친구", "친구", "사람"), ("가방", "가방", "물건"), ("구름", "구름", "자연")]
    word, answer, hint = random.choice(words)
    topic = _topic_for(1, ["낱말 읽기"])
    prompt = f"'{word}'의 뜻은 무엇인가요?"
    distractors = [w for w, _, _ in random.sample(words, 3) if w != word]
    return _make(prompt, answer, topic, options=[answer] + distractors, explanation=f"'{word}'는 {answer}를 뜻합니다.")


def _k1_opposite():
    pairs = [("크다", "작다"), ("높다", "낮다"), ("많다", "적다"), ("빠르다", "느리다"), ("밝다", "어둡다"), ("따뜻하다", "차갑다")]
    a, b = random.choice(pairs)
    topic = _topic_for(1, ["반대말"])
    answer = b
    prompt = f"'{a}'의 반대말은?"
    return _make(prompt, answer, topic, options=[b, a, random.choice([p[0] for p in pairs if p[0] != a]), random.choice([p[1] for p in pairs if p[1] != b])])


def _k1_sentence_punct():
    topic = _topic_for(1, ["문장 부호"])
    q = random.choice([
        ("이름이 무엇인가요", "?"),
        ("와 정말 멋지다", "!"),
        ("나는 학교에 간다", "."),
        ("얼마예요", "?"),
    ])
    prompt = f"'{q[0]}'에 알맞은 문장 부호는?"
    answer = q[1]
    return _make(prompt, answer, topic, options=[".", ",", "?", "!"])


def _k2_similar():
    pairs = [("기쁘다", "즐겁다"), ("맛있다", "달다"), ("예쁘다", "아름답다"), ("배고프다", "출출하다"), ("피곤하다", "지치다")]
    a, b = random.choice(pairs)
    topic = _topic_for(2, ["비슷한 말"])
    answer = b
    prompt = f"'{a}'와 뜻이 비슷한 말은?"
    return _make(prompt, answer, topic, options=[b, random.choice([p[1] for p in pairs if p[0] != a]), "무섭다", "화나다"])


def _k2_sentence_subject():
    sentences = [
        ("강아지가 공을 가지고 논다.", "강아지"),
        ("새가 하늘을 난다.", "새"),
        ("어머니가 밥을 하신다.", "어머니"),
        ("친구들이 울상에서 뛴다.", "친구들"),
    ]
    sent, answer = random.choice(sentences)
    topic = _topic_for(2, ["문장 이해"])
    prompt = f"'{sent}'에서 행동을 하는 대상은?"
    return _make(prompt, answer, topic)


# ───────────────────────────────
# 3~4학년: 국어사전·문단·비유·요약
# ───────────────────────────────

def _k3_dictionary():
    topic = _topic_for(3, ["국어사전", "어휘"])
    words = ["가방", "가위", "가을", "강아지", "공부", "귤", "나라", "다리", "딸기", "마을"]
    idx = random.randint(0, len(words) - 2)
    a, b = words[idx], words[idx + 1]
    prompt = f"국어사전에서 '{a}'와 '{b}' 중 먼저 나오는 낱말은?"
    answer = a if a < b else b
    return _make(prompt, answer, topic, options=[a, b, random.choice(words), random.choice(words)])


def _k3_paragraph_main():
    topic = _topic_for(3, ["문단", "중심 문장"])
    paragraphs = [
        ("독서는 우리에게 많은 지식을 줍니다. 책을 읽으면 새로운 세계를 만날 수 있고, 상상력도 커집니다.", "독서는 우리에게 많은 지식을 줍니다."),
        ("욕심이 과하면 큰 화를 입을 수 있습니다. 적당히 가지려는 마음이 중요합니다.", "욕심이 과하면 큰 화를 입을 수 있습니다."),
        ("친구와 사이좋게 지내는 방법은 서로를 이해하는 것입니다. 다투더라도 대화로 풀어야 합니다.", "친구와 사이좋게 지내는 방법은 서로를 이해하는 것입니다."),
    ]
    p, answer = random.choice(paragraphs)
    prompt = f"다음 문단의 중심 문장을 고르세요.\n\n{p}"
    distractors = [a for _, a in random.sample(paragraphs, 3) if a != answer]
    return _make(prompt, answer, topic, options=[answer] + distractors, explanation="문단의 가장 중요한 내용을 담은 문장이 중심 문장입니다.")


def _k3_honorific():
    topic = _topic_for(3, ["높임 표현"])
    pairs = [
        ("할머니가 잔다.", "할머니께서 주무십니다."),
        ("아버지가 먹는다.", "아버지께서 드십니다."),
        ("선생님이 간다.", "선생님께서 가십니다."),
    ]
    wrong, answer = random.choice(pairs)
    prompt = f"다음 문장을 높임말로 바르게 고친 것은?\n'{wrong}'"
    distractors = [a for _, a in random.sample(pairs, 3) if a != answer]
    return _make(prompt, answer, topic, options=[answer] + distractors)


def _k4_metaphor():
    topic = _topic_for(4, ["비유적 표현", "비유"])
    examples = [
        ("얼굴이 사과처럼 빨갛다.", "비유"),
        ("바람이 노래한다.", "의인법"),
        ("시간은 화살처럼 빠르다.", "직유법"),
        ("하늘이 우는 것 같았다.", "의인법"),
    ]
    sent, answer = random.choice(examples)
    prompt = f"'{sent}'에 쓰인 표현법은?"
    return _make(prompt, answer, topic, options=["비유", "의인법", "직유법", "반어법"])


def _k4_fact_opinion():
    topic = _topic_for(4, ["사실과 의견"])
    sentences = [
        ("우리나라의 수도는 서울이다.", "사실"),
        ("겨울은 너무 추워서 싫다.", "의견"),
        ("지구는 태양 주위를 돈다.", "사실"),
        ("이 영화가 가장 재미있다.", "의견"),
    ]
    sent, answer = random.choice(sentences)
    prompt = f"'{sent}'는 사실인가요, 의견인가요?"
    return _make(prompt, answer, topic, options=["사실", "의견"])


def _k4_summary():
    topic = _topic_for(4, ["요약"])
    texts = [
        ("민준이는 매일 아침 일찍 일어나 학교에 간다. 학교에서 친구들과 함께 공부하고 점심을 먹은 뒤 집에 돌아온다.", "민준이의 하루 일과"),
        ("비가 많이 와서 산길은 미끄러웠다. 등산객들은 조심스럽게 발걸음을 옮겼다.", "비로 인해 산길이 미끄러웠던 상황"),
    ]
    text, answer = random.choice(texts)
    prompt = f"다음 내용을 가장 잘 요약한 것은?\n\n{text}"
    distractors = [a for _, a in texts if a != answer]
    if len(distractors) > 3:
        distractors = random.sample(distractors, 3)
    return _make(prompt, answer, topic, options=[answer] + distractors)


# ───────────────────────────────
# 5~6학년: 논설문·문학·매체·속담
# ───────────────────────────────

def _k5_argument():
    topic = _topic_for(5, ["논설문", "주장과 근거"])
    arguments = [
        ("학교 급식에 채소를 더 넣어야 한다.", "채소를 먹으면 비타민을 섭취할 수 있고 건강을 지킬 수 있다."),
        ("도서관 이용 시간을 늘려야 한다.", "학생들이 더 많이 독서할 수 있어 지식과 상상력이 커진다."),
        ("분리배출을 꼭 해야 한다.", "환경을 보호하고 자원을 재활용할 수 있다."),
    ]
    claim, answer = random.choice(arguments)
    prompt = f"'{claim}'라는 주장을 뒷받침하는 근거로 알맞은 것은?"
    distractors = [a for _, a in random.sample(arguments, 3) if a != answer]
    return _make(prompt, answer, topic, options=[answer] + distractors)


def _k5_literary_element():
    topic = _topic_for(5, ["문학", "이야기"])
    prompt = "문학 작품에서 사건이 벌어지는 시간과 장소를 무엇이라 하나요?"
    answer = "배경"
    return _make(prompt, answer, topic, options=["배경", "인물", "줄거리", "주제"])


def _k5_media():
    topic = _topic_for(5, ["매체", "비판적 읽기"])
    prompt = "광고를 비판적으로 볼 때 가장 먼저 살펴야 할 것은?"
    answer = "과장되거나 숨긴 정보"
    return _make(prompt, answer, topic, options=["과장되거나 숨긴 정보", "광고 길이", "배경 음악", "출연자 옷"])


def _k5_proverb():
    proverbs = [
        ("가는 말이 고와야 오는 말이 곱다.", "상대에게 한 말은 되돌아온다."),
        ("등잔 밑이 어둡다.", "가까운 곳에 오히려 못 본다."),
        ("소 잃고 외양간 고친다.", "일이 난 뒤에 대비한다."),
    ]
    p, answer = random.choice(proverbs)
    topic = _topic_for(5, ["속담"])
    prompt = f"'{p}'의 뜻으로 알맞은 것은?"
    distractors = [a for _, a in random.sample(proverbs, 3) if a != answer]
    return _make(prompt, answer, topic, options=[answer] + distractors)


def _k6_writing_revision():
    topic = _topic_for(6, ["글쓰기", "퇴고"])
    prompt = "글의 내용과 표현을 고쳐 쓰는 과정을 무엇이라 하나요?"
    answer = "퇴고"
    return _make(prompt, answer, topic, options=["퇴고", "발췌", "요약", "논술"])


def _k6_compare_contrast():
    topic = _topic_for(6, ["설명 방법"])
    prompt = "두 대상의 공통점과 차이점을 밝히는 설명 방법은?"
    answer = "비교와 대조"
    return _make(prompt, answer, topic, options=["비교와 대조", "예시", "정의", "분류"])


def _k6_character():
    topic = _topic_for(6, ["문학", "인물 이해"])
    prompt = "작품 속 인물의 말과 행동으로 알 수 있는 것은?"
    answer = "성격"
    return _make(prompt, answer, topic, options=["성격", "배경", "줄거리", "주제"])


# ───────────────────────────────
# 중학년: 문법·문학·논증·매체
# ───────────────────────────────

def _k7_morpheme():
    topic = _topic_for(7, ["문법", "형태소"])
    prompt = "단어의 짜임에서 실질적인 의미를 가진 가장 작은 단위는?"
    answer = "형태소"
    return _make(prompt, answer, topic, options=["형태소", "음절", "문장", "품사"])


def _k7_speaker():
    topic = _topic_for(7, ["문학"])
    prompt = "문학 작품에서 말하는 이를 무엇이라 하나요?"
    answer = "화자"
    return _make(prompt, answer, topic, options=["화자", "독자", "작가", "인물"])


def _k7_argument_essay():
    topic = _topic_for(7, ["논설문"])
    prompt = "주장과 근거를 중심으로 상대를 설득하는 글은?"
    answer = "논설문"
    return _make(prompt, answer, topic, options=["논설문", "설명문", "수필", "일기"])


def _k8_novel_element():
    topic = _topic_for(8, ["소설"])
    prompt = "소설의 구성 요소가 아닌 것은?"
    answer = "운율"
    return _make(prompt, answer, topic, options=["인물", "사건", "배경", "운율"])


def _k8_voice():
    topic = _topic_for(8, ["문법"])
    prompt = "문장의 주체가 스스로 행동하는 표현은?"
    answer = "능동 표현"
    return _make(prompt, answer, topic, options=["능동 표현", "수동 표현", "피동 표현", "사동 표현"])


def _k8_debate():
    topic = _topic_for(8, ["토론"])
    prompt = "상대의 주장을 인정하면서 다른 의견을 제시하는 것은?"
    answer = "반론"
    return _make(prompt, answer, topic, options=["반론", "입론", "결론", "요약"])


def _k9_literary_value():
    topic = _topic_for(9, ["문학"])
    prompt = "문학 작품이 독자에게 주는 아름다움과 감동의 성질은?"
    answer = "문학성"
    return _make(prompt, answer, topic, options=["문학성", "논리성", "사실성", "객관성"])


def _k9_phonological_change():
    topic = _topic_for(9, ["음운"])
    prompt = "같은 음운 환경에서 소리가 달라지는 현상은?"
    answer = "음운 변동"
    return _make(prompt, answer, topic, options=["음운 변동", "음운 규칙", "형태 변화", "어휘 변화"])


def _k9_argument_claim():
    topic = _topic_for(9, ["논증"])
    prompt = "글쓴이가 문제에 대해 내세우는 핵심 생각은?"
    answer = "주장"
    return _make(prompt, answer, topic, options=["주장", "근거", "예시", "반론"])


# ───────────────────────────────
# 풀이형 문제
# ───────────────────────────────

SOLUTION_BANKS = {
    1: [
        ("'바다', '하늘', '산' 중 가장 넓어 보이는 것은 무엇일까요? 이유를 한 문장으로 써 보세요.", "하늘이 가장 넓다. 땅 위 모든 것을 덮기 때문이다.", "관찰과 표현"),
        ("'봄'에 대해 한 문장으로 느낌을 써 보세요.", "봄에는 따뜻한 바람이 불고 꽃이 핀다.", "계절 표현"),
    ],
    2: [
        ("친구에게 책을 빌려 달라고 부탁하는 문장을 써 보세요.", "친구야, 내일까지 이 책 좀 빌려 줄 수 있어?", "바른 표현"),
        ("'우리 반'을 한 문장으로 소개해 보세요.", "우리 반은 친구들이 서로 도와주는 따뜻한 반이에요.", "문장 쓰기"),
    ],
    3: [
        ("'독서'의 좋은 점을 두 가지 이상 써 보세요.", "독서는 지식을 넓히고 상상력을 키워 준다.", "설명 쓰기"),
        ("'친구와 싸웠을 때' 화해할 수 있는 방법을 써 보세요.", "먼저 사과하고 서로의 마음을 이야기하면서 화해한다.", "의견 쓰기"),
    ],
    4: [
        ("'노력'의 의미를 예를 들어 설명해 보세요.", "노력은 목표를 위해 힘쓰는 것이다. 매일 연습해서 피아노를 잘 치게 된 것이 노력의 예이다.", "개념 설명"),
        ("길을 가다가 돈을 주웠다면 어떻게 할 것인지 이유와 함께 써 보세요.", "경찰서에 맡길 것이다. 주인이 찾을 수 있도록 돕는 것이 옳기 때문이다.", "의견 쓰기"),
    ],
    5: [
        ("'독서는 마음의 양식이다.'라는 말의 뜻을 써 보세요.", "책을 읽으면 마음이 풍요로워지고 올바른 가치관을 갖게 된다.", "속담 이해"),
        ("학교 급식에 채소를 더 넣어야 하는지 찬성/반대 의견과 근거를 써 보세요.", "찬성한다. 채소를 먹으면 비타민을 섭취할 수 있고 건강을 지킬 수 있다.", "의견 쓰기"),
    ],
    6: [
        ("'환경 보호'를 위해 우리가 실천할 수 있는 일 두 가지를 써 보세요.", "분리배출을 하고, 사용하지 않는 전기를 끈다.", "의견 쓰기"),
        ("'친구'의 의미를 예를 들어 설명해 보세요.", "친구는 어려울 때 서로 돕고 기쁠 때 함께 웃는 사람이다.", "개념 설명"),
    ],
    7: [
        ("'공부'가 중요한 이유를 두 가지 이상 써 보세요.", "공부는 지식을 쌓고 미래에 필요한 능력을 기르는 데 도움이 된다.", "의견 쓰기"),
        ("좋은 글의 조건 두 가지를 쓰고 설명해 보세요.", "주제가 분명하고 근거가 구체적이어야 한다.", "논술"),
    ],
    8: [
        ("'스마트폰 사용'에 대한 찬성/반대 의견과 근거를 써 보세요.", "적절히 사용하면 정보 검색과 소통에 도움이 되지만, 과하면 학업에 방해가 된다.", "논술"),
        ("'책 읽기'가 요즘 줄어드는 이유와 해결 방법을 써 보세요.", "스마트폰이 재미있어서 책보다 영상을 보기 때문이다. 학교에서 매일 20분 독서 시간을 가지면 좋겠다.", "문제 해결"),
    ],
    9: [
        ("'인권'의 의미와 중요성을 써 보세요.", "인권은 사람으로서 누구나 갖는 기본 권리이다. 인권을 존중해야 평화로운 사회를 만들 수 있다.", "논술"),
        ("'미디어'가 우리 생활에 미치는 영향을 긍정적/부정적 측면에서 써 보세요.", "긍정적으로는 빠른 정보 전달이 가능하고, 부정적으로는 가짜 뉴스에 노출될 수 있다.", "논술"),
    ],
}


GENERATORS = {
    1: [_k1_consonant_vowel, _k1_word_reading, _k1_opposite, _k1_sentence_punct],
    2: [_k2_similar, _k2_sentence_subject, _k1_opposite],
    3: [_k3_dictionary, _k3_paragraph_main, _k3_honorific],
    4: [_k4_metaphor, _k4_fact_opinion, _k4_summary],
    5: [_k5_argument, _k5_literary_element, _k5_media, _k5_proverb],
    6: [_k6_writing_revision, _k6_compare_contrast, _k6_character],
    7: [_k7_morpheme, _k7_speaker, _k7_argument_essay],
    8: [_k8_novel_element, _k8_voice, _k8_debate],
    9: [_k9_literary_value, _k9_phonological_change, _k9_argument_claim],
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
    # 우선 choice/write 유형 채우기
    while len(selected) < count - min(2, len(SOLUTION_BANKS.get(grade, SOLUTION_BANKS[9]))):
        g = random.choice(generators)
        q = g()
        selected.append((q["prompt"], q["answer"], q.get("options", []), q["topic"]))
    # 풀이형 추가
    solution_bank = SOLUTION_BANKS.get(grade, SOLUTION_BANKS[9])
    solution_count = min(2, len(solution_bank), count - len(selected))
    selected += [(prompt, answer, [], topic) for prompt, answer, topic in random.sample(solution_bank, solution_count)]
    random.shuffle(selected)
    selected = selected[:count]
    questions = []
    for prompt, answer, options, topic in selected:
        questions.append(_transform_question(prompt, answer, options, topic))
    return questions
