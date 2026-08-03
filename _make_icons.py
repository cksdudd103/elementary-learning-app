from PIL import Image, ImageDraw

for size in [192, 512]:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    r = size // 8
    draw.rounded_rectangle([0, 0, size, size], radius=r, fill=(99, 102, 241, 255))
    # 책 모양
    margin = size // 5
    book_w = size - 2 * margin
    book_h = int(book_w * 1.2)
    x = margin
    y = (size - book_h) // 2
    draw.rounded_rectangle([x, y, x + book_w, y + book_h], radius=size//32, fill=(255, 255, 255, 240))
    draw.rectangle([x + book_w//2 - 2, y + size//20, x + book_w//2 + 2, y + book_h - size//20], fill=(199, 210, 254, 255))
    # 별
    star_size = size // 10
    draw.regular_polygon((size - margin - star_size, margin + star_size, star_size), 5, fill=(251, 191, 36, 255), rotation=180)
    draw.regular_polygon((margin + star_size, margin + star_size, star_size*0.7), 5, fill=(251, 191, 36, 255), rotation=180)
    img.save(f"app/static/icons/icon-{size}.png")
    print(f"Created app/static/icons/icon-{size}.png")
