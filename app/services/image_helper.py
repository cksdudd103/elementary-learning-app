import base64 as _base64


def _svg_data_uri(svg_body):
    encoded = _base64.b64encode(svg_body.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def placeholder_image(text, color="#4a7c59", bg="#eef5f0", width=120, height=120):
    """주어진 텍스트와 색상으로 SVG 플레이스홀더 이미지 URL을 만듭니다."""
    safe_text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # 긴 텍스트는 줄바꿈
    lines = []
    if len(safe_text) > 8:
        for i in range(0, len(safe_text), 8):
            lines.append(safe_text[i:i + 8])
    else:
        lines = [safe_text]
    if len(lines) > 3:
        lines = lines[:2] + ["..."]
    line_height = 18
    start_y = (height - len(lines) * line_height) // 2 + 14
    text_elements = "\n".join(
        f'<text x="{width // 2}" y="{start_y + i * line_height}" text-anchor="middle" fill="{color}" font-size="16" font-family="sans-serif">{line}</text>'
        for i, line in enumerate(lines)
    )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"'>
        f'<rect width="{width}" height="{height}" rx="16" fill="{bg}"/>'
        f'{text_elements}'
        f'</svg>'
    )
    return _svg_data_uri(svg)


def topic_image(topic, width=200, height=140):
    """과목 주제에 맞는 색상의 플레이스홀더 이미지를 만듭니다."""
    colors = {
        "수": ("#2b4c8c", "#e1e9ff"),
        "계산": ("#2b4c8c", "#e1e9ff"),
        "덧셈": ("#2b4c8c", "#e1e9ff"),
        "뺄셈": ("#2b4c8c", "#e1e9ff"),
        "곱셈": ("#2b4c8c", "#e1e9ff"),
        "나눗셈": ("#2b4c8c", "#e1e9ff"),
        "문학": ("#a04431", "#ffe2da"),
        "독해": ("#a04431", "#ffe2da"),
        "어휘": ("#176e4e", "#ddf5e8"),
        "영어": ("#176e4e", "#ddf5e8"),
        "사회": ("#8c5e2b", "#fff2c8"),
        "역사": ("#8c5e2b", "#fff2c8"),
        "지리": ("#176e4e", "#ddf5e8"),
        "과학": ("#176e4e", "#ddf5e8"),
    }
    for key, (color, bg) in colors.items():
        if key in topic:
            return placeholder_image(topic, color=color, bg=bg, width=width, height=height)
    return placeholder_image(topic, width=width, height=height)
