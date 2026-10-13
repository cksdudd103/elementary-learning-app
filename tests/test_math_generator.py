"""수학 문제 생성기가 문제와 맞는 정답을 만드는지 확인합니다."""

import re

from app.services.math_generator import (
    _g1_compare,
    _g1_subtraction,
    _g2_subtraction_no_borrow,
    _g3_shape_count,
    _g7_ratio_word,
    generate_question,
)


def _parse(prompt_expr):
    left, _ = prompt_expr.split("=")
    a_text, b_text = left.split("-")
    return int(a_text) - int(b_text)


def test_grade1_subtraction_is_non_negative(app):
    for _ in range(40):
        question = _g1_subtraction()
        assert _parse(question["prompt"]) == int(question["answer"])
        assert int(question["answer"]) >= 0
        assert question["answer"] in question["options"]


def test_grade1_compare_has_a_single_larger_number(app):
    for _ in range(40):
        question = _g1_compare()
        left, right = question["prompt"].split(" 중 ")[0].split("와 ")
        a, b = int(left), int(right)
        assert a != b
        assert int(question["answer"]) == max(a, b)


def test_grade2_subtraction_has_no_borrow(app):
    for _ in range(40):
        question = _g2_subtraction_no_borrow()
        a_text, b_text = question["prompt"].split("=")[0].split("-")
        a, b = int(a_text), int(b_text)
        assert a >= b
        assert a % 10 >= b % 10
        assert int(question["answer"]) == a - b


def test_shape_count_matches_the_prompt(app):
    for _ in range(20):
        question = _g3_shape_count()
        numbers = [int(number) for number in re.findall(r"\d+", question["prompt"])]
        assert int(question["answer"]) == sum(numbers)


def test_ratio_word_larger_part_sums_to_total(app):
    for _ in range(30):
        question = _g7_ratio_word()
        prompt = question["prompt"]
        ratio = prompt.split("비가 ")[1].split("이고")[0]
        a, b = [int(part) for part in ratio.split(":")]
        total = int(prompt.split("합이 ")[1].split("일")[0])
        part_a = total * a / (a + b)
        part_b = total * b / (a + b)
        assert part_a.is_integer() and part_b.is_integer()
        assert int(question["answer"]) == max(part_a, part_b)


def test_generate_question_keeps_semester(app):
    question = generate_question(3, semester=2, preferred_topics=["곱셈"])
    assert question["semester"] == 2
    assert "prompt" in question and "answer" in question
