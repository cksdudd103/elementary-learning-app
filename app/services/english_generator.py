import random
import re


# 2022 개정 교육과정: 영어는 3~4학년군, 5~6학년군으로 운영
# 3~4학년: 알파벳/파닉스, 기본 어휘, 간단한 문장
# 5~6학년: 시제, 의문문, 어휘 확장, 문장 확장

VOCABULARY = {
    1: [("cat", "고양이"), ("dog", "개"), ("apple", "사과"), ("red", "빨간색"), ("book", "책"), ("school", "학교"), ("friend", "친구"), ("happy", "행복한")],
    2: [("pencil", "연필"), ("sun", "태양"), ("sister", "여자형제"), ("soccer", "축구"), ("blue", "파란색"), ("breakfast", "아침식사"), ("bird", "새"), ("Monday", "월요일")],
    3: [
        ("bag", "가방"), ("desk", "책상"), ("chair", "의자"), ("pen", "펜"), ("eraser", "지우개"),
        ("ruler", "자"), ("door", "문"), ("window", "창문"), ("teacher", "선생님"), ("student", "학생"),
        ("big", "큰"), ("small", "작은"), ("long", "긴"), ("short", "짧은"),
    ],
    4: [
        ("classroom", "교실"), ("library", "도서관"), ("gym", "체육관"), ("playground", "울장"),
        ("homework", "숙제"), ("subject", "과목"), ("science", "과학"), ("music", "음악"),
        ("delicious", "맛있는"), ("beautiful", "아름다운"), ("favorite", "가장 좋아하는"), ("interesting", "흥미로운"),
    ],
    5: [
        ("travel", "여행"), ("hobby", "취미"), ("experience", "경험"), ("environment", "환경"),
        ("healthy", "건강한"), ("dangerous", "위험한"), ("wonderful", "멋진"), ("terrible", "끔찍한"),
        ("decide", "결정하다"), ("prepare", "준비하다"), ("improve", "향상시키다"), ("protect", "보호하다"),
    ],
    6: [
        ("confidence", "자신감"), ("challenge", "도전"), ("opportunity", "기회"), ("responsibility", "책임"),
        ("consider", "고려하다"), ("achieve", "성취하다"), ("contribute", "기여하다"), ("apologize", "사과하다"),
        ("although", "비록 ~일지라도"), ("however", "그러나"), ("therefore", "따라서"), ("instead", "대신에"),
    ],
    7: [("helmet", "헬멧"), ("bicycle", "자전거"), ("cousin", "사촌"), ("patience", "인내심"), ("environment", "환경"), ("tourist", "관광객"), ("confident", "자신감 있는"), ("expected", "예상된")],
    8: [("project", "프로젝트"), ("invention", "발명"), ("opinion", "의견"), ("recycling", "재활용"), ("apologized", "사과했다"), ("meeting", "회의"), ("countries", "나라들"), ("practice", "연습")],
    9: [("scientist", "과학자"), ("documentary", "다큐멘터리"), ("climate", "기후"), ("challenges", "도전"), ("speech", "연설"), ("assignment", "과제"), ("opinions", "의견"), ("solutions", "해결책")],
}

SENTENCES = {
    1: [
        ("I am happy.", "나는 행복해요."),
        ("This is a cat.", "이것은 고양이예요."),
        ("I like apples.", "나는 사과를 좋아해요."),
        ("It is red.", "그것은 빨간색이에요."),
        ("Good morning.", "좋은 아침이에요."),
        ("Thank you.", "감사해요."),
        ("I can run.", "나는 뛸 수 있어요."),
        ("Open the book.", "책을 펼쳐요."),
        ("I see a dog.", "나는 개를 봐요."),
        ("We are friends.", "우리는 친구예요."),
    ],
    2: [
        ("I have a pencil.", "나는 연필을 가지고 있어요."),
        ("The sun is bright.", "태양이 밝아요."),
        ("She is my sister.", "그녀는 내 여자 형제예요."),
        ("He likes soccer.", "그는 축구를 좋아해요."),
        ("We go to school.", "우리는 학교에 가요."),
        ("Can you swim?", "너는 수영할 수 있니?"),
        ("This bag is blue.", "이 가방은 파란색이에요."),
        ("I eat breakfast.", "나는 아침을 먹어요."),
        ("The bird can fly.", "새는 날 수 있어요."),
        ("Today is Monday.", "오늘은 월요일이에요."),
    ],
    3: [
        ("I go to school every day.", "나는 매일 학교에 가요."),
        ("She has a red bag.", "그녀는 빨간 가방을 가지고 있어요."),
        ("They are my friends.", "그들은 내 친구들이에요."),
        ("Can I use your pen?", "네 펜을 써도 될까요?"),
        ("This is my classroom.", "이것은 내 교실이에요."),
        ("I like my teacher.", "나는 우리 선생님을 좋아해요."),
        ("We play in the playground.", "우리는 울장에서 놀아요."),
        ("The desk is clean.", "책상이 깨끗해요."),
        ("It is a sunny day.", "오늘은 맑은 날이에요."),
        ("He sits on the chair.", "그는 의자에 앉아요."),
    ],
    4: [
        ("I usually get up at seven.", "나는 보통 일곱 시에 일어나요."),
        ("My favorite subject is science.", "내가 가장 좋아하는 과목은 과학이에요."),
        ("How much is this notebook?", "이 공책은 얼마예요?"),
        ("We visited the museum yesterday.", "우리는 어제 박물관에 방문했어요."),
        ("He is reading a funny story.", "그는 재미있는 이야기를 읽고 있어요."),
        ("Would you like some juice?", "주스를 좀 드릴까요?"),
        ("The library is next to the bank.", "도서관은 은행 옆에 있어요."),
        ("I want to be a doctor.", "나는 의사가 되고 싶어요."),
        ("She walks to school every morning.", "그녀는 매일 아침 학교에 걸어가요."),
        ("What did you do last weekend?", "지난 주말에 뭐 했어요?"),
    ],
    5: [
        ("I have to finish my homework.", "나는 숙제를 끝내야 해요."),
        ("She was watching television then.", "그녀는 그때 TV를 보고 있었어요."),
        ("Could you open the window, please?", "창문을 좀 열어 주시겠어요?"),
        ("I am going to visit my grandparents.", "나는 조부모님을 뵈러 갈 거예요."),
        ("How often do you exercise?", "얼마나 자주 울동해요?"),
        ("If it rains, we will stay home.", "비가 오면 우리는 집에 있을 거예요."),
        ("Walking is good for your health.", "걷기는 건강에 좋아요."),
        ("He wants to become a famous singer.", "그는 유명한 가수가 되고 싶어해요."),
    ],
    6: [
        ("You should drink enough water every day.", "너는 매일 충분한 물을 마셔야 해요."),
        ("The festival will be held next Saturday.", "축제는 다음 주 토요일에 열릴 거예요."),
        ("I was surprised to hear the news.", "그 소식을 듣고 놀랐어요."),
        ("Have you ever traveled to another country?", "다른 나라에 가 본 적이 있어요?"),
        ("She practices the piano to become a musician.", "그녀는 음악가가 되기 위해 피아노를 연습해요."),
        ("We need to protect animals in danger.", "우리는 위험에 처한 동물들을 보호해야 해요."),
        ("Although he was tired, he kept studying.", "그는 피곤했지만 계속 공부했어요."),
        ("The book was written by a young author.", "그 책은 젊은 작가에 의해 쓰였어요."),
    ],
    7: [
        ("I have been interested in science since childhood.", "나는 어렸을 때부터 과학에 관심이 있었어요."),
        ("You must wear a helmet while riding a bicycle.", "자전거를 탈 때는 헬멧을 써야 해요."),
        ("The girl who is singing on stage is my cousin.", "묵대에서 노래하는 소녀는 내 사촌이에요."),
        ("If you study regularly, you will improve quickly.", "규칙적으로 공부하면 빨리 늘 거예요."),
        ("Learning another language takes time and patience.", "다른 언어를 배우는 것은 시간과 인내심이 필요해요."),
    ],
    8: [
        ("The project was completed earlier than we expected.", "그 프로젝트는 우리가 예상했던 것보다 일찍 완료되었어요."),
        ("I look forward to meeting students from other countries.", "다른 나라 학생들을 만나게 되어 기대돼요."),
        ("The man standing by the gate is our new teacher.", "문 옆에 서 있는 남자는 우리의 새 선생님이에요."),
        ("Unless you hurry, you will miss the last bus.", "서두르지 않으면 마지막 버스를 놓칠 거예요."),
        ("She has studied English for more than five years.", "그녀는 영어를 5년 넘게 공부했어요."),
    ],
    9: [
        ("If I had more time, I would learn another language.", "시간이 더 있으면 다른 언어를 배울 텐데요."),
        ("The scientist whose work won the prize thanked her team.", "상을 받은 연구를 한 과학자는 그녀의 팀에 감사했어요."),
        ("Having finished the assignment, he went out for a walk.", "과제를 끝낸 후 그는 산책하러 나갔어요."),
        ("It is important that everyone respect different opinions.", "모두가 다른 의견을 존중하는 것이 중요해요."),
        ("Despite being nervous, she delivered an excellent speech.", "긴장했음에도 불구하고 그녀는 훌륭한 연설을 했어요."),
    ],
}


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
    return random.choice(_curriculum_topics("english", grade, fallback))


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


def _e_vocab_choice(grade):
    topic = _topic_for(grade, ["어휘"])
    word, meaning = random.choice(VOCABULARY[grade])
    all_meanings = [m for _, m in VOCABULARY[grade]]
    distractors = [m for m in random.sample(all_meanings, min(4, len(all_meanings))) if m != meaning]
    if len(distractors) < 3:
        distractors += ["학교", "집", "책"]
    prompt = f"'{word}'의 뜻은 무엇인가요?"
    return _make(prompt, meaning, topic, options=_choice_options(meaning, distractors[:3]))


def _e_word_scramble(grade):
    topic = _topic_for(grade, ["어휘", "문장 만들기"])
    word, meaning = random.choice(VOCABULARY[grade])
    letters = list(word)
    shuffled = letters[:]
    while shuffled == letters and len(letters) > 1:
        random.shuffle(shuffled)
    prompt = f"'{meaning}'의 영어 낱말을 알맞게 배열하세요. ({' '.join(shuffled)})"
    return _make(prompt, word, topic)


def _e_sentence_scramble(grade):
    topic = _topic_for(grade, ["문장 만들기"])
    sentence, meaning = random.choice(SENTENCES[grade])
    words = re.findall(r"[A-Za-z']+", sentence)
    shuffled = words[:]
    while shuffled == words and len(words) > 1:
        random.shuffle(shuffled)
    prompt = " / ".join(shuffled)
    return _make(prompt, sentence, topic, explanation=f"뜻: {meaning}")


def _e_blank_sentence(grade):
    templates = {
        3: [
            ("I ___ to school every day.", "go", ["goes", "going", "went"]),
            ("She ___ a red bag.", "has", ["have", "had", "having"]),
            ("They ___ my friends.", "are", ["is", "was", "were"]),
        ],
        4: [
            ("I usually ___ up at seven.", "get", ["gets", "got", "getting"]),
            ("He ___ a funny story.", "is reading", ["reads", "read", "was read"]),
            ("The library ___ next to the bank.", "is", ["are", "was", "were"]),
        ],
        5: [
            ("She ___ watching television then.", "was", ["is", "were", "be"]),
            ("If it ___, we will stay home.", "rains", ["rain", "rained", "raining"]),
            ("I ___ never seen a dolphin.", "have", ["has", "had", "having"]),
        ],
        6: [
            ("The festival ___ be held next Saturday.", "will", ["is", "was", "were"]),
            ("The book ___ written by a young author.", "was", ["is", "were", "be"]),
            ("I have lived here ___ three years.", "for", ["since", "at", "on"]),
        ],
        7: [
            ("You ___ wear a helmet while riding a bicycle.", "must", ["can", "may", "will"]),
            ("The concert was canceled ___ of heavy rain.", "because", ["so", "but", "and"]),
            ("This problem is easier than I ___.", "expected", ["expect", "expecting", "had expected"]),
        ],
        8: [
            ("I look forward to ___ students from other countries.", "meeting", ["meet", "met", "meets"]),
            ("She has studied English for more than five ___.", "years", ["year", "year's", "years'"]),
            ("He apologized for ___ late at the meeting.", "arriving", ["arrive", "arrived", "arrives"]),
        ],
        9: [
            ("If I had more time, I ___ learn another language.", "would", ["will", "can", "may"]),
            ("Not only is exercise healthy, but it also ___ stress.", "reduces", ["reduce", "reducing", "reduced"]),
            ("Despite being nervous, she ___ an excellent speech.", "delivered", ["deliver", "delivering", "was delivered"]),
        ],
    }
    topic = _topic_for(grade, ["문법"])
    bank = templates.get(grade, templates[9])
    sentence, answer, distractors = random.choice(bank)
    prompt = f"빈칸에 알맞은 말을 고르세요.\n{sentence}"
    return _make(prompt, answer, topic, options=_choice_options(answer, distractors))


def _e_tense_question(grade):
    topic = _topic_for(grade, ["시제", "문법"])
    templates = {
        4: [("I ___ (get) up at seven every day.", "get"), ("She ___ (walk) to school every morning.", "walks")],
        5: [("She ___ (watch) television then.", "was watching"), ("If it rains, we ___ (stay) home.", "will stay")],
        6: [("The festival ___ (hold) next Saturday.", "will be held"), ("I ___ (live) here for three years.", "have lived")],
        7: [("The concert ___ (cancel) because of heavy rain.", "was canceled"), ("I ___ (do) my homework when he called.", "was doing")],
        8: [("She ___ (study) English for more than five years.", "has studied"), ("The project ___ (complete) earlier than expected.", "was completed")],
        9: [("If I had more time, I ___ (learn) another language.", "would learn"), ("By the time we arrived, the movie ___ (start) already.", "had started")],
    }
    bank = templates.get(grade, [])
    if not bank:
        return _e_blank_sentence(grade)
    sentence, answer = random.choice(bank)
    prompt = f"괄호 안 동사의 알맞은 형태로 바꿔 쓰세요.\n{sentence}"
    return _make(prompt, answer, topic)


def _e_translation(grade):
    topic = _topic_for(grade, ["쓰기", "번역"])
    sentence, meaning = random.choice(SENTENCES[grade])
    prompt = f"다음 한국어 문장을 영어로 쓰세요.\n'{meaning}'"
    return _make(prompt, sentence, topic, explanation=f"해석: {meaning}")


GENERATORS = {
    1: [_e_vocab_choice, _e_word_scramble],
    2: [_e_vocab_choice, _e_word_scramble],
    3: [_e_vocab_choice, _e_blank_sentence, _e_sentence_scramble, _e_word_scramble],
    4: [_e_vocab_choice, _e_blank_sentence, _e_sentence_scramble, _e_tense_question, _e_translation],
    5: [_e_vocab_choice, _e_blank_sentence, _e_tense_question, _e_sentence_scramble, _e_translation],
    6: [_e_vocab_choice, _e_blank_sentence, _e_tense_question, _e_sentence_scramble, _e_translation],
    7: [_e_vocab_choice, _e_blank_sentence, _e_tense_question, _e_sentence_scramble, _e_translation],
    8: [_e_vocab_choice, _e_blank_sentence, _e_tense_question, _e_sentence_scramble, _e_translation],
    9: [_e_vocab_choice, _e_blank_sentence, _e_tense_question, _e_sentence_scramble, _e_translation],
}


def generate_english_set(grade, count=10):
    generators = GENERATORS.get(grade, GENERATORS[9])
    questions = []
    while len(questions) < count:
        g = random.choice(generators)
        questions.append(g(grade))
    random.shuffle(questions)
    return questions[:count]


def _choice_options(answer, distractors, shuffle=True):
    opts = [str(answer)] + [str(d) for d in distractors]
    if shuffle:
        random.shuffle(opts)
    return opts
