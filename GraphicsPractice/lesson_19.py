import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("assets", exist_ok=True)
os.makedirs("output", exist_ok=True)


def shade(color, k):
    """Изменяет яркость RGB-кортежа с коэффициентом k и ограничением [0..255]."""
    return tuple(max(0, min(255, int(c * k))) for c in color)


def load_button_font(size=20):
    """Загружает Arial из системной папки Windows или возвращает шрифт по умолчанию."""
    font_path = "C:/Windows/Fonts/arial.ttf"
    if os.path.exists(font_path):
        return ImageFont.truetype(font_path, size)
    return ImageFont.load_default()


def make_button(text, bg, size=(160, 48), fg="white", radius=10, font_size=20):
    """
    Рисует кнопку заданного размера с текстом по центру на прозрачном фоне (RGBA).
    """
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    d.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=bg)

    font = load_button_font(font_size)
    box = d.textbbox((0, 0), text, font=font)
    x = (size[0] - (box[2] - box[0])) // 2 - box[0]
    y = (size[1] - (box[3] - box[1])) // 2 - box[1]

    d.text((x, y), text, font=font, fill=fg)
    return img


def generate_login_states():
    """Задачи 19.1 и 19.3: состояния кнопки 'Войти' (normal, hover, pressed, disabled)."""
    base = (52, 152, 219)

    make_button("Войти", base, fg="white").save("assets/btn_normal.png", format="PNG")
    make_button("Войти", shade(base, 1.15), fg="white").save("assets/btn_hover.png", format="PNG")
    make_button("Войти", shade(base, 0.85), fg="white").save("assets/btn_pressed.png", format="PNG")

    # Четвёртое состояние (Задача 19.3): серая кнопка с бледным текстом
    disabled_bg = (160, 166, 173)
    disabled_fg = (214, 218, 222)
    make_button("Войти", disabled_bg, fg=disabled_fg).save("assets/btn_disabled.png", format="PNG")

    print("[19.1 & 19.3] Сохранены состояния кнопки 'Войти' в assets/")


def generate_action_buttons():
    """Задача 19.2: кнопки 'Отмена' (красная) и 'Сохранить' (зелёная)."""
    red_base = (220, 53, 69)
    green_base = (40, 167, 69)

    make_button("Отмена", red_base, fg="white").save("output/btn_cancel.png", format="PNG")
    make_button("Сохранить", green_base, fg="white").save("output/btn_save.png", format="PNG")

    print("[19.2] Сохранены кнопки 'Отмена' и 'Сохранить' в output/")


if __name__ == "__main__":
    generate_login_states()
    generate_action_buttons()