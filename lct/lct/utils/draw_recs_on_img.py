from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from models.rectangle import Rectangle


def draw_rectangles_on_image(image: Image, rectangles: list[Rectangle]):
    image = image.copy()
    draw = ImageDraw.Draw(image)
    for rect in rectangles:
        rect = Rectangle(**rect)
        label = f"Класс: {rect.cls}, Коэф: {rect.conf:.2f}"
        fontsize = max(round(max(image.size) / 40), 12)
        font = ImageFont.truetype("lct/fonts/arial.ttf", fontsize)
        txt_width, txt_height = font.getsize(label)
        text_position = (rect.left[0], rect.left[1] - txt_height + 1)
        box_position = (rect.left[0], rect.left[1], rect.right[0], rect.right[1])
        draw.text(text_position, label, fill="red", font=font)
        draw.rectangle(box_position, outline="red", width=2)

    return image
