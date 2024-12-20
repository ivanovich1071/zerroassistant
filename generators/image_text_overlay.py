from PIL import Image, ImageDraw, ImageFont
import os
import logging

class ImageTextOverlay:
    def __init__(self, font_path="C:/Windows/Fonts/arial.ttf", font_size=48):
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font not found: {font_path}")
        self.font = ImageFont.truetype(font_path, font_size)
        self.font_size = font_size

    def add_text_to_image(self, image_path, text, output_path="output_image.jpg"):
        """Добавляет текст на изображение и сохраняет его, гарантируя замену файла."""
        # Проверяем, существует ли входное изображение
        if not os.path.exists(image_path):
            logging.error(f"Input image not found: {image_path}")
            raise FileNotFoundError(f"Input image not found: {image_path}")

        # Удаляем старый файл, если он существует
        if os.path.exists(output_path):
            os.remove(output_path)

        # Открываем изображение
        img = Image.open(image_path).convert("RGBA")
        img_width, img_height = img.size

        # Создаем подложку для текста (10% от высоты изображения)
        overlay_height = int(img_height * 0.15)
        overlay = Image.new("RGBA", (img_width, overlay_height), (0, 0, 0, 192))  # Прозрачность 75%

        # Разбиваем текст на строки, чтобы уместить его на подложке
        draw = ImageDraw.Draw(overlay)
        max_width = img_width - 40  # Отступы по краям
        lines = []
        line = ""
        for word in text.split():
            test_line = f"{line} {word}".strip()
            if draw.textlength(test_line, font=self.font) <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)

        # Вычисляем вертикальное позиционирование текста
        line_height = self.font_size + 5
        text_y = (overlay_height - len(lines) * line_height) // 2
        text_x = 20  # Горизонтальный отступ

        # Наносим текст построчно
        for line in lines:
            draw.text((text_x, text_y), line, font=self.font, fill=(255, 255, 255, 255))
            text_y += line_height

        # Накладываем подложку с текстом на изображение
        img.paste(overlay, (0, 0), overlay)

        # Преобразуем изображение из RGBA в RGB перед сохранением
        img = img.convert("RGB")

        # Сохраняем результат
        img.save(output_path)
        logging.info(f"Image saved with text overlay at {output_path}")
