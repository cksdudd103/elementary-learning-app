import re
from difflib import SequenceMatcher


def normalize_text(value):
    value = (value or "").lower().strip()
    value = re.sub(r"[^a-z0-9가-힣\s.\-]", "", value)
    return re.sub(r"\s+", " ", value).strip(" .")


def similarity(answer, expected):
    normalized_answer = normalize_text(answer)
    normalized_expected = normalize_text(expected)
    if not normalized_answer or not normalized_expected:
        return 0.0
    return SequenceMatcher(None, normalized_answer, normalized_expected).ratio()


def extract_keywords(text):
    """풀이형 답안의 핵심 키워드를 추출합니다."""
    text = normalize_text(text)
    # 불용어 제거
    stopwords = {"은", "는", "이", "가", "을", "를", "의", "에", "에서", "으로", "하고", "그리고", "하지만", "또는", "입니다", "있다", "있다"}
    words = [w for w in text.split() if w not in stopwords and len(w) >= 2]
    return set(words)


def grade_solution(answer, expected, max_points=15):
    """풀이형(서술형) 채점: 키워드 매칭으로 부분 점수를 줍니다."""
    if not answer or not answer.strip():
        return 0
    expected_keywords = extract_keywords(expected)
    if not expected_keywords:
        return max_points if len(answer.strip()) >= 5 else 0
    answer_keywords = extract_keywords(answer)
    matched = expected_keywords & answer_keywords
    ratio = len(matched) / len(expected_keywords)
    if ratio >= 0.7:
        return max_points
    if ratio >= 0.4:
        return max_points // 2
    if len(answer.strip()) >= 10 and ratio >= 0.2:
        return max_points // 3
    return 0


def grade_answer(answer, expected, question_type, grade_level, max_points=10):
    if question_type == "speaking":
        threshold = 0.72 if grade_level <= 4 else 0.8
        return max_points if similarity(answer, expected) >= threshold else 0
    if question_type == "solution":
        return grade_solution(answer, expected, max_points)
    if question_type == "choice":
        return max_points if normalize_text(answer) == normalize_text(expected) else 0
    return max_points if normalize_text(answer) == normalize_text(expected) else 0
