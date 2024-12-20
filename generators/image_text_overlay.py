from PIL import Image, ImageDraw, ImageFont

class ImageTextOverlay:
    def __init__(self, font_path=None, font_size=40):
        # Используем указанный шрифт или встроенный шрифт Pillow
        self.font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
        self.font_size = font_size

    def add_text_to_image(self, image_path, text, output_path="output_image.jpg"):
        """Добавляет подложку с текстом (заголовком) на изображение."""
        # Открываем изображение
        img = Image.open(image_path).convert('RGBA')

        # Получаем размеры изображения
        img_width, img_height = img.size

        # Создаем подложку
        overlay_height = int(img_height * 0.1)  # 10% от высоты изображения
        overlay = Image.new('RGBA', (img_width, overlay_height), (0, 0, 0, 192))  # Черная подложка с прозрачностью 75%

        # Создаем изображение с наложением подложки
        img_with_overlay = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
        img_with_overlay.paste(img, (0, 0))
        img_with_overlay.paste(overlay, (0, 0), mask=overlay)

        # Создаем объект для рисования
        draw = ImageDraw.Draw(img_with_overlay)

        # Позиция текста
        text_x = 20
        text_y = 10

        # Наносим текст
        draw.text((text_x, text_y), text, font=self.font, fill=(255, 255, 255, 255))  # Белый цвет

        # Сохраняем изображение с текстом
        img_with_overlay.convert("RGB").save(output_path, "JPEG")
        return output_path
