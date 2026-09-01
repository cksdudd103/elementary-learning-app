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
    1: ["I am happy.", "This is a cat.", "I like apples.", "It is red.", "Good morning.", "Thank you.", "I can run.", "Open the book.", "I see a dog.", "We are friends."],
    2: ["I have a pencil.", "The sun is bright.", "She is my sister.", "He likes soccer.", "We go to school.", "Can you swim?", "This bag is blue.", "I eat breakfast.", "The bird can fly.", "Today is Monday."],
    3: [
        "I go to school every day.", "She has a red bag.", "They are my friends.", "Can I use your pen?",
        "This is my classroom.", "I like my teacher.", "We play in the playground.", "The desk is clean.",
        "It is a sunny day.", "He sits on the chair.",
    ],
    4: [
        "I usually get up at seven.", "My favorite subject is science.", "How much is this notebook?",
        "We visited the museum yesterday.", "He is reading a funny story.", "Would you like some juice?",
        "The library is next to the bank.", "I want to be a doctor.", "She walks to school every morning.",
        "What did you do last weekend?",
    ],
    5: [
        "I have to finish my homework.", "She was watching television then.", "Could you open the window, please?",
        "I am going to visit my grandparents.", "How often do you exercise?", "If it rains, we will stay home.",
        "Walking is good for your health.", "He wants to become a famous singer.",
    ],
    6: [
        "You should drink enough water every day.", "The festival will be held next Saturday.", "I was surprised to hear the news.",
        "Have you ever traveled to another country?", "She practices the piano to become a musician.",
        "We need to protect animals in danger.", "Although he was tired, he kept studying.",
        "The book was written by a young author.",
    ],
    7: ["I have been interested in science since childhood.", "You must wear a helmet while riding a bicycle.", "The girl who is singing on stage is my cousin.", "If you study regularly, you will improve quickly.", "Learning another language takes time and patience."],
    8: ["The project was completed earlier than we expected.", "I look forward to meeting students from other countries.", "The man standing by the gate is our new teacher.", "Unless you hurry, you will miss the last bus.", "She has studied English for more than five years."],
    9: ["If I had more time, I would learn another language.", "The scientist whose work won the prize thanked her team.", "Having finished the assignment, he went out for a walk.", "It is important that everyone respect different opinions.", "Despite being nervous, she delivered an excellent speech."],
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
    sentence = random.choice(SENTENCES[grade])
    words = re.findall(r"[A-Za-z']+", sentence)
    shuffled = words[:]
    while shuffled == words and len(words) > 1:
        random.shuffle(shuffled)
    prompt = " / ".join(shuffled)
    return _make(prompt, sentence, topic)


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
    sentence = random.choice(SENTENCES[grade])
    translations = {
        "I go to school every day.": "나는 매일 학교에 간다.",
        "She has a red bag.": "그녀는 빨간 가방을 가지고 있다.",
        "They are my friends.": "그들은 내 친구들이다.",
        "I usually get up at seven.": "나는 보통 일곱 시에 일어난다.",
        "He is reading a funny story.": "그는 재미있는 이야기를 읽고 있다.",
        "I have to finish my homework.": "나는 숙제를 끝내야 한다.",
        "She was watching television then.": "그녀는 그때 TV를 보고 있었다.",
        "You should drink enough water every day.": "너는 매일 충분한 물을 마셔야 한다.",
        "The festival will be held next Saturday.": "축제는 다음 주 토요일에 열릴 것이다.",
    }
    meaning = translations.get(sentence, "(한국어 뜻)")
    prompt = f"다음 한국어 문장을 영어로 쓰세요.\n'{meaning}'"
    return _make(prompt, sentence, topic)


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
