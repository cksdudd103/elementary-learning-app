import random
import re


VOCABULARY = {
    1: [("cat", "고양이"), ("dog", "개"), ("apple", "사과"), ("red", "빨간색"), ("book", "책"), ("school", "학교"), ("friend", "친구"), ("happy", "행복한")],
    2: [("pencil", "연필"), ("sun", "태양"), ("sister", "여자형제"), ("soccer", "축구"), ("blue", "파란색"), ("breakfast", "아침식사"), ("bird", "새"), ("Monday", "월요일")],
    3: [("basketball", "농구"), ("classroom", "교실"), ("rabbit", "토끼"), ("teeth", "이"), ("milk", "우유"), ("brother", "남자형제"), ("sunny", "맑은"), ("homework", "숙제")],
    4: [("science", "과학"), ("museum", "박물관"), ("story", "이야기"), ("library", "도서관"), ("doctor", "의사"), ("heavier", "더 무거운"), ("weekend", "주말"), ("travel", "여행")],
    5: [("whale", "고래"), ("window", "창문"), ("exercise", "울동"), ("space", "우주"), ("chef", "요리사"), ("exciting", "흥미로운"), ("dolphin", "돌고래"), ("health", "건강")],
    6: [("festival", "축제"), ("camera", "칩processa"), ("country", "나라"), ("mountain", "산"), ("musician", "음악가"), ("danger", "위험"), ("author", "작가"), ("station", "역")],
    7: [("helmet", "헬멧"), ("bicycle", "자전거"), ("cousin", "사촌"), ("patience", "인내심"), ("environment", "환경"), ("tourist", "관광객"), ("confident", "자신감 있는"), ("expected", "예상된")],
    8: [("project", "프로젝트"), ("invention", "발명"), ("opinion", "의견"), ("recycling", "재활용"), ("apologized", "사과했다"), ("meeting", "회의"), ("countries", "나라들"), ("practice", "연습")],
    9: [("scientist", "과학자"), ("documentary", "다큐멘터리"), ("climate", "기후"), ("challenges", "도전"), ("speech", "연설"), ("assignment", "과제"), ("opinions", "의견"), ("solutions", "해결책")],
}

SENTENCES = {
    1: ["I am happy.", "This is a cat.", "I like apples.", "It is red.", "Good morning.", "Thank you.", "I can run.", "Open the book.", "I see a dog.", "We are friends.", "Sit down, please.", "My name is Mina."],
    2: ["I have a pencil.", "The sun is bright.", "She is my sister.", "He likes soccer.", "We go to school.", "Can you swim?", "This bag is blue.", "I eat breakfast.", "The bird can fly.", "Today is Monday.", "Please close the door.", "They are very kind."],
    3: ["I play basketball after school.", "My mother cooks dinner.", "Where is your classroom?", "There are three books.", "We study English together.", "What time is it?", "The rabbit has long ears.", "I brush my teeth every day.", "She does not like milk.", "Do you have a brother?", "It is sunny today.", "Please help me with this."],
    4: ["I usually get up at seven.", "My favorite subject is science.", "How much is this notebook?", "We visited the museum yesterday.", "He is reading a funny story.", "Would you like some juice?", "The library is next to the bank.", "I want to be a doctor.", "She walks to school every morning.", "What did you do last weekend?", "My family will travel tomorrow.", "This box is heavier than that one."],
    5: ["I have to finish my homework.", "She was watching television then.", "The blue whale is the largest animal.", "Could you open the window, please?", "I am going to visit my grandparents.", "How often do you exercise?", "We learned about space at school.", "He wants to become a famous chef.", "The movie was more exciting than the book.", "If it rains, we will stay home.", "I have never seen a dolphin.", "Walking is good for your health."],
    6: ["You should drink enough water every day.", "The festival will be held next Saturday.", "I was surprised to hear the news.", "This is the camera that my uncle gave me.", "Have you ever traveled to another country?", "The mountain is covered with snow in winter.", "She practices the piano to become a musician.", "We need to protect animals in danger.", "The book was written by a young author.", "Please tell me how to get to the station.", "I have lived here for three years.", "Although he was tired, he kept studying."],
    7: ["I have been interested in science since childhood.", "You must wear a helmet while riding a bicycle.", "The girl who is singing on stage is my cousin.", "If you study regularly, you will improve quickly.", "We decided to collect cans for the environment.", "The concert was canceled because of heavy rain.", "Could you tell me where the post office is?", "Learning another language takes time and patience.", "My teacher advised me to read more books.", "The museum is visited by many tourists every year.", "I was doing my homework when he called.", "This problem is easier than I expected."],
    8: ["The project was completed earlier than we expected.", "I look forward to meeting students from other countries.", "The man standing by the gate is our new teacher.", "Unless you hurry, you will miss the last bus.", "She has studied English for more than five years.", "The invention made it possible to communicate faster.", "We were asked to share our opinions with the class.", "Recycling is one of the easiest ways to help Earth.", "I am not sure whether he will join the club.", "The more you practice, the more confident you become.", "He apologized for arriving late at the meeting.", "The story was so moving that everyone became quiet."],
    9: ["If I had more time, I would learn another language.", "The scientist whose work won the prize thanked her team.", "Having finished the assignment, he went out for a walk.", "It is important that everyone respect different opinions.", "The city has changed greatly since I first visited it.", "Not only is exercise healthy, but it also reduces stress.", "The documentary showed how climate change affects wildlife.", "I wish I had listened more carefully to your advice.", "Students are encouraged to develop their own solutions.", "By the time we arrived, the movie had already started.", "What matters most is how we respond to challenges.", "Despite being nervous, she delivered an excellent speech."],
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
    distractors = [m for _, m in random.sample(VOCABULARY[grade], min(4, len(VOCABULARY[grade]))) if m != meaning]
    if len(distractors) < 3:
        distractors += ["학교", "집", "책"]
    prompt = f"'{word}'의 뜻은 무엇인가요?"
    return _make(prompt, meaning, topic, options=[meaning] + distractors[:3])


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
        1: [("I ___ happy.", "am"), ("This ___ a cat.", "is"), ("I can ___.", "run")],
        2: [("She ___ my sister.", "is"), ("He ___ soccer.", "likes"), ("We ___ to school.", "go")],
        3: [("My mother ___ dinner.", "cooks"), ("There ___ three books.", "are"), ("She does not ___ milk.", "like")],
        4: [("We ___ the museum yesterday.", "visited"), ("I want to ___ a doctor.", "be"), ("This box is ___ than that one.", "heavier")],
        5: [("She ___ watching television then.", "was"), ("If it ___, we will stay home.", "rains"), ("I have never ___ a dolphin.", "seen")],
        6: [("The festival will be ___ next Saturday.", "held"), ("The book was ___ by a young author.", "written"), ("I have ___ here for three years.", "lived")],
        7: [("You ___ wear a helmet while riding a bicycle.", "must"), ("The concert was ___ because of heavy rain.", "canceled"), ("This problem is easier than I ___.", "expected")],
        8: [("I look forward to ___ students from other countries.", "meeting"), ("She has studied English for more than five ___.", "years"), ("He apologized for ___ late at the meeting.", "arriving")],
        9: [("If I had more time, I ___ learn another language.", "would"), ("Not only is exercise healthy, but it also ___ stress.", "reduces"), ("Despite being nervous, she ___ an excellent speech.", "delivered")],
    }
    topic = _topic_for(grade, ["문법"])
    sentence, answer = random.choice(templates.get(grade, templates[9]))
    distractors = [a for _, a in random.sample(templates.get(grade, templates[9]), min(4, len(templates.get(grade, templates[9])))) if a != answer]
    if len(distractors) < 3:
        distractors += ["is", "are", "was"]
    return _make(f"빈칸에 알맞은 말을 고르세요.\n{sentence}", answer, topic, options=[answer] + distractors[:3])


def _e_tense_question(grade):
    topic = _topic_for(grade, ["시제", "문법"])
    templates = {
        3: [("I ___ (brush) my teeth every day.", "brush"), ("She ___ (do) not like milk.", "does")],
        4: [("We ___ (visit) the museum yesterday.", "visited"), ("My family ___ (travel) tomorrow.", "will travel")],
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


def _e_listening_or_speaking(grade):
    topic = _topic_for(grade, ["듣기·말하기"])
    sentence = random.choice(SENTENCES[grade])
    question_type = random.choice(["listening", "speaking"])
    if question_type == "listening":
        return _make("문장을 듣고 그대로 입력하세요.", sentence, topic, question_type="listening")
    return _make(sentence, sentence, topic, question_type="speaking")


def _e_translation(grade):
    topic = _topic_for(grade, ["쓰기", "번역"])
    sentence = random.choice(SENTENCES[grade])
    # 간단한 한국어 해석 제공
    translations = {
        "I am happy.": "나는 행복해.",
        "This is a cat.": "이것은 고양이야.",
        "I like apples.": "나는 사과를 좋아해.",
        "Good morning.": "좋은 아침이야.",
        "I have a pencil.": "나는 연필을 가지고 있어.",
        "The sun is bright.": "태양이 밝아.",
        "She is my sister.": "그녀는 내 여동생이야.",
        "I play basketball after school.": "나는 방과 후에 농구를 해.",
        "My mother cooks dinner.": "우리 엄마는 저녁을 요리해.",
        "Where is your classroom?": "너의 교실은 어디에 있니?",
        "I usually get up at seven.": "나는 보통 일곱 시에 일어나.",
        "My favorite subject is science.": "내가 가장 좋아하는 과목은 과학이야.",
        "I have to finish my homework.": "나는 숙제를 끝내야 해.",
        "She was watching television then.": "그녀는 그때 TV를 보고 있었어.",
        "You should drink enough water every day.": "너는 매일 충분한 물을 마셔야 해.",
        "The festival will be held next Saturday.": "축제는 다음 주 토요일에 열릴 거야.",
        "I have been interested in science since childhood.": "나는 어릴 때부터 과학에 관심이 있었어.",
        "The project was completed earlier than we expected.": "그 프로젝트는 예상보다 일찍 완료되었어.",
        "If I had more time, I would learn another language.": "시간이 더 있었다면 다른 언어를 배웠을 텐데.",
    }
    meaning = translations.get(sentence, "(한국어 뜻)")
    prompt = f"다음 한국어 문장을 영어로 쓰세요.\n'{meaning}'"
    return _make(prompt, sentence, topic)


GENERATORS = {
    1: [_e_vocab_choice, _e_word_scramble, _e_sentence_scramble, _e_listening_or_speaking],
    2: [_e_vocab_choice, _e_word_scramble, _e_sentence_scramble, _e_listening_or_speaking],
    3: [_e_vocab_choice, _e_blank_sentence, _e_tense_question, _e_sentence_scramble, _e_listening_or_speaking],
    4: [_e_vocab_choice, _e_blank_sentence, _e_tense_question, _e_sentence_scramble, _e_translation, _e_listening_or_speaking],
    5: [_e_vocab_choice, _e_blank_sentence, _e_tense_question, _e_sentence_scramble, _e_translation, _e_listening_or_speaking],
    6: [_e_vocab_choice, _e_blank_sentence, _e_tense_question, _e_sentence_scramble, _e_translation, _e_listening_or_speaking],
    7: [_e_vocab_choice, _e_blank_sentence, _e_tense_question, _e_sentence_scramble, _e_translation, _e_listening_or_speaking],
    8: [_e_vocab_choice, _e_blank_sentence, _e_tense_question, _e_sentence_scramble, _e_translation, _e_listening_or_speaking],
    9: [_e_vocab_choice, _e_blank_sentence, _e_tense_question, _e_sentence_scramble, _e_translation, _e_listening_or_speaking],
}


def generate_english_set(grade, count=10):
    generators = GENERATORS.get(grade, GENERATORS[9])
    questions = []
    # 듣기/말하기는 각각 1~2개 보장
    min_speaking_listening = 2 if grade >= 3 else 1
    listening_speaking = 0
    target_ls = min(min_speaking_listening, count // 3)
    while listening_speaking < target_ls:
        q = _e_listening_or_speaking(grade)
        questions.append(q)
        if q["question_type"] in ("listening", "speaking"):
            listening_speaking += 1
    while len(questions) < count:
        g = random.choice(generators)
        questions.append(g(grade))
    random.shuffle(questions)
    return questions[:count]
