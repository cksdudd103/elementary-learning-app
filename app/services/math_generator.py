import random


def make(
    prompt,
    answer,
    topic,
    explanation=None,
    options=None,
    question_type=None,
    image_url=None,
    max_points=10,
):
    determined_type = question_type or ("choice" if options else "write")
    return {
        "prompt": prompt,
        "answer": str(answer),
        "topic": topic,
        "explanation": explanation or f"정답은 {answer}입니다.",
        "question_type": determined_type,
        "options": options or [],
        "image_url": image_url,
        "max_points": max_points,
    }


def _choice_options(answer, distractors, shuffle=True):
    opts = [str(answer)] + [str(d) for d in distractors]
    if shuffle:
        random.shuffle(opts)
    return opts


def _distractors(answer, count=3, min_val=None, max_val=None, step=1, exclude=None):
    exclude = set(str(x) for x in (exclude or []))
    exclude.add(str(answer))
    candidates = set()
    attempts = 0
    while len(candidates) < count and attempts < count * 50:
        offset = random.choice([step * i for i in range(1, count + 5)])
        sign = random.choice([-1, 1])
        val = answer + sign * offset
        if min_val is not None and val < min_val:
            val = answer + offset
        if max_val is not None and val > max_val:
            val = answer - offset
        if str(val) not in exclude and (min_val is None or val >= min_val) and (max_val is None or val <= max_val):
            candidates.add(val)
        attempts += 1
    for delta in range(1, count * 5):
        if len(candidates) >= count:
            break
        for sign in (-1, 1):
            val = answer + sign * delta * step
            if str(val) not in exclude and (min_val is None or val >= min_val) and (max_val is None or val <= max_val):
                candidates.add(val)
    return [str(v) for v in list(candidates)[:count]]


def _arithmetic_choices(answer, count=4, span=10):
    opts = {answer}
    deltas = list(range(1, span + 1))
    random.shuffle(deltas)
    for d in deltas:
        if len(opts) >= count:
            break
        for v in (answer + d, answer - d):
            if v >= 0:
                opts.add(v)
    opts = list(opts)[:count]
    random.shuffle(opts)
    return [str(o) for o in opts]


def _topic_for(grade, fallback):
    try:
        from ..models import CurriculumUnit
        units = CurriculumUnit.query.filter_by(subject="math", grade_level=grade).order_by(CurriculumUnit.unit_order).all()
        if units:
            return random.choice([u.unit_name for u in units])
    except Exception:
        pass
    return random.choice(fallback)


# ============================================================
# 1학년: 9까지/50까지/100까지 수, 한 자리 덧셈·뺄셈
# ============================================================
def _g1_addition():
    a, b = random.randint(1, 5), random.randint(1, 4)
    answer = a + b
    topic = _topic_for(1, ["수와 연산", "덧셈"])
    prompt = f"{a} + {b} = ?"
    return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=6))


def _g1_subtraction():
    a, b = random.randint(2, 9), random.randint(1, 5)
    answer = a - b
    topic = _topic_for(1, ["수와 연산", "뺄셈"])
    prompt = f"{a} - {b} = ?"
    return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=6))


def _g1_compare():
    a, b = random.randint(1, 9), random.randint(1, 9)
    answer = max(a, b)
    topic = _topic_for(1, ["수의 크기 비교"])
    prompt = f"{a}와 {b} 중 큰 수는?"
    return make(prompt, answer, topic, options=_choice_options(answer, [min(a, b), a + b, abs(a - b)]))


def _g1_pattern():
    start = random.randint(1, 5)
    answer = start + 4
    topic = _topic_for(1, ["규칙 찾기"])
    prompt = f"{start}, {start + 1}, {start + 2}, {start + 3}, ?"
    return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=4))


def _g1_picture_count():
    answer = random.randint(1, 9)
    topic = _topic_for(1, ["수 세기"])
    prompt = f"사과가 {answer}개 있습니다. 숫자로 쓰면?"
    return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=5))


# ============================================================
# 2학년: 받아올림/내림 없는 두 자리 수 덧셈·뺄셈, 구구단 준비
# ============================================================
def _g2_addition_no_carry():
    a = random.randint(11, 45)
    b = random.randint(11, 45)
    # 받아올림 없도록
    if (a % 10) + (b % 10) >= 10:
        a = (a // 10) * 10 + random.randint(1, 4)
        b = (b // 10) * 10 + random.randint(1, 5 - (a % 10))
    answer = a + b
    topic = _topic_for(2, ["수와 연산", "덧셈"])
    prompt = f"{a} + {b} = ?"
    return make(prompt, answer, topic, options=_distractors(answer, count=3, min_val=10, max_val=99, step=10))


def _g2_subtraction_no_borrow():
    a = random.randint(21, 89)
    b = random.randint(11, a - 1)
    # 받아내림 없도록
    if (a % 10) < (b % 10):
        temp = a % 10
        b = (b // 10) * 10 + temp - 1
    answer = a - b
    topic = _topic_for(2, ["수와 연산", "뺄셈"])
    prompt = f"{a} - {b} = ?"
    return make(prompt, answer, topic, options=_distractors(answer, count=3, min_val=0, max_val=80, step=5))


def _g2_multiplication_intro():
    a, b = random.randint(2, 5), random.randint(2, 5)
    answer = a * b
    topic = _topic_for(2, ["곱셈의 준비"])
    prompt = f"{a} 묶음씩 {b} 묶음이면 모두 몇 개인가요?"
    return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=10))


def _g2_time():
    hour = random.randint(1, 12)
    minute = random.choice([0, 15, 30, 45])
    topic = _topic_for(2, ["측정", "시간"])
    if minute == 0:
        prompt = f"{hour}시를 디지털 시계로 나타낸 시간은?"
        answer = f"{hour}:00"
    else:
        prompt = f"{hour}시 {minute}분을 디지털 시계로 나타낸 시간은?"
        answer = f"{hour}:{minute:02d}"
    distractors = [f"{hour}:{random.choice([5, 10, 20, 50]):02d}" for _ in range(3)]
    return make(prompt, answer, topic, options=_choice_options(answer, distractors))


# ============================================================
# 3학년: 구구단, 두 자리/세 자리 덧셈·뺄셈, 나눗셈 준비
# ============================================================
def _g3_multiplication_table():
    a, b = random.randint(2, 9), random.randint(2, 9)
    answer = a * b
    topic = _topic_for(3, ["수와 연산", "곱셈"])
    prompt = f"{a} × {b} = ?"
    return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=12))


def _g3_division_table():
    b = random.randint(2, 9)
    answer = random.randint(2, 9)
    a = b * answer
    topic = _topic_for(3, ["수와 연산", "나눗셈"])
    prompt = f"{a} ÷ {b} = ?"
    return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=10))


def _g3_addition_carry():
    a = random.randint(23, 89)
    b = random.randint(23, 89)
    answer = a + b
    topic = _topic_for(3, ["수와 연산", "덧셈"])
    prompt = f"{a} + {b} = ?"
    return make(prompt, answer, topic, question_type="write")


def _g3_subtraction_borrow():
    a = random.randint(50, 99)
    b = random.randint(21, a - 1)
    answer = a - b
    topic = _topic_for(3, ["수와 연산", "뺄셈"])
    prompt = f"{a} - {b} = ?"
    return make(prompt, answer, topic, question_type="write")


def _g3_shape_count():
    answer = random.randint(3, 8)
    topic = _topic_for(3, ["도형", "변화와 관계"])
    prompt = "삼각형이 3개, 사각형이 2개 있습니다. 도형은 모두 몇 개인가요?"
    return make(prompt, 5, topic, options=_arithmetic_choices(5, count=4, span=6))


# ============================================================
# 4학년: 세 자리/네 자리 덧셈·뺄셈, 두 자리 곱셈, 나눗셈, 평멸도형
# ============================================================
def _g4_addition_large():
    a = random.randint(123, 987)
    b = random.randint(123, 987)
    answer = a + b
    topic = _topic_for(4, ["수와 연산", "덧셈"])
    prompt = f"{a} + {b} = ?"
    return make(prompt, answer, topic, question_type="write")


def _g4_subtraction_large():
    a = random.randint(500, 1999)
    b = random.randint(123, a - 1)
    answer = a - b
    topic = _topic_for(4, ["수와 연산", "뺄셈"])
    prompt = f"{a} - {b} = ?"
    return make(prompt, answer, topic, question_type="write")


def _g4_multiplication_2digit():
    a = random.randint(12, 99)
    b = random.randint(2, 9)
    answer = a * b
    topic = _topic_for(4, ["수와 연산", "곱셈"])
    prompt = f"{a} × {b} = ?"
    return make(prompt, answer, topic, question_type="write")


def _g4_division_2digit():
    b = random.randint(2, 9)
    answer = random.randint(12, 99)
    a = b * answer
    topic = _topic_for(4, ["수와 연산", "나눗셈"])
    prompt = f"{a} ÷ {b} = ?"
    return make(prompt, answer, topic, question_type="write")


def _g4_factor_multiple():
    n = random.randint(2, 9)
    multiples = [n * i for i in range(1, 6)]
    answer = random.choice(multiples)
    topic = _topic_for(4, ["수와 연산", "배수와 약수"])
    prompt = f"{n}의 배수 중 하나를 고르세요."
    return make(prompt, answer, topic, options=_choice_options(answer, [answer + 1, answer + n, answer - 1]))


# ============================================================
# 5학년: 자연수 사칙연산, 분수/소수 덧셈·뺄셈, 평균, 넓이
# ============================================================
def _g5_large_mixed():
    a = random.randint(1000, 9999)
    b = random.randint(100, 999)
    c = random.randint(2, 9)
    topic = _topic_for(5, ["수와 연산", "사칙연산"])
    op = random.choice(["+", "-"])
    if op == "+":
        answer = a + b
        prompt = f"{a} + {b} = ?"
    else:
        answer = a - b
        prompt = f"{a} - {b} = ?"
    return make(prompt, answer, topic, question_type="write")


def _g5_fraction_add():
    a1 = random.randint(1, 3)
    a2 = random.randint(1, 3)
    b = random.randint(4, 9)
    num = a1 + a2
    answer = _format_fraction(num, b)
    topic = _topic_for(5, ["수와 연산", "분수"])
    prompt = f"{a1}/{b} + {a2}/{b} = ?"
    return make(prompt, answer, topic, options=_choice_options(answer, [_format_fraction(num + 1, b), _format_fraction(num - 1, b), _format_fraction(b, num)]))


def _g5_fraction_sub():
    a1 = random.randint(3, 7)
    a2 = random.randint(1, a1 - 1)
    b = random.randint(5, 9)
    num = a1 - a2
    answer = _format_fraction(num, b)
    topic = _topic_for(5, ["수와 연산", "분수"])
    prompt = f"{a1}/{b} - {a2}/{b} = ?"
    return make(prompt, answer, topic, options=_choice_options(answer, [_format_fraction(num + 1, b), _format_fraction(num - 1, b), _format_fraction(b, num)]))


def _g5_decimal_add():
    a = round(random.uniform(0.1, 9.9), 1)
    b = round(random.uniform(0.1, 9.9), 1)
    answer = round(a + b, 1)
    topic = _topic_for(5, ["수와 연산", "소수"])
    prompt = f"{a} + {b} = ?"
    return make(prompt, answer, topic, options=_distractors(round(answer, 1), count=3, step=1, exclude=[a, b]))


def _g5_average():
    nums = [random.randint(50, 99) for _ in range(3)]
    answer = sum(nums) // len(nums)
    topic = _topic_for(5, ["자료와 가능성", "평균"])
    prompt = f"{', '.join(map(str, nums))}의 평균은? (몫만 쓰세요)"
    return make(prompt, answer, topic, options=_distractors(answer, count=3, step=5))


# ============================================================
# 6학년: 분수/소수 곱셈·나눗셈, 비와 비율, 직육면체 부피/겉넓이
# ============================================================
def _g6_fraction_multiply():
    a = random.randint(1, 5)
    b = random.randint(2, 5)
    c = random.randint(2, 5)
    # (a/b) × c = (a×c)/b
    num = a * c
    answer = _format_fraction(num, b)
    topic = _topic_for(6, ["수와 연산", "분수의 곱셈"])
    prompt = f"{a}/{b} × {c} = ?"
    return make(prompt, answer, topic, options=_choice_options(answer, [_format_fraction(num + 1, b), _format_fraction(num - 1, b), _format_fraction(a + c, b)]))


def _g6_fraction_divide():
    a = random.randint(1, 5)
    b = random.randint(2, 5)
    c = random.randint(2, 5)
    # (a/b) ÷ c = a/(b×c)
    num = a
    den = b * c
    answer = _format_fraction(num, den)
    topic = _topic_for(6, ["수와 연산", "분수의 나눗셈"])
    prompt = f"{a}/{b} ÷ {c} = ?"
    return make(prompt, answer, topic, options=_choice_options(answer, [_format_fraction(num + 1, den), _format_fraction(num, den + 1), _format_fraction(a * c, b)]))


def _g6_ratio():
    a, b = random.randint(2, 8), random.randint(2, 8)
    answer = f"{a}:{b}"
    topic = _topic_for(6, ["변화와 관계", "비와 비율"])
    prompt = f"파란 공이 {a}개, 빨간 공이 {b}개일 때, 파란 공과 빨간 공의 개수 비는?"
    return make(prompt, answer, topic, options=_choice_options(answer, [f"{b}:{a}", f"{a+b}:{a}", f"{a}:{a+b}"]))


def _g6_volume():
    l, w, h = random.randint(2, 6), random.randint(2, 6), random.randint(2, 6)
    answer = l * w * h
    topic = _topic_for(6, ["도형과 측정", "직육면체의 부피"])
    prompt = f"가로 {l}cm, 세로 {w}cm, 높이 {h}cm인 직육면체의 부피는?"
    return make(prompt, answer, topic, options=_distractors(answer, count=3, step=l * w))


def _g6_percent():
    base = random.randint(100, 500)
    p = random.choice([10, 20, 25, 50])
    answer = base * p // 100
    topic = _topic_for(6, ["변화와 관계", "비율"])
    prompt = f"{base}의 {p}%는?"
    return make(prompt, answer, topic, options=_distractors(answer, count=3, step=10))


# ============================================================
# 중학년 (7~9): 기존 로직 유지 (앱이 초등 중심이므로 최소한으로)
# ============================================================
def _format_fraction(numerator, denominator):
    from math import gcd
    g = gcd(numerator, denominator)
    num, den = numerator // g, denominator // g
    if den == 1:
        return str(num)
    if num > den:
        return f"{num // den} {num % den}/{den}"
    return f"{num}/{den}"


def _g7_integer():
    a, b = random.randint(-9, 9), random.randint(-9, 9)
    op = random.choice(["+", "-"])
    answer = a + b if op == "+" else a - b
    topic = _topic_for(7, ["정수"])
    prompt = f"{a} {op} {b} = ?"
    return make(prompt, answer, topic, options=_distractors(answer, count=3, step=3))


def _g7_linear_equation():
    a = random.randint(2, 5)
    b = random.randint(1, 9)
    answer = random.randint(1, 9)
    c = a * answer + b
    topic = _topic_for(7, ["일차방정식"])
    prompt = f"{a}x + {b} = {c}일 때, x의 값은?"
    return make(prompt, answer, topic, options=_distractors(answer, count=3, step=1))


def _g7_coordinate():
    x, y = random.randint(-5, 5), random.randint(-5, 5)
    answer = f"({x}, {y})"
    topic = _topic_for(7, ["좌표평면"])
    prompt = f"좌표평면에서 x좌표가 {x}, y좌표가 {y}인 점의 좌표는?"
    return make(prompt, answer, topic, options=_choice_options(answer, [f"({y}, {x})", f"({-x}, {y})", f"({x}, {-y})"]))


def _g7_ratio_word():
    a, b = random.randint(2, 8), random.randint(2, 8)
    total = random.choice([20, 30, 40, 50])
    answer = total * a // (a + b)
    topic = _topic_for(7, ["비"])
    prompt = f"두 수의 비가 {a}:{b}이고 합이 {total}일 때, 큰 수는?"
    return make(prompt, answer, topic, options=_distractors(answer, count=3, step=total // 10))


PROBLEM_GENERATORS = {
    1: [_g1_addition, _g1_subtraction, _g1_compare, _g1_pattern, _g1_picture_count],
    2: [_g2_addition_no_carry, _g2_subtraction_no_borrow, _g2_multiplication_intro, _g2_time],
    3: [_g3_multiplication_table, _g3_division_table, _g3_addition_carry, _g3_subtraction_borrow, _g3_shape_count],
    4: [_g4_addition_large, _g4_subtraction_large, _g4_multiplication_2digit, _g4_division_2digit, _g4_factor_multiple],
    5: [_g5_large_mixed, _g5_fraction_add, _g5_fraction_sub, _g5_decimal_add, _g5_average],
    6: [_g6_fraction_multiply, _g6_fraction_divide, _g6_ratio, _g6_volume, _g6_percent],
    7: [_g7_integer, _g7_linear_equation, _g7_coordinate, _g7_ratio_word],
    8: [_g7_integer, _g7_linear_equation, _g7_coordinate, _g7_ratio_word],
    9: [_g7_integer, _g7_linear_equation, _g7_coordinate, _g7_ratio_word],
}


def generate_question(grade):
    generators = PROBLEM_GENERATORS.get(grade, PROBLEM_GENERATORS[9])
    return random.choice(generators)()


def generate_math_set(grade, count=10):
    generators = PROBLEM_GENERATORS.get(grade, PROBLEM_GENERATORS[9])
    questions = []
    seen = set()
    max_attempts = count * 30
    attempts = 0
    while len(questions) < count and attempts < max_attempts:
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
