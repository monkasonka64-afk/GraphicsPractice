import os
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

os.makedirs("assets", exist_ok=True)
os.makedirs("output", exist_ok=True)


def ensure_button_assets():
    """
    Создаёт изображения состояний кнопок в assets/, если они ещё не подготовлены.
    """
    specs = {
        "assets/btn_normal.png": ("#2563eb", "#1d4ed8", "#ffffff"),
        "assets/btn_hover.png": ("#3b82f6", "#2563eb", "#ffffff"),
        "assets/btn_pressed.png": ("#1e40af", "#172554", "#e2e8f0"),
        "assets/btn_disabled.png": ("#94a3b8", "#64748b", "#e2e8f0"),
    }

    for path, (fill_col, border_col, text_col) in specs.items():
        if not os.path.exists(path):
            w, h = 150, 44
            img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            d.rounded_rectangle((1, 1, w - 2, h - 2), radius=10, fill=fill_col, outline=border_col, width=2)
            img.save(path, format="PNG")


def make_image_button(
    parent,
    normal,
    hover,
    pressed,
    command,
    disabled=None,
    enabled=True,
    label_text="",
    bg="#ffffff",
):
    """
    Задача 30.2 и 30.3: создаёт кнопку на базе Label с поддержкой состояний
    normal, hover, pressed, disabled и переключения активности через флаг enabled.
    """
    state = {"enabled": bool(enabled), "hovered": False}
    initial_img = normal if state["enabled"] else (disabled or normal)

    btn = tk.Label(
        parent,
        image=initial_img,
        text=label_text,
        compound=tk.CENTER,
        fg="#ffffff" if state["enabled"] else "#e2e8f0",
        font=("Segoe UI", 10, "bold"),
        bg=bg,
        borderwidth=0,
        highlightthickness=0,
        cursor="hand2" if state["enabled"] else "arrow",
    )
    btn.images = {
        "normal": normal,
        "hover": hover,
        "pressed": pressed,
        "disabled": disabled,
    }

    def on_enter(event):
        state["hovered"] = True
        if not state["enabled"]:
            return
        btn.config(image=hover)

    def on_leave(event):
        state["hovered"] = False
        if not state["enabled"]:
            return
        btn.config(image=normal)

    def on_press(event):
        if not state["enabled"]:
            return
        btn.config(image=pressed)

    def on_release(event):
        if not state["enabled"]:
            return
        btn.config(image=hover if state["hovered"] else normal)
        if callable(command):
            command()

    def set_enabled(value: bool):
        state["enabled"] = bool(value)
        if state["enabled"]:
            btn.config(
                image=hover if state["hovered"] else normal,
                fg="#ffffff",
                cursor="hand2",
            )
        else:
            btn.config(
                image=disabled if disabled is not None else normal,
                fg="#e2e8f0",
                cursor="arrow",
            )

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.bind("<ButtonPress-1>", on_press)
    btn.bind("<ButtonRelease-1>", on_release)
    btn.set_enabled = set_enabled
    return btn


def run_lesson_30():
    ensure_button_assets()

    root = tk.Tk()
    root.title("Урок 30 — Кнопки с картинками и событиями")
    root.geometry("800x600")
    root.configure(bg="#f8fafc")

    normal = ImageTk.PhotoImage(Image.open("assets/btn_normal.png"))
    hover = ImageTk.PhotoImage(Image.open("assets/btn_hover.png"))
    pressed = ImageTk.PhotoImage(Image.open("assets/btn_pressed.png"))
    disabled_img = ImageTk.PhotoImage(Image.open("assets/btn_disabled.png"))

    status_var = tk.StringVar(value="Состояние: кнопки активны")
    tk.Label(
        root,
        textvariable=status_var,
        font=("Segoe UI", 11, "bold"),
        bg="#f8fafc",
        fg="#0f172a",
    ).pack(pady=(40, 20))

    # Основная кнопка (Задача 30.1)
    def on_ok():
        print("Кнопка нажата")
        status_var.set("Нажата кнопка: Применить")

    btn_ok = make_image_button(
        root,
        normal=normal,
        hover=hover,
        pressed=pressed,
        command=on_ok,
        disabled=disabled_img,
        enabled=True,
        label_text="Применить",
        bg="#f8fafc",
    )
    btn_ok.place(x=230, y=400)

    # Вторая кнопка «Отмена» (Задача 30.2)
    def on_cancel():
        print("Нажата кнопка Отмена")
        status_var.set("Нажата кнопка: Отмена")

    btn_cancel = make_image_button(
        root,
        normal=normal,
        hover=hover,
        pressed=pressed,
        command=on_cancel,
        disabled=disabled_img,
        enabled=True,
        label_text="Отмена",
        bg="#f8fafc",
    )
    btn_cancel.place(x=410, y=400)

    # Флаг активности для демонстрации неактивного состояния (Задача 30.3)
    is_enabled_var = tk.BooleanVar(value=True)

    def toggle_disabled_state():
        flag = is_enabled_var.get()
        btn_ok.set_enabled(flag)
        btn_cancel.set_enabled(flag)
        status_var.set("Состояние: кнопки активны" if flag else "Состояние: кнопки отключены (disabled)")

    tk.Checkbutton(
        root,
        text="Кнопки активны (флаг состояния)",
        variable=is_enabled_var,
        command=toggle_disabled_state,
        font=("Segoe UI", 10),
        bg="#f8fafc",
        fg="#1e293b",
        activebackground="#f8fafc",
    ).place(x=280, y=465)

    root.mainloop()


if __name__ == "__main__":
    run_lesson_30()