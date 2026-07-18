import random
import urllib.parse


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
    """정답 근처의 적절한 오답을 만듭니다."""
    exclude = set(str(x) for x in (exclude or []))
    exclude.add(str(answer))
    candidates = set()
    attempts = 0
    span = max(step, abs(answer) + 10)
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
    # 부족하면 단순 오프셋 추가
    for delta in range(1, count * 5):
        if len(candidates) >= count:
            break
        for sign in (-1, 1):
            val = answer + sign * delta * step
            if str(val) not in exclude and (min_val is None or val >= min_val) and (max_val is None or val <= max_val):
                candidates.add(val)
                if len(candidates) >= count:
                    break
    return list(candidates)[:count]


def _arithmetic_choices(answer, count=4, span=10):
    return _choice_options(answer, _distractors(answer, count=count - 1, min_val=max(0, answer - span), max_val=answer + span))


def _svg_image(content, size="160x160", bg="white"):
    w, h = size.split("x")
    svg = f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' style='background:{bg};font-family:sans-serif'>{content}</svg>"
    return "data:image/svg+xml;utf8," + urllib.parse.quote(svg, safe="/:'=")


def _apple_svg(count, size="160x160"):
    w, h = size.split("x")
    if count == 0:
        content = f'<text x="{int(w)//2}" y="{int(h)//2}" font-size="48" text-anchor="middle" dominant-baseline="middle">0</text>'
    else:
        cols = 5 if count > 12 else 4
        rows = (count + cols - 1) // cols
        cell_w = int(w) // cols
        cell_h = int(h) // max(rows, 1)
        content = "".join(
            f'<text x="{(i % cols) * cell_w + cell_w // 2}" y="{(i // cols) * cell_h + cell_h // 2 + 10}" font-size="24" text-anchor="middle">🍎</text>'
            for i in range(count)
        )
    return _svg_image(content, size)


def _image_choices(answer_label, distractor_labels, size="160x160"):
    labels = [str(answer_label)] + [str(d) for d in distractor_labels]
    random.shuffle(labels)
    return [f"IMG|{_apple_svg(int(label), size)}|{label}" for label in labels]


def _fraction_svg(numerator, denominator, size="200x120"):
    w, h = size.split("x")
    bw, bh = 160, 40
    x0, y0 = (int(w) - bw) // 2, (int(h) - bh) // 2
    parts = []
    for i in range(denominator):
        color = "#ff9999" if i < numerator else "#eeeeee"
        parts.append(f'<rect x="{x0 + i * (bw // denominator)}" y="{y0}" width="{bw // denominator - 2}" height="{bh}" fill="{color}" stroke="#333"/>')
    content = "".join(parts) + f'<text x="{int(w)//2}" y="{y0 + bh + 30}" font-size="18" text-anchor="middle">{numerator}/{denominator}</text>'
    return _svg_image(content, size)


def _bar_graph_svg(title, data, size="300x200", unit=""):
    w, h = size.split("x")
    max_val = max(data.values()) if data else 1
    chart_h = 140
    chart_w = 240
    x0, y0 = 30, 10
    bars = []
    bar_w = chart_w // len(data) - 10
    for idx, (label, val) in enumerate(data.items()):
        bh = int((val / max_val) * chart_h) if max_val else 0
        x = x0 + idx * (bar_w + 10) + 5
        y = y0 + chart_h - bh
        bars.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{bh}" fill="#4a90d9" stroke="#333"/>')
        bars.append(f'<text x="{x + bar_w // 2}" y="{y0 + chart_h + 20}" font-size="12" text-anchor="middle">{label}</text>')
        bars.append(f'<text x="{x + bar_w // 2}" y="{y - 5}" font-size="12" text-anchor="middle">{val}{unit}</text>')
    axis = f'<line x1="{x0}" y1="{y0 + chart_h}" x2="{x0 + chart_w}" y2="{y0 + chart_h}" stroke="#333"/>'
    content = f'<text x="{int(w)//2}" y="25" font-size="14" text-anchor="middle">{title}</text>' + "".join(bars) + axis
    return _svg_image(content, size)


def _number_line_svg(points, labels, size="320x100"):
    w, h = size.split("x")
    y = 60
    start, end = min(points) - 1, max(points) + 1
    total = end - start
    x0, x1 = 20, int(w) - 20
    scale = (x1 - x0) / total
    ticks = []
    for i in range(start, end + 1):
        x = x0 + (i - start) * scale
        ticks.append(f'<line x1="{x}" y1="{y-5}" x2="{x}" y2="{y+5}" stroke="#333"/>')
        ticks.append(f'<text x="{x}" y="{y+25}" font-size="12" text-anchor="middle">{i}</text>')
    line = f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#333" stroke-width="2"/>'
    dots = []
    for val, label in zip(points, labels):
        x = x0 + (val - start) * scale
        color = "#e74c3c" if label == "?" else "#2ecc71"
        dots.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{color}" stroke="#333"/>')
        dots.append(f'<text x="{x}" y="{y-15}" font-size="12" text-anchor="middle">{label}</text>')
    content = line + "".join(ticks) + "".join(dots)
    return _svg_image(content, size)


def _format_fraction(numerator, denominator):
    return f"{numerator}/{denominator}"


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
    topics = _curriculum_topics("math", grade, fallback)
    return random.choice(topics)


# ───────────────────────────────
# 학년별 문제 생성기
# ───────────────────────────────

def _g1_addition_word():
    a, b = random.randint(2, 9), random.randint(1, 9)
    answer = a + b
    item = random.choice(["사과", "바나나", "공", "연필", "책", "자동차", "토끼", "꽃", "풍선", "과자"])
    topic = _topic_for(1, ["덧셈", "뺄셈", "수 비교"])
    prompt = f"{item}가 {a}개 있어요. 친구가 {b}개 더 주었어요. 모두 몇 개인가요?"
    qtype = random.choice(["choice", "write", "solution"])
    if qtype == "choice":
        return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=10))
    if qtype == "solution":
        return make(prompt, answer, topic, question_type="solution", explanation=f"{a} + {b} = {answer}이므로 {item}는 모두 {answer}개입니다.", max_points=15)
    return make(prompt, answer, topic, explanation=f"{a} + {b} = {answer}입니다.")


def _g1_subtraction_word():
    a, b = random.randint(5, 14), random.randint(1, 9)
    answer = a - b
    item = random.choice(["사과", "바나나", "연필", "풍선", "과자", "구슬", "스티커"])
    topic = _topic_for(1, ["덧셈", "뺄셈", "수 비교"])
    prompt = f"{item}가 {a}개 있었어요. {b}개를 먹었어요. 몇 개가 남았나요?"
    qtype = random.choice(["choice", "write"])
    if qtype == "choice":
        return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=10))
    return make(prompt, answer, topic, explanation=f"{a} - {b} = {answer}입니다.")


def _g1_compare():
    a, b = random.sample(range(1, 20), 2)
    topic = _topic_for(1, ["수 비교"])
    prompt = f"{a}와 {b} 중 어느 쪽이 더 큰가요?"
    answer = max(a, b)
    return make(prompt, answer, topic, options=_choice_options(answer, [min(a, b), abs(a - b), a + b]))


def _g1_pattern():
    start = random.randint(1, 5)
    step = random.randint(1, 3)
    seq = [start + step * i for i in range(4)]
    answer = start + step * 4
    topic = _topic_for(1, ["규칙 찾기"])
    prompt = f"규칙에 따라 다음 수를 쓰세요. {', '.join(map(str, seq))}, ?"
    return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=10))


def _g1_picture_count():
    answer = random.randint(1, 12)
    topic = _topic_for(1, ["수 비교", "덧셈과 뺄셈"])
    prompt = f"그림 속 사과가 {answer}개인 것을 고르세요."
    return make(prompt, answer, topic, options=_image_choices(answer, [answer + 1, answer - 1, answer + 2]))


def _g2_addition():
    a, b = random.randint(10, 99), random.randint(10, 99)
    answer = a + b
    topic = _topic_for(2, ["두 자리 수 연산", "덧셈과 뺄셈"])
    prompt = f"{a} + {b} = ?"
    qtype = random.choice(["choice", "write", "solution"])
    if qtype == "choice":
        return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=50))
    if qtype == "solution":
        return make(prompt, answer, topic, question_type="solution", max_points=15)
    return make(prompt, answer, topic)


def _g2_multiplication_word():
    a, b = random.randint(2, 9), random.randint(2, 9)
    answer = a * b
    topic = _topic_for(2, ["곱셈", "곱셈구구"])
    prompt = f"한 상자에 {a}개씩 {b}상자가 있어요. 모두 몇 개인가요?"
    qtype = random.choice(["choice", "write"])
    if qtype == "choice":
        return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=15))
    return make(prompt, answer, topic, explanation=f"{a} × {b} = {answer}입니다.")


def _g2_time():
    hour = random.randint(1, 11)
    minute = random.choice([0, 15, 30, 45])
    topic = _topic_for(2, ["시각"])
    prompt = f"시계가 {hour}시 {minute}분을 가리킬 때, 디지털 시계로 올바르게 표시한 것은?"
    answer = f"{hour:02d}:{minute:02d}"
    distractors = [f"{hour:02d}:{random.choice([0,15,30,45]):02d}" for _ in range(3)]
    return make(prompt, answer, topic, options=_choice_options(answer, distractors))


def _g2_length():
    cm = random.randint(20, 95)
    topic = _topic_for(2, ["길이"])
    prompt = f"{cm}cm는 몇 cm 몇 mm인가요? (예: 34cm 5mm)"
    answer = f"{cm}cm 0mm"
    return make(prompt, answer, topic)


def _g3_multiplication():
    a, b = random.randint(12, 99), random.randint(2, 9)
    answer = a * b
    topic = _topic_for(3, ["곱셈", "나눗셈"])
    prompt = f"{a} × {b} = ?"
    qtype = random.choice(["choice", "write", "solution"])
    if qtype == "choice":
        return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=100))
    if qtype == "solution":
        return make(prompt, answer, topic, question_type="solution", max_points=15)
    return make(prompt, answer, topic)


def _g3_division_word():
    b = random.randint(2, 9)
    answer = random.randint(3, 15)
    a = b * answer
    topic = _topic_for(3, ["나눗셈"])
    prompt = f"{a}개의 사탕을 {b}명이 똑같이 나누면 한 명당 몇 개인가요?"
    qtype = random.choice(["choice", "write"])
    if qtype == "choice":
        return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=10))
    return make(prompt, answer, topic, explanation=f"{a} ÷ {b} = {answer}입니다.")


def _g3_fraction_visual():
    numerator = random.randint(1, 3)
    denominator = random.randint(numerator + 1, 6)
    topic = _topic_for(3, ["분수"])
    answer = _format_fraction(numerator, denominator)
    prompt = f"색칠된 부분을 분수로 나타내세요."
    image_url = _fraction_svg(numerator, denominator)
    return make(prompt, answer, topic, image_url=image_url, options=_choice_options(answer, [
        _format_fraction(numerator + 1, denominator),
        _format_fraction(numerator, denominator + 1),
        _format_fraction(denominator, numerator),
    ]))


def _g3_perimeter():
    width = random.randint(3, 12)
    height = random.randint(3, 12)
    answer = 2 * (width + height)
    topic = _topic_for(3, ["도형의 둘레"])
    prompt = f"가로 {width}cm, 세로 {height}cm인 직사각형의 둘레는 몇 cm인가요?"
    qtype = random.choice(["choice", "write"])
    if qtype == "choice":
        return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=20))
    return make(prompt, answer, topic, explanation=f"({width} + {height}) × 2 = {answer}cm입니다.")


def _g4_large_multiply():
    a, b = random.randint(100, 999), random.randint(10, 99)
    answer = a * b
    topic = _topic_for(4, ["곱셈", "나눗셈"])
    prompt = f"{a} × {b} = ?"
    qtype = random.choice(["choice", "write", "solution"])
    if qtype == "choice":
        return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=5000))
    if qtype == "solution":
        return make(prompt, answer, topic, question_type="solution", max_points=15)
    return make(prompt, answer, topic)


def _g4_division_large():
    b = random.randint(10, 99)
    answer = random.randint(10, 50)
    a = b * answer
    topic = _topic_for(4, ["나눗셈"])
    prompt = f"{a} ÷ {b} = ?"
    return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=20))


def _g4_decimal():
    a = round(random.uniform(0.1, 9.9), 1)
    b = round(random.uniform(0.1, 9.9), 1)
    answer = round(a + b, 1)
    topic = _topic_for(4, ["소수"])
    prompt = f"{a} + {b} = ?"
    return make(prompt, answer, topic, options=_choice_options(answer, [
        round(answer + 0.1, 1), round(answer - 0.1, 1), round(answer + 1, 1)
    ]))


def _g4_factor_multiple():
    number = random.randint(12, 48)
    topic = _topic_for(4, ["약수와 배수"])
    if random.choice([True, False]):
        divisors = [d for d in range(1, number + 1) if number % d == 0]
        answer = ",".join(map(str, divisors))
        prompt = f"{number}의 약수를 작은 수부터 쉼표로 모두 쓰세요."
    else:
        multiples = [number * i for i in range(1, 6)]
        answer = ",".join(map(str, multiples))
        prompt = f"{number}의 배수 5개를 작은 수부터 쉼표로 쓰세요."
    return make(prompt, answer, topic)


def _g5_gcf_lcm():
    a, b = random.sample(range(6, 36), 2)
    topic = _topic_for(5, ["약수와 배수"])
    if random.choice([True, False]):
        # 최대공약수
        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x
        answer = gcd(a, b)
        prompt = f"{a}와 {b}의 최대공약수는?"
    else:
        def lcm(x, y):
            def gcd(a, b):
                while b:
                    a, b = b, a % b
                return a
            return x * y // gcd(x, y)
        answer = lcm(a, b)
        prompt = f"{a}와 {b}의 최소공배수는?"
    return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=max(answer, 20)))


def _g5_fraction_calc():
    ops = random.choice(["+", "-"])
    topic = _topic_for(5, ["분수의 덧셈과 뺄셈"])
    if ops == "+":
        a1, a2 = random.randint(1, 3), random.randint(1, 3)
        b = random.randint(4, 9)
        num = a1 + a2
        answer = _format_fraction(num, b)
        prompt = f"{a1}/{b} + {a2}/{b} = ?"
    else:
        a1, a2 = random.randint(3, 7), random.randint(1, a1 - 1)
        b = random.randint(5, 9)
        answer = _format_fraction(a1 - a2, b)
        prompt = f"{a1}/{b} - {a2}/{b} = ?"
    return make(prompt, answer, topic, options=_choice_options(answer, [
        _format_fraction(num + 1, b) if ops == "+" else _format_fraction(a1 - a2 + 1, b),
        _format_fraction(num - 1, b) if ops == "+" else _format_fraction(a1 - a2 - 1, b),
        _format_fraction(b, num) if ops == "+" else _format_fraction(b, a1 - a2),
    ]))


def _g5_area():
    shape = random.choice(["rectangle", "triangle", "parallelogram"])
    topic = _topic_for(5, ["넓이와 둘레"])
    if shape == "rectangle":
        w, h = random.randint(3, 20), random.randint(3, 20)
        answer = w * h
        prompt = f"가로 {w}cm, 세로 {h}cm인 직사각형의 넓이는?"
    elif shape == "triangle":
        b, h = random.randint(4, 20), random.randint(4, 20)
        answer = b * h // 2
        prompt = f"밑변 {b}cm, 높이 {h}cm인 삼각형의 넓이는?"
    else:
        b, h = random.randint(4, 20), random.randint(4, 20)
        answer = b * h
        prompt = f"밑변 {b}cm, 높이 {h}cm인 평행사변형의 넓이는?"
    return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=max(20, answer // 2)))


def _g5_average():
    count = random.randint(3, 5)
    nums = [random.randint(60, 100) for _ in range(count)]
    answer = sum(nums) // count
    topic = _topic_for(5, ["평균"])
    prompt = f"{', '.join(map(str, nums))}의 평균은? (몫만 쓰세요)"
    return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=20))


def _g6_ratio():
    total = random.choice([100, 200, 300, 400])
    percent = random.choice([10, 20, 25, 30, 40, 50, 75])
    answer = total * percent // 100
    topic = _topic_for(6, ["비와 비율"])
    prompt = f"{total}명 중 {percent}%가 도서관을 이용한다면 몇 명인가요?"
    return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=50))


def _g6_equation():
    coefficient = random.randint(2, 9)
    answer = random.randint(2, 15)
    constant = random.randint(1, 20)
    left = coefficient * answer + constant
    topic = _topic_for(6, ["방정식"])
    prompt = f"{coefficient}x + {constant} = {left}일 때 x의 값은?"
    qtype = random.choice(["choice", "write", "solution"])
    if qtype == "choice":
        return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=10))
    if qtype == "solution":
        return make(prompt, answer, topic, question_type="solution", explanation=f"양변에서 {constant}을 빼고 {coefficient}로 나누면 x = {answer}입니다.", max_points=15)
    return make(prompt, answer, topic)


def _g6_circle():
    r = random.randint(2, 10)
    topic = _topic_for(6, ["원"])
    if random.choice([True, False]):
        answer = 2 * r * 3
        prompt = f"반지름이 {r}cm인 원의 둘레를 구하세요. (원주율을 3으로 계산)"
    else:
        answer = r * r * 3
        prompt = f"반지름이 {r}cm인 원의 넓이를 구하세요. (원주율을 3으로 계산)"
    return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=30))


def _g6_volume():
    l, w, h = random.randint(2, 10), random.randint(2, 10), random.randint(2, 10)
    answer = l * w * h
    topic = _topic_for(6, ["부피"])
    prompt = f"가로 {l}cm, 세로 {w}cm, 높이 {h}cm인 직육면체의 부피는?"
    return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=50))


def _g7_integer():
    a, b = random.randint(-20, 20), random.randint(-20, 20)
    op = random.choice(["+", "-"])
    topic = _topic_for(7, ["정수와 유리수"])
    if op == "+":
        answer = a + b
        prompt = f"({a}) + ({b}) = ?"
    else:
        answer = a - b
        prompt = f"({a}) - ({b}) = ?"
    return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=20))


def _g7_linear_equation():
    a = random.randint(2, 9)
    answer = random.randint(-10, 15)
    b = random.randint(-15, 15)
    c = a * answer + b
    topic = _topic_for(7, ["일차방정식"])
    prompt = f"{a}x + ({b}) = {c}일 때 x의 값은?"
    qtype = random.choice(["choice", "write", "solution"])
    if qtype == "choice":
        return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=15))
    if qtype == "solution":
        return make(prompt, answer, topic, question_type="solution", max_points=15)
    return make(prompt, answer, topic)


def _g7_coordinate():
    x, y = random.randint(-5, 5), random.randint(-5, 5)
    answer = f"({x},{y})"
    topic = _topic_for(7, ["좌표평면"])
    prompt = f"x좌표가 {x}이고 y좌표가 {y}인 점의 좌표를 쓰세요. (예: (3,-2))"
    distractors = [f"({y},{x})", f"({-x},{y})", f"({x},{-y})"]
    return make(prompt, answer, topic, options=_choice_options(answer, distractors))


def _g7_ratio_word():
    a, b = random.randint(2, 8), random.randint(2, 8)
    total = a + b
    scale = random.randint(2, 5)
    answer = a * scale
    topic = _topic_for(7, ["비와 비율"])
    prompt = f"두 수의 비가 {a}:{b}이고, 두 수의 합이 {total * scale}일 때 작은 수는?"
    return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=20))


def _g8_system():
    x, y = random.randint(1, 9), random.randint(1, 9)
    a, b = random.randint(1, 5), random.randint(1, 5)
    c1 = a * x + b * y
    c2 = a * x - b * y
    topic = _topic_for(8, ["연립방정식"])
    answer = x
    prompt = f"{a}x + {b}y = {c1}, {a}x - {b}y = {c2}일 때 x의 값은?"
    qtype = random.choice(["choice", "write", "solution"])
    if qtype == "choice":
        return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=5))
    if qtype == "solution":
        return make(prompt, answer, topic, question_type="solution", explanation=f"두 식을 더하면 2×{a}x = {2*c1}, x = {answer}입니다.", max_points=15)
    return make(prompt, answer, topic)


def _g8_linear_function():
    m = random.randint(-4, 5)
    while m == 0:
        m = random.randint(-4, 5)
    b = random.randint(-5, 5)
    x = random.randint(-3, 5)
    answer = m * x + b
    topic = _topic_for(8, ["일차함수"])
    prompt = f"y = {m}x + ({b})에서 x = {x}일 때 y의 값은?"
    return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=15))


def _g8_probability():
    total = random.randint(6, 20)
    target = random.randint(1, total - 1)
    topic = _topic_for(8, ["확률"])
    prompt = f"{total}개의 공 중 {target}개가 빨간색입니다. 빨간색 공을 하나 뽑을 확률은? (분수로)"
    answer = _format_fraction(target, total)
    return make(prompt, answer, topic, options=_choice_options(answer, [
        _format_fraction(target + 1, total),
        _format_fraction(target, total + 1),
        _format_fraction(total - target, total),
    ]))


def _g8_pythagorean():
    a, b = random.randint(3, 12), random.randint(3, 12)
    answer = a * a + b * b
    topic = _topic_for(8, ["피타고라스 정리"])
    prompt = f"직각삼각형의 두 변의 길이가 각각 {a}cm, {b}cm일 때 빗변의 제곱은?"
    return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=30))


def _g9_radical():
    n = random.randint(2, 15)
    answer = n
    topic = _topic_for(9, ["제곱근"])
    prompt = f"√{n * n} = ?"
    return make(prompt, answer, topic, options=_arithmetic_choices(answer, count=4, span=10))


def _g9_quadratic_equation():
    p, q = random.randint(1, 10), random.randint(1, 10)
    answer = f"{min(p, q)},{max(p, q)}"
    topic = _topic_for(9, ["이차방정식"])
    prompt = f"x² - {p + q}x + {p * q} = 0의 두 근을 작은 수부터 쉼표로 쓰세요."
    return make(prompt, answer, topic, options=_choice_options(answer, [
        f"{max(p, q)},{min(p, q)}",
        f"{-p},{-q}",
        f"{p},{q}",
    ]))


def _g9_quadratic_function():
    a = random.randint(1, 3)
    h, k = random.randint(-3, 3), random.randint(-5, 5)
    answer = f"({h},{k})"
    topic = _topic_for(9, ["이차함수"])
    prompt = f"y = {a}(x - {h})² + {k}의 꼭짓점 좌표를 쓰세요. (예: (2,-3))"
    return make(prompt, answer, topic, options=_choice_options(answer, [
        f"({-h},{k})", f"({h},{-k})", f"({-h},{-k})",
    ]))


def _g9_trigonometry():
    angle = random.choice([30, 45, 60])
    topic = _topic_for(9, ["삼각비"])
    if angle == 30:
        answer = "1/2"
        prompt = "sin 30°의 값은?"
    elif angle == 45:
        answer = "√2/2"
        prompt = "sin 45°의 값은?"
    else:
        answer = "√3/2"
        prompt = "sin 60°의 값은?"
    return make(prompt, answer, topic, options=_choice_options(answer, ["0", "1", "√3/3"]))


PROBLEM_GENERATORS = {
    1: [_g1_addition_word, _g1_subtraction_word, _g1_compare, _g1_pattern, _g1_picture_count],
    2: [_g2_addition, _g2_multiplication_word, _g2_time, _g2_length],
    3: [_g3_multiplication, _g3_division_word, _g3_fraction_visual, _g3_perimeter],
    4: [_g4_large_multiply, _g4_division_large, _g4_decimal, _g4_factor_multiple],
    5: [_g5_gcf_lcm, _g5_fraction_calc, _g5_area, _g5_average],
    6: [_g6_ratio, _g6_equation, _g6_circle, _g6_volume],
    7: [_g7_integer, _g7_linear_equation, _g7_coordinate, _g7_ratio_word],
    8: [_g8_system, _g8_linear_function, _g8_probability, _g8_pythagorean],
    9: [_g9_radical, _g9_quadratic_equation, _g9_quadratic_function, _g9_trigonometry],
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
    # 유일성 확보가 어려우면 중복 허용
    while len(questions) < count:
        questions.append(random.choice(generators)())
    random.shuffle(questions)
    return questions
