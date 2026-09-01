from typing import Literal

Category = Literal[
    "Greetings",
    "Animals",
    "Colors",
    "Numbers",
    "Family",
    "School",
    "Food",
    "Daily",
    "Weather",
    "Hobbies",
]
Level = Literal["elementary", "middle"]

CATEGORIES: list[Category] = [
    "Greetings",
    "Animals",
    "Colors",
    "Numbers",
    "Family",
    "School",
    "Food",
    "Daily",
    "Weather",
    "Hobbies",
]

LEVELS: list[Level] = ["elementary", "middle"]

LESSONS: list[dict] = [
    # ---------- Elementary ----------
    {"id": "g1", "en": "Hello!", "ko": "안녕하세요!", "category": "Greetings", "level": "elementary", "grammar": ["인사말"]},
    {"id": "g2", "en": "Good morning.", "ko": "좋은 아침이에요.", "category": "Greetings", "level": "elementary", "grammar": ["주어 + be동사", "형용사(좋은) + 명사(아침)"]},
    {"id": "g3", "en": "Good night.", "ko": "안녕히 주무세요.", "category": "Greetings", "level": "elementary", "grammar": ["형용사(좋은) + 명사(밤)"]},
    {"id": "g4", "en": "Thank you.", "ko": "감사합니다.", "category": "Greetings", "level": "elementary", "grammar": ["감사 표현"]},
    {"id": "g5", "en": "I am sorry.", "ko": "미안합니다.", "category": "Greetings", "level": "elementary", "grammar": ["주어(I) + be동사(am) + 형용사(sorry)"]},
    {"id": "g6", "en": "Nice to meet you.", "ko": "만나서 반가워요.", "category": "Greetings", "level": "elementary", "grammar": ["to 부정사", "형용사(nice)"]},
    {"id": "g7", "en": "How are you?", "ko": "어떻게 지내요?", "category": "Greetings", "level": "elementary", "grammar": ["의문문", "be동사(are)"]},
    {"id": "g8", "en": "I am fine, thank you.", "ko": "잘 지내요, 감사합니다.", "category": "Greetings", "level": "elementary", "grammar": ["주어(I) + be동사(am) + 형용사(fine)", "감사 표현"]},

    {"id": "a1", "en": "It is a cat.", "ko": "그것은 고양이입니다.", "category": "Animals", "level": "elementary", "grammar": ["주어(It) + be동사(is) + 주격보어(a cat)", "부정관사(a)"]},
    {"id": "a2", "en": "I like dogs.", "ko": "나는 개를 좋아해요.", "category": "Animals", "level": "elementary", "grammar": ["주어(I) + 동사(like) + 목적어(dogs)", "복수명사"]},
    {"id": "a3", "en": "The bird is small.", "ko": "새는 작아요.", "category": "Animals", "level": "elementary", "grammar": ["주어(The bird) + be동사(is) + 형용사(small)", "정관사(the)"]},
    {"id": "a4", "en": "I see a rabbit.", "ko": "토끼를 보아요.", "category": "Animals", "level": "elementary", "grammar": ["주어(I) + 동사(see) + 목적어(a rabbit)", "부정관사(a)"]},
    {"id": "a5", "en": "The elephant is big.", "ko": "코끼리는 커요.", "category": "Animals", "level": "elementary", "grammar": ["주어(The elephant) + be동사(is) + 형용사(big)", "정관사(the)"]},
    {"id": "a6", "en": "Fish can swim.", "ko": "물고기는 수영할 수 있어요.", "category": "Animals", "level": "elementary", "grammar": ["주어(Fish) + 조동사(can) + 동사(swim)", "복수명사"]},

    {"id": "c1", "en": "The sky is blue.", "ko": "하늘은 파란색입니다.", "category": "Colors", "level": "elementary", "grammar": ["주어(The sky) + be동사(is) + 주격보어(blue)", "정관사(the)"]},
    {"id": "c2", "en": "I like red.", "ko": "나는 빨간색을 좋아해요.", "category": "Colors", "level": "elementary", "grammar": ["주어(I) + 동사(like) + 목적어(red)", "색깔 명사"]},
    {"id": "c3", "en": "Grass is green.", "ko": "잔디는 초록색입니다.", "category": "Colors", "level": "elementary", "grammar": ["주어(Grass) + be동사(is) + 주격보어(green)", "불가산명사"]},
    {"id": "c4", "en": "The sun is yellow.", "ko": "태양은 노란색입니다.", "category": "Colors", "level": "elementary", "grammar": ["주어(The sun) + be동사(is) + 주격보어(yellow)", "정관사(the)"]},
    {"id": "c5", "en": "My bag is black.", "ko": "내 가방은 검은색입니다.", "category": "Colors", "level": "elementary", "grammar": ["주어(My bag) + be동사(is) + 주격보어(black)", "소유격(My)"]},
    {"id": "c6", "en": "The cat is white.", "ko": "고양이는 흰색입니다.", "category": "Colors", "level": "elementary", "grammar": ["주어(The cat) + be동사(is) + 주격보어(white)", "정관사(the)"]},

    {"id": "n1", "en": "I am seven years old.", "ko": "나는 일곱 살이에요.", "category": "Numbers", "level": "elementary", "grammar": ["주어(I) + be동사(am) + 나이 표현", "수(7) + 복수명사(years old)"]},
    {"id": "n2", "en": "I have two apples.", "ko": "사과 두 개가 있어요.", "category": "Numbers", "level": "elementary", "grammar": ["주어(I) + 동사(have) + 목적어(two apples)", "수(2) + 복수명사(apples)"]},
    {"id": "n3", "en": "One, two, three.", "ko": "하나, 둘, 셋.", "category": "Numbers", "level": "elementary", "grammar": ["기수"]},
    {"id": "n4", "en": "There are five books.", "ko": "책이 다섯 권 있어요.", "category": "Numbers", "level": "elementary", "grammar": ["There is/are 구문", "수(5) + 복수명사(books)"]},
    {"id": "n5", "en": "I see ten birds.", "ko": "새 열 마리를 보아요.", "category": "Numbers", "level": "elementary", "grammar": ["주어(I) + 동사(see) + 목적어(ten birds)", "수(10) + 복수명사(birds)"]},

    {"id": "f1", "en": "This is my mom.", "ko": "이 분은 우리 엄마예요.", "category": "Family", "level": "elementary", "grammar": ["주어(This) + be동사(is) + 주격보어(my mom)", "소유격(my)"]},
    {"id": "f2", "en": "My dad is tall.", "ko": "우리 아빠는 키가 커요.", "category": "Family", "level": "elementary", "grammar": ["주어(My dad) + be동사(is) + 형용사(tall)", "소유격(My)"]},
    {"id": "f3", "en": "I love my family.", "ko": "나는 가족을 사랑해요.", "category": "Family", "level": "elementary", "grammar": ["주어(I) + 동사(love) + 목적어(my family)", "소유격(my)"]},
    {"id": "f4", "en": "My brother is kind.", "ko": "우리 남동생은 착해요.", "category": "Family", "level": "elementary", "grammar": ["주어(My brother) + be동사(is) + 형용사(kind)", "소유격(My)"]},
    {"id": "f5", "en": "My sister is cute.", "ko": "우리 여동생은 귀여워요.", "category": "Family", "level": "elementary", "grammar": ["주어(My sister) + be동사(is) + 형용사(cute)", "소유격(My)"]},

    {"id": "s1", "en": "I go to school.", "ko": "나는 학교에 가요.", "category": "School", "level": "elementary", "grammar": ["주어(I) + 동사(go) + 전치사구(to school)", "전치사(to)"]},
    {"id": "s2", "en": "I like my teacher.", "ko": "나는 선생님을 좋아해요.", "category": "School", "level": "elementary", "grammar": ["주어(I) + 동사(like) + 목적어(my teacher)", "소유격(my)"]},
    {"id": "s3", "en": "I read a book.", "ko": "나는 책을 읽어요.", "category": "School", "level": "elementary", "grammar": ["주어(I) + 동사(read) + 목적어(a book)", "부정관사(a)"]},
    {"id": "s4", "en": "Please open your book.", "ko": "책을 펴 주세요.", "category": "School", "level": "elementary", "grammar": ["청유문", "소유격(your)"]},
    {"id": "s5", "en": "I write in my notebook.", "ko": "나는 공책에 써요.", "category": "School", "level": "elementary", "grammar": ["주어(I) + 동사(write) + 전치사구(in my notebook)", "소유격(my)"]},
    {"id": "s6", "en": "May I go to the bathroom?", "ko": "화장실에 가도 돼요?", "category": "School", "level": "elementary", "grammar": ["의문문", "조동사(May)", "전치사(to)"]},

    {"id": "fo1", "en": "I like apples.", "ko": "나는 사과를 좋아해요.", "category": "Food", "level": "elementary", "grammar": ["주어(I) + 동사(like) + 목적어(apples)", "복수명사"]},
    {"id": "fo2", "en": "I drink milk.", "ko": "나는 우유를 마셔요.", "category": "Food", "level": "elementary", "grammar": ["주어(I) + 동사(drink) + 목적어(milk)", "불가산명사"]},
    {"id": "fo3", "en": "This pizza is yummy.", "ko": "이 피자는 맛있어요.", "category": "Food", "level": "elementary", "grammar": ["주어(This pizza) + be동사(is) + 형용사(yummy)", "지시대명사(This)"]},
    {"id": "fo4", "en": "I eat rice every day.", "ko": "나는 매일 밥을 먹어요.", "category": "Food", "level": "elementary", "grammar": ["주어(I) + 동사(eat) + 목적어(rice)", "부사(every day)", "불가산명사(rice)"]},
    {"id": "fo5", "en": "I want some water.", "ko": "물을 좀 마시고 싶어요.", "category": "Food", "level": "elementary", "grammar": ["주어(I) + 동사(want) + 목적어(some water)", "불가산명사(water)"]},

    {"id": "d1", "en": "I wake up early.", "ko": "나는 일찍 일어나요.", "category": "Daily", "level": "elementary", "grammar": ["주어(I) + 동사(wake up) + 부사(early)", "부사구"]},
    {"id": "d2", "en": "I brush my teeth.", "ko": "나는 이를 닦아요.", "category": "Daily", "level": "elementary", "grammar": ["주어(I) + 동사(brush) + 목적어(my teeth)", "소유격(my)"]},
    {"id": "d3", "en": "I play with my friend.", "ko": "나는 친구와 놀아요.", "category": "Daily", "level": "elementary", "grammar": ["주어(I) + 동사(play) + 전치사구(with my friend)", "전치사(with)", "소유격(my)"]},
    {"id": "d4", "en": "It is sunny today.", "ko": "오늘은 화창해요.", "category": "Daily", "level": "elementary", "grammar": ["주어(It) + be동사(is) + 형용사(sunny)", "시간부사(today)"]},
    {"id": "d5", "en": "I go to bed at nine.", "ko": "나는 아홉 시에 잠자리에 들어요.", "category": "Daily", "level": "elementary", "grammar": ["주어(I) + 동사(go) + 전치사구(to bed)", "시간전치사(at)"]},

    # ---------- Middle ----------
    {"id": "mg1", "en": "How have you been?", "ko": "잘 지냈어요?", "category": "Greetings", "level": "middle", "grammar": ["현재완료", "have been"]},
    {"id": "mg2", "en": "It is nice to see you again.", "ko": "다시 만나서 반가워요.", "category": "Greetings", "level": "middle", "grammar": ["주어(It) + be동사(is) + 형용사(nice)", "to 부정사", "부사(again)"]},

    {"id": "ma1", "en": "A dog is running in the park.", "ko": "공원에서 개가 뛰고 있어요.", "category": "Animals", "level": "middle", "grammar": ["주어(A dog) + 현재진행형(is running)", "장소전치사(in the park)"]},
    {"id": "ma2", "en": "The rabbit jumped over the fence.", "ko": "토끼가 울타리를 뛰어넘었어요.", "category": "Animals", "level": "middle", "grammar": ["주어(The rabbit) + 동사(jumped)", "과거시제", "전치사(over)"]},

    {"id": "mc1", "en": "Her dress was bright pink.", "ko": "그녀의 드레스는 밝은 분홍색이었어요.", "category": "Colors", "level": "middle", "grammar": ["주어(Her dress) + be동사 과거(was)", "소유격(Her)", "형용사(bright pink)"]},
    {"id": "mc2", "en": "The leaves turn yellow in autumn.", "ko": "가을에 잎은 노랗게 변해요.", "category": "Colors", "level": "middle", "grammar": ["주어(The leaves) + 동사(turn)", "주격보어(yellow)", "시간전치사(in autumn)"]},

    {"id": "mn1", "en": "About twenty students came to class.", "ko": "약 스무 명의 학생들이 수업에 왔어요.", "category": "Numbers", "level": "middle", "grammar": ["부사(About)", "주어(twenty students)", "동사(came)", "과거시제"]},
    {"id": "mn2", "en": "I have lived here for three years.", "ko": "나는 여기에 3년 동안 살았어요.", "category": "Numbers", "level": "middle", "grammar": ["주어(I) + 현재완료(have lived)", "기간전치사(for)", "수(3) + 복수명사(years)"]},

    {"id": "mf1", "en": "My parents always support me.", "ko": "우리 부모님은 항상 나를 지지해 주세요.", "category": "Family", "level": "middle", "grammar": ["주어(My parents) + 부사(always) + 동사(support) + 목적어(me)", "복수명사"]},
    {"id": "mf2", "en": "My younger brother plays the piano well.", "ko": "우리 남동생은 피아노를 잘 쳐요.", "category": "Family", "level": "middle", "grammar": ["주어(My younger brother) + 동사(plays) + 목적어(the piano)", "부사(well)", "정관사(the) + 악기"]},

    {"id": "ms1", "en": "The teacher explained the lesson clearly.", "ko": "선생님이 그 수업을 분명하게 설명하셨어요.", "category": "School", "level": "middle", "grammar": ["주어(The teacher) + 동사(explained) + 목적어(the lesson)", "부사(clearly)", "과거시제"]},
    {"id": "ms2", "en": "We will have a math test tomorrow.", "ko": "우리는 내일 수학 시험이 있을 거예요.", "category": "School", "level": "middle", "grammar": ["주어(We) + 미래시제(will have)", "목적어(a math test)", "시간부사(tomorrow)"]},

    {"id": "mfo1", "en": "She made a delicious cake for us.", "ko": "그녀는 우리를 위해 맛있는 케이크를 만들었어요.", "category": "Food", "level": "middle", "grammar": ["주어(She) + 동사(made) + 목적어(a delicious cake)", "형용사(delicious)", "전치사(for)", "과거시제"]},
    {"id": "mfo2", "en": "This soup tastes salty.", "ko": "이 수프는 짠 맛이 나요.", "category": "Food", "level": "middle", "grammar": ["주어(This soup) + 감각동사(tastes) + 주격보어(salty)", "지시대명사(This)"]},

    {"id": "md1", "en": "After school, I usually do my homework.", "ko": "학교 끝나고 나는 보통 숙제를 해요.", "category": "Daily", "level": "middle", "grammar": ["시간부사구(After school)", "주어(I) + 부사(usually) + 동사(do) + 목적어(my homework)", "소유격(my)"]},
    {"id": "md2", "en": "He did not finish his breakfast.", "ko": "그는 아침 식사를 끝내지 못했어요.", "category": "Daily", "level": "middle", "grammar": ["주어(He) + 부정문(did not finish)", "목적어(his breakfast)", "과거시제", "소유격(his)"]},

    {"id": "w1", "en": "It might rain this afternoon.", "ko": "오늘 오후에 비가 올지도 몰라요.", "category": "Weather", "level": "middle", "grammar": ["주어(It) + 조동사(might) + 동사(rain)", "시간부사구(this afternoon)"]},
    {"id": "w2", "en": "The wind blew strongly yesterday.", "ko": "어제 바람이 세게 불었어요.", "category": "Weather", "level": "middle", "grammar": ["주어(The wind) + 동사(blew) + 부사(strongly)", "과거시제", "시간부사(yesterday)"]},
    {"id": "w3", "en": "If it snows, we can build a snowman.", "ko": "눈이 오면 우리는 눈사람을 만들 수 있어요.", "category": "Weather", "level": "middle", "grammar": ["조걱문(if)", "주어(we) + 조동사(can) + 동사(build)", "목적어(a snowman)"]},

    {"id": "h1", "en": "I enjoy reading comic books.", "ko": "나는 만화책 읽는 것을 즐겨요.", "category": "Hobbies", "level": "middle", "grammar": ["주어(I) + 동사(enjoy) + 동명사(reading)", "목적어(comic books)", "복수명사"]},
    {"id": "h2", "en": "She has been learning English for two years.", "ko": "그녀는 2년 동안 영어를 배우고 있어요.", "category": "Hobbies", "level": "middle", "grammar": ["주어(She) + 현재완료진행(has been learning)", "목적어(English)", "기간전치사(for)", "수(2) + 복수명사(years)"]},
    {"id": "h3", "en": "My friends invited me to a movie.", "ko": "친구들이 나를 영화에 초대했어요.", "category": "Hobbies", "level": "middle", "grammar": ["주어(My friends) + 동사(invited) + 목적어(me)", "to 부정사", "소유격(My)", "과거시제"]},
]


def get_lessons(category: str | None = None, level: str | None = None) -> list[dict]:
    """Return lessons filtered by category and level."""
    result = LESSONS[:]
    if level and level != "all":
        result = [item for item in result if item["level"] == level]
    if category and category != "all":
        result = [item for item in result if item["category"] == category]
    return result


def normalize_answer(text: str) -> str:
    return (
        text.lower()
        .replace(".", "")
        .replace(",", "")
        .replace("?", "")
        .replace("!", "")
        .strip()
    )


def is_correct(input_text: str, answer: str) -> bool:
    return normalize_answer(input_text) == normalize_answer(answer)
