"""초기 데이터 시드: 전국 시도교육청, 샘플 학교, 학년별 교육과정 단원"""

from app.extensions import db
from app.models import EducationOffice, School, CurriculumUnit


EDUCATION_OFFICES = [
    ("서울특별시교육청", "서울", "서울특별시 중구 세종대로 110", "02-399-1000", "https://www.sen.go.kr"),
    ("부산광역시교육청", "부산", "부산광역시 연제구 중앙대로 1001", "051-860-0100", "https://www.pen.go.kr"),
    ("대구광역시교육청", "대구", "대구광역시 중구 중앙대로 419", "053-230-1000", "https://www.dge.go.kr"),
    ("인천광역시교육청", "인천", "인천광역시 남동구 정각로 206", "032-423-2800", "https://www.ice.go.kr"),
    ("광주광역시교육청", "광주", "광주광역시 서구 금화로 210", "062-380-0114", "https://www.gen.go.kr"),
    ("대전광역시교육청", "대전", "대전광역시 서구 둔산로 169", "042-600-7300", "https://www.dje.go.kr"),
    ("울산광역시교육청", "울산", "울산광역시 남구 삼산로 218", "052-250-3000", "https://www.use.go.kr"),
    ("세종특별자치시교육청", "세종", "세종특별자치시 조치원읍 교육원로 9", "044-320-1300", "https://www.sje.go.kr"),
    ("경기도교육청", "경기", "경기도 수원시 팔달구 매산로1가 60", "031-249-0114", "https://www.goe.go.kr"),
    ("강원특별자치도교육청", "강원", "강원특별자치도 춘천시 중앙로 183", "033-250-3100", "https://www.gwe.go.kr"),
    ("충청북도교육청", "충북", "충청북도 청주시 상당구 중고개로 336", "043-290-5000", "https://www.cbe.go.kr"),
    ("충청남도교육청", "충남", "충청남도 홍성군 홍북면 충남대로 21", "041-620-3000", "https://www.cne.go.kr"),
    ("전북특별자치도교육청", "전북", "전북특별자치도 전주시 완산구 교육로 236", "063-239-1000", "https://www.jbe.go.kr"),
    ("전라남도교육청", "전남", "전라남도 무안군 삼향읍 오룡길 1", "061-280-3000", "https://www.jne.go.kr"),
    ("경상북도교육청", "경북", "경상북도 안동시 풍천면 도청대로 455", "054-880-2000", "https://www.gbe.go.kr"),
    ("경상남도교육청", "경남", "경상남도 창원시 의창구 중앙대로 300", "055-250-3000", "https://www.gne.go.kr"),
    ("제주특별자치도교육청", "제주", "제주특별자치도 제주시 제주동로 74", "064-800-3000", "https://www.jje.go.kr"),
]

SAMPLE_SCHOOLS = [
    # (region, name, type)
    ("서울", "서울교대부설초등학교", "elementary"),
    ("서울", "서울교대부설중학교", "middle"),
    ("서울", "경기고등학교", "high"),
    ("부산", "부산초등학교", "elementary"),
    ("부산", "부산중학교", "middle"),
    ("대구", "대구초등학교", "elementary"),
    ("대구", "대구중학교", "middle"),
    ("인천", "인천초등학교", "elementary"),
    ("인천", "인천중학교", "middle"),
    ("광주", "광주초등학교", "elementary"),
    ("대전", "대전초등학교", "elementary"),
    ("울산", "울산초등학교", "elementary"),
    ("세종", "세종초등학교", "elementary"),
    ("경기", "경기초등학교", "elementary"),
    ("경기", "경기중학교", "middle"),
    ("강원", "강원초등학교", "elementary"),
    ("충북", "충북초등학교", "elementary"),
    ("충남", "충남초등학교", "elementary"),
    ("전북", "전북초등학교", "elementary"),
    ("전남", "전남초등학교", "elementary"),
    ("경북", "경북초등학교", "elementary"),
    ("경남", "경남초등학교", "elementary"),
    ("제주", "제주초등학교", "elementary"),
]

# (학년, 단원번호, 단원명, 학습목표, 키워드)
MATH_UNITS = {
    1: [
        ("1. 9까지의 수", "9까지의 수를 읽고 쓰고 비교할 수 있다.", "수 비교"),
        ("2. 덧셈과 뺄셈", "20 이하의 덧셈과 뺄셈을 할 수 있다.", "덧셈 뺄셈"),
        ("3. 모양", "여러 가지 모양을 알아보고 분류할 수 있다.", "도형"),
    ],
    2: [
        ("1. 세 자리 수", "세 자리 수를 읽고 쓰고 비교할 수 있다.", "수 비교"),
        ("2. 두 자리 덧셈과 뺄셈", "두 자리 수의 덧셈과 뺄셈을 할 수 있다.", "덧셈 뺄셈"),
        ("3. 평멸도형", "삼각형, 사각형, 원을 알아본다.", "도형"),
    ],
    3: [
        ("1. 곱셈", "구구단을 이용하여 곱셈을 할 수 있다.", "곱셈"),
        ("2. 나눗셈", "나눗셈의 의미와 계산을 할 수 있다.", "나눗셈"),
        ("3. 분수", "분수의 의미와 크기를 비교할 수 있다.", "분수"),
    ],
    4: [
        ("1. 큰 수", "억 단위까지의 수를 읽고 쓸 수 있다.", "큰 수"),
        ("2. 곱셈과 나눗셈", "두 자리 수의 곱셈과 나눗셈을 할 수 있다.", "곱셈 나눗셈"),
        ("3. 분수와 소수", "분수와 소수의 관계를 이해한다.", "분수 소수"),
    ],
    5: [
        ("1. 약수와 배수", "약수와 배수, 공약수, 공배수를 이해한다.", "약수 배수"),
        ("2. 분수의 덧셈과 뺄셈", "분수의 덧셈과 뺄셈을 할 수 있다.", "분수 연산"),
        ("3. 다각형의 넓이", "삼각형, 사다리꼴, 평행사변형의 넓이를 구한다.", "넓이"),
    ],
    6: [
        ("1. 분수의 나눗셈", "분수의 나눗셈을 할 수 있다.", "분수 나눗셈"),
        ("2. 비와 비율", "비와 비율을 이해하고 활용한다.", "비 비율"),
        ("3. 원의 넓이와 둘레", "원의 넓이와 둘레를 구할 수 있다.", "원"),
    ],
    7: [
        ("1. 정수와 유리수", "정수와 유리수를 이해한다.", "정수 유리수"),
        ("2. 문자와 식", "문자를 사용하여 식을 세우고 계산한다.", "식"),
        ("3. 일차방정식", "일차방정식을 풀 수 있다.", "방정식"),
    ],
    8: [
        ("1. 식의 계산", "다항식의 덧셈, 뺄셈, 곱셈을 할 수 있다.", "다항식"),
        ("2. 연립방정식", "연립방정식을 풀 수 있다.", "연립방정식"),
        ("3. 일차함수", "일차함수의 그래프와 성질을 이해한다.", "함수"),
    ],
    9: [
        ("1. 제곱근과 실수", "제곱근과 실수를 이해한다.", "제곱근"),
        ("2. 인수분해", "다항식을 인수분해할 수 있다.", "인수분해"),
        ("3. 이차방정식", "이차방정식을 풀 수 있다.", "이차방정식"),
    ],
}

KOREAN_UNITS = {
    1: [
        ("1. 듣기·말하기", "바른 말과 예의 바른 말하기", "인사 말하기"),
        ("2. 쓰기", "글자의 기본 획과 모양", "글씨"),
    ],
    2: [
        ("1. 듣기·말하기", "듣기 예절과 이야기 나누기", "대화"),
        ("2. 읽기", "낱말과 문장 읽기", "문장"),
    ],
    3: [
        ("1. 문학", "동시와 이야기 감상", "동화"),
        ("2. 문법", "문장의 성분과 품사", "품사"),
    ],
    4: [
        ("1. 문학", "시와 산문 읽기", "시"),
        ("2. 쓰기", "글의 구조와 문단", "문단"),
    ],
    5: [
        ("1. 문법", "효음과 어미", "어미"),
        ("2. 문학", "고전 소설과 현대 소설", "소설"),
    ],
    6: [
        ("1. 문학", "수필과 극", "수필"),
        ("2. 문법", "문장 부호와 띄어쓰기", "맞춤법"),
    ],
    7: [
        ("1. 문학", "현대 시와 산문", "현대시"),
        ("2. 문법", "품사와 문장 성분", "문장성분"),
    ],
    8: [
        ("1. 문학", "고전 산문과 시", "고전"),
        ("2. 쓰기", "논술문 쓰기", "논술"),
    ],
    9: [
        ("1. 문학", "문학의 다양한 주제", "문학"),
        ("2. 문법", "담화와 화법", "화법"),
    ],
}

SOCIAL_UNITS = {
    1: [
        ("1. 우리 가족과 학교", "가족과 학교 생활의 중요성", "가족 학교"),
        ("2. 우리 동네", "지역 사회의 모습", "동네"),
    ],
    2: [
        ("1. 우리나라의 자연", "계절과 지형", "자연"),
        ("2. 전통 문화", "우리 전통과 문화", "전통"),
    ],
    3: [
        ("1. 지리", "우리나라의 지역", "지역"),
        ("2. 역사", "고조선과 삼국시대", "역사"),
    ],
    4: [
        ("1. 지리", "기후와 산업", "기후 산업"),
        ("2. 역사", "고려와 조선", "고려 조선"),
    ],
    5: [
        ("1. 역사", "근대 한국의 변화", "근대"),
        ("2. 사회·정치", "민주주의와 헌법", "민주주의"),
    ],
    6: [
        ("1. 역사", "현대 한국", "현대"),
        ("2. 경제", "시장과 경제", "경제"),
    ],
    7: [
        ("1. 역사", "인류 문명", "문명"),
        ("2. 지리", "세계의 다양한 지역", "세계"),
    ],
    8: [
        ("1. 역사", "근대 국가 형성", "근대국가"),
        ("2. 사회·정치", "권력과 시민", "시민"),
    ],
    9: [
        ("1. 역사", "근현대 세계", "근현대"),
        ("2. 사회·정치", "국제 사회", "국제"),
    ],
}

ENGLISH_UNITS = {
    1: [
        ("1. Hello!", "인사와 자기소개", "greeting self-introduction"),
        ("2. My Family", "가족 소개", "family"),
    ],
    2: [
        ("1. My School", "학교 생활 표현", "school"),
        ("2. My Day", "하루 일과", "daily routine"),
    ],
    3: [
        ("1. My Hobby", "취미 표현", "hobby"),
        ("2. My Favorite Food", "음식 표현", "food"),
    ],
    4: [
        ("1. Where Are You?", "장소와 방향", "place direction"),
        ("2. My Weekend", "과거 경험", "past experience"),
    ],
    5: [
        ("1. My Future", "미래 계획", "future plan"),
        ("2. Our Earth", "지구와 환경", "environment"),
    ],
    6: [
        ("1. My Dream", "직업과 꿈", "dream job"),
        ("2. Around the World", "세계 문화", "world culture"),
    ],
    7: [
        ("1. Me and My Friends", "성격과 외모", "personality appearance"),
        ("2. Healthy Life", "건강과 생활", "health"),
    ],
    8: [
        ("1. Inventions", "발명과 과학", "invention"),
        ("2. Our Traditions", "전통과 문화", "tradition"),
    ],
    9: [
        ("1. Communication", "의사소통 방법", "communication"),
        ("2. Our Future", "미래 사회", "future society"),
    ],
}


def seed_education_offices():
    if EducationOffice.query.first():
        return
    for name, region, address, phone, homepage in EDUCATION_OFFICES:
        db.session.add(EducationOffice(
            name=name, region=region, address=address, phone=phone, homepage=homepage
        ))
    db.session.commit()


def seed_schools():
    if School.query.first():
        return
    office_map = {office.region: office.id for office in EducationOffice.query.all()}
    for region, name, school_type in SAMPLE_SCHOOLS:
        if region not in office_map:
            continue
        db.session.add(School(
            education_office_id=office_map[region],
            name=name,
            school_type=school_type,
            homepage="",
        ))
    db.session.commit()


def seed_curriculum_units():
    if CurriculumUnit.query.first():
        return
    for grade, units in MATH_UNITS.items():
        for order, (name, objective, keywords) in enumerate(units, start=1):
            db.session.add(CurriculumUnit(
                subject="math", grade_level=grade, unit_order=order,
                unit_name=name, learning_objective=objective, keywords=keywords
            ))
    for grade, units in KOREAN_UNITS.items():
        for order, (name, objective, keywords) in enumerate(units, start=1):
            db.session.add(CurriculumUnit(
                subject="korean", grade_level=grade, unit_order=order,
                unit_name=name, learning_objective=objective, keywords=keywords
            ))
    for grade, units in SOCIAL_UNITS.items():
        for order, (name, objective, keywords) in enumerate(units, start=1):
            db.session.add(CurriculumUnit(
                subject="social", grade_level=grade, unit_order=order,
                unit_name=name, learning_objective=objective, keywords=keywords
            ))
    for grade, units in ENGLISH_UNITS.items():
        for order, (name, objective, keywords) in enumerate(units, start=1):
            db.session.add(CurriculumUnit(
                subject="english", grade_level=grade, unit_order=order,
                unit_name=name, learning_objective=objective, keywords=keywords
            ))
    db.session.commit()


def seed_all():
    seed_education_offices()
    seed_schools()
    seed_curriculum_units()
    print("Seed data inserted.")


if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_all()
