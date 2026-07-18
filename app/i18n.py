from flask import session
from flask_login import current_user

MESSAGES = {
    "ko": {
        "app_name": "하루쑥쑥",
        "dashboard": "학습 홈",
        "math": "수학",
        "english": "영어",
        "korean": "국어",
        "social": "사회",
        "history": "학습 기록",
        "wrong_answers": "오답 노트",
        "admin": "관리자",
        "logout": "로그아웃",
        "login": "로그인",
        "register": "회원가입",
        "start": "10문제 시작",
        "review": "복습하기",
        "submit": "제출하고 채점하기",
        "score": "점수",
        "correct": "정답",
        "your_answer": "내 답",
    },
    "en": {
        "app_name": "Daily Grow",
        "dashboard": "Learning Home",
        "math": "Math",
        "english": "English",
        "korean": "Korean",
        "social": "Social Studies",
        "history": "History",
        "wrong_answers": "Wrong Answers",
        "admin": "Admin",
        "logout": "Log out",
        "login": "Log in",
        "register": "Sign up",
        "start": "Start 10 Questions",
        "review": "Review",
        "submit": "Submit and Grade",
        "score": "Score",
        "correct": "Answer",
        "your_answer": "Your answer",
    },
}


def get_locale():
    if current_user.is_authenticated:
        return current_user.ui_language
    return session.get("language", "ko")


def translate(key):
    language = get_locale()
    return MESSAGES.get(language, MESSAGES["ko"]).get(key, key)