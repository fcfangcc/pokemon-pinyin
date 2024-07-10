from PIL import Image, ImageDraw, ImageFont
from pypinyin import pinyin

PNG_SIZE = 400
FONT_SIZE = 50

# 设置 A4 纸的大小，单位是像素
# A4 尺寸是 210 x 297 mm，像素 = mm * DPI (例如，300 DPI)
dpi = 300
a4_width_mm = 210
a4_height_mm = 297
a4_width_px = int(a4_width_mm * dpi / 25.4)
a4_height_px = int(a4_height_mm * dpi / 25.4)


def convert_transparent_to_white(image_path):
    img = Image.open(image_path).convert("RGBA")
    W, L = img.size
    white_pixel = (0, 0, 0, 0)  # 设置透明
    for h in range(W):
        for i in range(L):
            if img.getpixel((h, i)) == white_pixel:
                img.putpixel((h, i), (255, 255, 255, 255))  # 白色
    return img


def draw_pokemon(
    background: Image,
    draw: ImageDraw.ImageDraw,
    position: tuple[int, int],
    pokemon: dict,
    font,
):
    name = pokemon["name"]
    pinyin_names = pinyin(name, v_to_u=True)

    if any(len(i) > 1 for i in pinyin_names):
        print(f"!!!发现多音字 {name=}, {pinyin_names=}")
    # 假设没有多音字
    pinyins = [i[0] for i in pinyin_names]

    x, y = position
    total_width = 0

    # 计算总宽度
    for i, char in enumerate(name):
        char_pinyin = pinyins[i]

        # 计算拼音和汉字的宽度
        pinyin_bbox = draw.textbbox((0, 0), char_pinyin, font=font)
        char_bbox = draw.textbbox((0, 0), char, font=font)

        pinyin_width = pinyin_bbox[2] - pinyin_bbox[0]
        char_width = char_bbox[2] - char_bbox[0]

        # 计算最大宽度
        char_spacing = max(pinyin_width, char_width) + 10
        total_width += char_spacing

    # 重新设置x，使其居中
    x = position[0] - total_width // 2

    # 画拼音和汉字
    for i, char in enumerate(name):
        char_pinyin = pinyins[i]

        # 计算拼音和汉字的宽度
        pinyin_bbox = draw.textbbox((0, 0), char_pinyin, font=font)
        char_bbox = draw.textbbox((0, 0), char, font=font)

        pinyin_width = pinyin_bbox[2] - pinyin_bbox[0]
        char_width = char_bbox[2] - char_bbox[0]

        # 计算最大宽度
        char_spacing = max(pinyin_width, char_width) + 10

        # 计算汉字的起始x位置，使其居中
        char_x = x + (pinyin_width - char_width) / 2

        # 画拼音
        draw.text((x, y), char_pinyin, font=font, fill="black")

        # 画汉字
        draw.text((char_x, y + FONT_SIZE + 10), char, font=font, fill="black")

        # 移动到下一个字符的位置
        x += char_spacing

    # 打开并插入固定大小的图片
    image = convert_transparent_to_white(pokemon["img_local_path"])
    image = image.resize((PNG_SIZE, PNG_SIZE))
    image_x = position[0] - PNG_SIZE // 2  # 将图片居中放置在文字正下方
    image_y = y + FONT_SIZE + 80  # 80应该通过计算得来，暂时先写死
    image_pil = image.convert("RGBA")
    background.paste(image_pil, (image_x, image_y))


def draw_a4(
    pokemons: list[dict], output: str | None = None, font_path: str | None = None
):
    font_path = font_path or "./simhei/SimHei.ttf"  # 确保字体文件路径正确
    font = ImageFont.truetype(font_path, FONT_SIZE)
    output = output or "output_a4.png"
    # 创建白色背景的图像
    background = Image.new("RGB", (a4_width_px, a4_height_px), "white")
    draw = ImageDraw.Draw(background)

    start_position = (250, 100)
    x, y = start_position
    # todo: 计算得到
    x_number = 5  # 横行
    y_number = 6  # 纵向
    for _ in range(y_number):
        for _ in range(x_number):
            if len(pokemons) == 0:
                break
            pokemon = pokemons.pop(0)
            draw_pokemon(background, draw, (x, y), pokemon, font)
            x += PNG_SIZE + 100
        else:
            x = start_position[0]
            y += PNG_SIZE + FONT_SIZE + FONT_SIZE + 100
            continue  # 如果内层循环没有 break，则继续外层循环
        break  # 如果内层循环有 break，则直接跳出外层循环

    # 保存图像
    background.save(output)


if __name__ == "__main__":
    draw_a4([{"name": "小火龙", "img_local_path": "./imgs/0001.png"}])
