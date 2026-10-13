import re


_ARITH = re.compile(
    r"(-?\d+(?:\.\d+)?(?:/\d+)?)\s*([+\-×÷])\s*(-?\d+(?:\.\d+)?(?:/\d+)?)"
)
_RATIO = re.compile(r"비가\s*(\d+)\s*:\s*(\d+).{0,12}합이\s*(\d+)")
_COUNTS = re.compile(r"([가-힣]+)이\s*(\d+)개")

TYPE_LABELS = {
    "write": "주관식",
    "choice": "객관식",
    "solution": "풀이형",
    "listening": "듣기",
    "speaking": "말하기",
}

TYPE_STEPS = {
    "choice": [
        "문제를 끝까지 읽고, 묻는 내용에 밑줄을 긋는다고 생각합니다.",
        "보기를 하나씩 문제 조건과 비교합니다. 맞는 것 같아도 나머지를 확인합니다.",
        "근거가 가장 분명한 보기 하나만 고릅니다.",
    ],
    "write": [
        "구하는 것이 무엇인지 먼저 정합니다.",
        "조건에 있는 수를 식이나 문장으로 옮깁니다.",
        "답을 적은 뒤, 그 답을 문제에 다시 넣어 맞는지 확인합니다.",
    ],
    "solution": [
        "주어진 조건과 구하는 것을 나누어 적습니다.",
        "풀이 과정을 건너뛰지 않고 순서대로 씁니다.",
        "마지막 줄에 ‘따라서 답은 …입니다.’라고 분명히 적습니다.",
    ],
    "listening": [
        "소리를 한 번 끝까지 듣습니다.",
        "다시 들으며 단어 사이를 띄어 적습니다.",
        "대소문자와 문장 부호를 빼고 뜻이 같은지 확인합니다.",
    ],
    "speaking": [
        "문장을 눈으로 한 번 읽습니다.",
        "끊어 읽을 곳에서 잠시 쉬며 소리 내어 말합니다.",
        "화면의 문장과 내가 말한 문장이 같은지 비교합니다.",
    ],
}


def type_label(question_type):
    return TYPE_LABELS.get(question_type, question_type or "문제")


def type_steps(question_type):
    return TYPE_STEPS.get(question_type, TYPE_STEPS["write"])


def detailed_explanation(prompt, answer, topic, note=None, subject="학습"):
    """문제, 풀이 순서, 검산이 함께 있는 설명을 만듭니다."""
    prompt = (prompt or "").strip()
    answer = "" if answer is None else str(answer)
    topic = topic or subject
    lines = [
        f"단원: {topic}",
        "1. 문제에서 구하는 것을 확인합니다.",
        f"   {prompt}",
    ]
    worked = _worked_steps(prompt, answer)
    if worked:
        lines.extend(worked)
    else:
        lines.append("2. 조건과 핵심 낱말을 찾아 근거를 정리합니다.")
        if note:
            lines.append(f"   {note}")
        lines.append(f"3. 정리한 근거로 답을 정하면 {answer}입니다.")
    lines.append(f"정답: {answer}")
    lines.append("확인: 적은 답이 문제의 조건과 단위에 맞는지 다시 읽어 보세요.")
    return "\n".join(lines)


def _worked_steps(prompt, answer):
    ratio = _RATIO.search(prompt)
    if ratio:
        a, b, total = (int(ratio.group(i)) for i in range(1, 4))
        share = total / (a + b)
        return [
            "2. 비의 앞항과 뒷항을 더해 전체를 몇 몫으로 나눌지 정합니다.",
            f"   {a} + {b} = {a + b}, 한 몫은 {total} ÷ {a + b} = {share:g}입니다.",
            f"3. 각 항에 한 몫을 곱합니다. {a} × {share:g} = {a * share:g}, {b} × {share:g} = {b * share:g}.",
            f"4. 두 수 가운데 큰 수를 고르면 {answer}입니다.",
        ]
    counts = _COUNTS.findall(prompt)
    if len(counts) >= 2 and "모두" in prompt:
        parts = [f"{name} {count}개" for name, count in counts]
        total = sum(int(count) for _, count in counts)
        return [
            "2. 종류별로 적힌 개수를 따로 확인합니다.",
            "   " + ", ".join(parts),
            f"3. 개수를 모두 더하면 {total}개입니다.",
        ]
    match = _ARITH.search(prompt)
    if not match:
        return []
    left, op, right = match.group(1), match.group(2), match.group(3)
    action = {"+": "더합니다", "-": "뺍니다", "×": "곱합니다", "÷": "나눕니다"}.get(op, "계산합니다")
    return [
        f"2. {left}과(와) {right}을(를) {action}.",
        f"   {left} {op} {right} = {answer}",
        "3. 계산 결과를 원래 식에 넣어 자리 수와 받아올림을 다시 확인합니다.",
    ]


def attempt_report(attempt):
    """결과 화면에 보여줄 맞은 수, 부분 점수, 단원별 기록을 모읍니다."""
    topics = {}
    correct = partial = missed = 0
    earned = possible = 0
    for item in attempt.items:
        name = item.topic or "기타"
        bucket = topics.setdefault(name, {"correct": 0, "total": 0, "points": 0, "max_points": 0})
        points = item.points or 0
        max_points = item.max_points or 0
        bucket["total"] += 1
        bucket["points"] += points
        bucket["max_points"] += max_points
        earned += points
        possible += max_points
        if item.is_correct:
            correct += 1
            bucket["correct"] += 1
        elif points > 0:
            partial += 1
        else:
            missed += 1
    return {
        "correct": correct,
        "partial": partial,
        "missed": missed,
        "total": len(attempt.items),
        "earned": earned,
        "possible": possible,
        "topics": [{"name": name, **stats} for name, stats in topics.items()],
    }
