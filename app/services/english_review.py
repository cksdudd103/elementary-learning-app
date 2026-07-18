import random


WORD_BANKS = {
    1: [
        ("cat", "고양이", "동물"), ("dog", "개", "동물"), ("apple", "사과", "과일"), ("red", "빨간색", "색깔"),
        ("book", "책", "물건"), ("school", "학교", "장소"), ("friend", "친구", "사람"), ("happy", "행복한", "기분"),
        ("run", "달리다", "동작"), ("big", "큰", "형용사"), ("small", "작은", "형용사"), ("water", "물", "음료"),
    ],
    2: [
        ("pencil", "연필", "물건"), ("sun", "태양", "자연"), ("sister", "여자 형제", "가족"), ("soccer", "축구", "울동"),
        ("blue", "파란색", "색깔"), ("breakfast", "아침 식사", "음식"), ("bird", "새", "동물"), ("Monday", "월요일", "요일"),
        ("teacher", "선생님", "사람"), ("classroom", "교실", "장소"), ("fast", "빠른", "형용사"), ("slow", "느린", "형용사"),
    ],
    3: [
        ("basketball", "농구", "울동"), ("rabbit", "토끼", "동물"), ("teeth", "이", "신체"), ("milk", "우유", "음료"),
        ("brother", "남자 형제", "가족"), ("sunny", "맑은", "날씨"), ("homework", "숙제", "학교"), ("library", "도서관", "장소"),
        ("weather", "날씨", "자연"), ("fruit", "과일", "음식"), ("often", "자주", "부사"), ("always", "항상", "부사"),
    ],
    4: [
        ("science", "과학", "과목"), ("museum", "박물관", "장소"), ("story", "이야기", "책"), ("doctor", "의사", "직업"),
        ("heavier", "더 무거운", "형용사"), ("weekend", "주말", "시간"), ("travel", "여행", "활동"), ("subject", "과목", "학교"),
        ("museum", "박물관", "장소"), ("sentence", "문장", "언어"), ("different", "다른", "형용사"), ("favorite", "가장 좋아하는", "형용사"),
    ],
    5: [
        ("whale", "고래", "동물"), ("window", "창문", "집"), ("exercise", "울동", "활동"), ("space", "우주", "과학"),
        ("chef", "요리사", "직업"), ("exciting", "흥미로운", "형용사"), ("dolphin", "돌고래", "동물"), ("health", "건강", "신체"),
        ("environment", "환경", "사회"), ("experience", "경험", "활동"), ("improve", "향상시키다", "동사"), ("neighbor", "이웃", "사람"),
    ],
    6: [
        ("festival", "축제", "행사"), ("camera", "칩processa", "물건"), ("country", "나라", "사회"), ("mountain", "산", "자연"),
        ("musician", "음악가", "직업"), ("danger", "위험", "상황"), ("author", "작가", "직업"), ("station", "역", "장소"),
        ("challenge", "도전", "활동"), ("culture", "문화", "사회"), ("volunteer", "자원봉사", "활동"), ("tradition", "전통", "문화"),
    ],
    7: [
        ("helmet", "헬멧", "물건"), ("bicycle", "자전거", "탈것"), ("cousin", "사촌", "가족"), ("patience", "인내심", "성격"),
        ("environment", "환경", "과학"), ("tourist", "관광객", "사람"), ("confident", "자신감 있는", "형용사"), ("expected", "예상된", "형용사"),
        ("opportunity", "기회", "상황"), ("responsibility", "책임", "사회"), ("communication", "의사소통", "활동"), ("generation", "세대", "사회"),
    ],
    8: [
        ("project", "프로젝트", "학교"), ("invention", "발명", "과학"), ("opinion", "의견", "사회"), ("recycling", "재활용", "환경"),
        ("apologized", "사과했다", "동사"), ("meeting", "회의", "활동"), ("countries", "나라들", "사회"), ("practice", "연습", "활동"),
        ("generation", "세대", "사회"), ("government", "정부", "사회"), ("technology", "기술", "과학"), ("population", "인구", "사회"),
    ],
    9: [
        ("scientist", "과학자", "직업"), ("documentary", "다큐멘터리", "매체"), ("climate", "기후", "과학"), ("challenges", "도전", "활동"),
        ("speech", "연설", "활동"), ("assignment", "과제", "학교"), ("opinions", "의견", "사회"), ("solutions", "해결책", "사회"),
        ("phenomenon", "현상", "과학"), ("consequence", "결과", "사회"), ("perspective", "관점", "사회"), ("contribution", "기여", "사회"),
    ],
}


CONVERSATIONS = {
    1: [
        {
            "title": "인사하기",
            "lines": [
                ("A", "Hello!"),
                ("B", "Hi! How are you?"),
                ("A", "I'm fine, thank you."),
                ("B", "Goodbye!"),
                ("A", "Bye!"),
            ],
        },
        {
            "title": "이름 묻기",
            "lines": [
                ("A", "What's your name?"),
                ("B", "My name is Mina."),
                ("A", "Nice to meet you."),
                ("B", "Nice to meet you, too."),
            ],
        },
    ],
    2: [
        {
            "title": "좋아하는 것",
            "lines": [
                ("A", "Do you like soccer?"),
                ("B", "Yes, I do."),
                ("A", "I like soccer, too."),
                ("B", "Let's play together."),
            ],
        },
        {
            "title": "가족 소개",
            "lines": [
                ("A", "Who is she?"),
                ("B", "She is my sister."),
                ("A", "How old is she?"),
                ("B", "She is seven."),
            ],
        },
    ],
    3: [
        {
            "title": "학교 생활",
            "lines": [
                ("A", "What time is it?"),
                ("B", "It's three o'clock."),
                ("A", "School is over. Let's go home."),
                ("B", "Okay. See you tomorrow."),
            ],
        },
        {
            "title": "취미",
            "lines": [
                ("A", "What do you do after school?"),
                ("B", "I play basketball."),
                ("A", "That sounds fun."),
                ("B", "Yes, I like it very much."),
            ],
        },
    ],
    4: [
        {
            "title": "쇼핑",
            "lines": [
                ("A", "How much is this notebook?"),
                ("B", "It's two thousand won."),
                ("A", "I'll take it."),
                ("B", "Thank you."),
            ],
        },
        {
            "title": "주말 계획",
            "lines": [
                ("A", "What did you do last weekend?"),
                ("B", "I visited my grandmother."),
                ("A", "That sounds nice."),
                ("B", "Yes, I had a good time."),
            ],
        },
    ],
    5: [
        {
            "title": "건강",
            "lines": [
                ("A", "You should drink enough water."),
                ("B", "Why?"),
                ("A", "Because it is good for your health."),
                ("B", "Okay, I will."),
            ],
        },
        {
            "title": "계획",
            "lines": [
                ("A", "What are you going to do tomorrow?"),
                ("B", "I'm going to visit my grandparents."),
                ("A", "Have a good time."),
                ("B", "Thank you."),
            ],
        },
    ],
    6: [
        {
            "title": "환경",
            "lines": [
                ("A", "We need to protect animals in danger."),
                ("B", "I agree. What can we do?"),
                ("A", "We should stop polluting the environment."),
                ("B", "That's a great idea."),
            ],
        },
        {
            "title": "여행",
            "lines": [
                ("A", "Have you ever traveled to another country?"),
                ("B", "Yes, I have been to Japan."),
                ("A", "What did you like there?"),
                ("B", "I liked the food and the people."),
            ],
        },
    ],
    7: [
        {
            "title": "조언",
            "lines": [
                ("A", "I have a problem."),
                ("B", "What's wrong?"),
                ("A", "I can't finish my homework."),
                ("B", "You should make a study plan."),
            ],
        },
        {
            "title": "학교 행사",
            "lines": [
                ("A", "Did you hear about the concert?"),
                ("B", "Yes, it was canceled because of rain."),
                ("A", "That's too bad."),
                ("B", "I know. I was really looking forward to it."),
            ],
        },
    ],
    8: [
        {
            "title": "의견 나누기",
            "lines": [
                ("A", "What do you think about recycling?"),
                ("B", "I think it is one of the easiest ways to help Earth."),
                ("A", "I agree. We should all try harder."),
                ("B", "Yes, small actions can make a big difference."),
            ],
        },
        {
            "title": "동아리",
            "lines": [
                ("A", "Are you going to join the English club?"),
                ("B", "I am not sure yet."),
                ("A", "The more you practice, the more confident you become."),
                ("B", "That's true. I'll join."),
            ],
        },
    ],
    9: [
        {
            "title": "사회 문제",
            "lines": [
                ("A", "What do you think is the biggest challenge today?"),
                ("B", "I think climate change is very serious."),
                ("A", "What should we do about it?"),
                ("B", "We should develop our own solutions and act together."),
            ],
        },
        {
            "title": "인권",
            "lines": [
                ("A", "Why is it important to respect different opinions?"),
                ("B", "Because everyone has the right to think freely."),
                ("A", "I see. We should listen to each other."),
                ("B", "Exactly. That's how we build a peaceful society."),
            ],
        },
    ],
}


def get_word_bank(grade):
    return WORD_BANKS.get(grade, WORD_BANKS[9])


def generate_word_set(grade, count=10):
    bank = get_word_bank(grade)
    if len(bank) >= count:
        return random.sample(bank, count)
    result = bank[:]
    while len(result) < count:
        result.extend(random.sample(bank, min(count - len(result), len(bank))))
    return result[:count]


def get_conversations(grade):
    return CONVERSATIONS.get(grade, CONVERSATIONS[9])


def generate_conversation_review(grade, count=2):
    convs = get_conversations(grade)
    return random.sample(convs, min(count, len(convs)))
