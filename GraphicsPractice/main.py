import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk

WINDOW_W, WINDOW_H = 800, 600
APP_TITLE = "ГрафМастер UI — Авторизация"

# Палитра из 5 цветов (Урок 31)
PALETTE = {
    "header": "#1F3A5F",   # тёмно-синий акцент
    "accent": "#2563EB",   # интерактивный синий
    "bg": "#F1F5F9",       # светло-серый фон
    "surface": "#FFFFFF",  # поверхность карточки и полей
    "text": "#334155",     # цвет текста и границ
}

# Все пути к ресурсам в одном словаре в начале файла (Задача 33.3)
ASSETS = {
    "icon": os.path.join("assets", "app.ico"),
    "bg": os.path.join("assets", "bg.jpg"),
    "logo": os.path.join("assets", "logo.png"),
    "user_icon": os.path.join("assets", "ic_user.png"),
    "lock_icon": os.path.join("assets", "ic_lock.png"),
    "btn_normal": os.path.join("assets", "btn_normal.png"),
    "btn_hover": os.path.join("assets", "btn_hover.png"),
    "btn_pressed": os.path.join("assets", "btn_pressed.png"),
    "btn_disabled": os.path.join("assets", "btn_disabled.png"),
}

# Тестовые учётные данные для проверки входа (Задача 33.2)
VALID_LOGIN = "admin"
VALID_PASSWORD = "123"


def make_fallback_photo(size: tuple[int, int], fill_hex: str, text: str = "") -> ImageTk.PhotoImage:
    """Резервная картинка, если файл ресурса не найден."""
    img = Image.new("RGBA", size, fill_hex)
    if text:
        draw = ImageDraw.Draw(img)
        draw.text((10, max(4, size[1] // 2 - 6)), text, fill="#FFFFFF")
    return ImageTk.PhotoImage(img)


def load_photo(path: str, size: tuple[int, int], fallback_hex: str, label: str = "") -> ImageTk.PhotoImage:
    """Загружает изображение заданного размера и удерживает ссылку через PhotoImage."""
    if os.path.isfile(path):
        with Image.open(path) as raw:
            resized = raw.convert("RGBA").resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(resized)
    return make_fallback_photo(size, fallback_hex, label)


class ImageStateButton(tk.Label):
    """Кнопка-изображение 160x48 с состояниями normal, hover, pressed и disabled."""

    def __init__(
        self,
        parent: tk.Widget,
        images: dict[str, ImageTk.PhotoImage],
        command,
        bg_hex: str,
        enabled: bool = True,
    ):
        self.images = images
        self.command = command
        self.enabled = enabled
        self._is_hover = False
        self._is_pressed = False

        super().__init__(
            parent,
            image=self._current_image(),
            bg=bg_hex,
            borderwidth=0,
            highlightthickness=0,
            cursor="hand2" if enabled else "arrow",
        )
        # Сохраняем ссылки на все состояния, чтобы сборщик мусора их не удалил
        self.image = self._current_image()

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _current_image(self) -> ImageTk.PhotoImage:
        if not self.enabled:
            return self.images["disabled"]
        if self._is_pressed:
            return self.images["pressed"]
        if self._is_hover:
            return self.images["hover"]
        return self.images["normal"]

    def refresh(self) -> None:
        img = self._current_image()
        self.configure(image=img, cursor="hand2" if self.enabled else "arrow")
        self.image = img

    def set_enabled(self, enabled: bool) -> None:
        self.enabled = enabled
        if not enabled:
            self._is_pressed = False
        self.refresh()

    def _on_enter(self, _event) -> None:
        self._is_hover = True
        self.refresh()

    def _on_leave(self, _event) -> None:
        self._is_hover = False
        self._is_pressed = False
        self.refresh()

    def _on_press(self, _event) -> None:
        if not self.enabled:
            return
        self._is_pressed = True
        self.refresh()

    def _on_release(self, event) -> None:
        if not self.enabled:
            return
        was_pressed = self._is_pressed
        self._is_pressed = False
        self.refresh()
        inside = 0 <= event.x <= self.winfo_width() and 0 <= event.y <= self.winfo_height()
        if was_pressed and inside and callable(self.command):
            self.command()


class AuthApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.root.resizable(False, False)
        self.root.configure(bg=PALETTE["bg"])

        # Иконка окна (16-256 px)
        if os.path.isfile(ASSETS["icon"]):
            try:
                self.root.iconbitmap(ASSETS["icon"])
            except tk.TclError:
                pass

        # Хранилище ссылок на PhotoImage
        self.photos: dict[str, ImageTk.PhotoImage] = {
            "bg": load_photo(ASSETS["bg"], (WINDOW_W, WINDOW_H), PALETTE["bg"], "BG"),
            "logo": load_photo(ASSETS["logo"], (200, 60), PALETTE["header"], "LOGO"),
            "user": load_photo(ASSETS["user_icon"], (24, 24), PALETTE["accent"], "U"),
            "lock": load_photo(ASSETS["lock_icon"], (24, 24), PALETTE["accent"], "P"),
            "btn_normal": load_photo(ASSETS["btn_normal"], (160, 48), PALETTE["accent"], "Войти"),
            "btn_hover": load_photo(ASSETS["btn_hover"], (160, 48), "#3B82F6", "Войти"),
            "btn_pressed": load_photo(ASSETS["btn_pressed"], (160, 48), PALETTE["header"], "Войти"),
            "btn_disabled": load_photo(ASSETS["btn_disabled"], (160, 48), "#94A3B8", "Войти"),
        }

        self._build_ui()

    def _build_ui(self) -> None:
        # Фоновое изображение 800x600
        bg_label = tk.Label(self.root, image=self.photos["bg"], borderwidth=0)
        bg_label.place(x=0, y=0, width=WINDOW_W, height=WINDOW_H)

        # Верхняя шапка 800x80 с логотипом 200x60
        header = tk.Frame(self.root, bg=PALETTE["header"], width=WINDOW_W, height=80)
        header.place(x=0, y=0)
        header.pack_propagate(False)

        logo_label = tk.Label(
            header,
            image=self.photos["logo"],
            bg=PALETTE["header"],
            borderwidth=0,
            highlightthickness=0,
        )
        logo_label.pack(side=tk.LEFT, padx=24, pady=10)

        # Карточка авторизации по центру окна
        card = tk.Frame(
            self.root,
            bg=PALETTE["surface"],
            width=380,
            height=320,
            highlightbackground=PALETTE["text"],
            highlightthickness=1,
        )
        card.place(relx=0.5, rely=0.54, anchor=tk.CENTER)
        card.pack_propagate(False)

        title_lbl = tk.Label(
            card,
            text="Вход в систему",
            font=("Segoe UI", 16, "bold"),
            bg=PALETTE["surface"],
            fg=PALETTE["header"],
        )
        title_lbl.pack(pady=(24, 18))

        # Поле «Логин» с иконкой 24x24 слева
        login_row = tk.Frame(card, bg=PALETTE["surface"])
        login_row.pack(pady=(0, 14))

        tk.Label(
            login_row,
            image=self.photos["user"],
            bg=PALETTE["surface"],
            borderwidth=0,
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.login_entry = tk.Entry(
            login_row,
            font=("Segoe UI", 11),
            width=26,
            fg=PALETTE["text"],
            bg=PALETTE["bg"],
            relief=tk.FLAT,
            highlightbackground="#CBD5E1",
            highlightcolor=PALETTE["accent"],
            highlightthickness=1,
        )
        self.login_entry.pack(side=tk.LEFT, ipady=7)
        self.login_entry.focus_set()

        # Поле «Пароль» с иконкой 24x24 слева
        pass_row = tk.Frame(card, bg=PALETTE["surface"])
        pass_row.pack(pady=(0, 22))

        tk.Label(
            pass_row,
            image=self.photos["lock"],
            bg=PALETTE["surface"],
            borderwidth=0,
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.password_entry = tk.Entry(
            pass_row,
            font=("Segoe UI", 11),
            width=26,
            show="*",
            fg=PALETTE["text"],
            bg=PALETTE["bg"],
            relief=tk.FLAT,
            highlightbackground="#CBD5E1",
            highlightcolor=PALETTE["accent"],
            highlightthickness=1,
        )
        self.password_entry.pack(side=tk.LEFT, ipady=7)
        self.password_entry.bind("<Return>", lambda _e: self.check_login())

        # Кнопка «Войти» 160x48 с состояниями
        self.login_btn = ImageStateButton(
            card,
            images={
                "normal": self.photos["btn_normal"],
                "hover": self.photos["btn_hover"],
                "pressed": self.photos["btn_pressed"],
                "disabled": self.photos["btn_disabled"],
            },
            command=self.check_login,
            bg_hex=PALETTE["surface"],
            enabled=True,
        )
        self.login_btn.pack(pady=(4, 0))

    def check_login(self) -> None:
        login = self.login_entry.get().strip()
        password = self.password_entry.get()

        if not login or not password:
            messagebox.showwarning(
                "Недостаточно данных",
                "Введите логин и пароль.",
                parent=self.root,
            )
            return

        if login == VALID_LOGIN and password == VALID_PASSWORD:
            messagebox.showinfo(
                "Успешный вход",
                f"Добро пожаловать, {login}!",
                parent=self.root,
            )
        else:
            messagebox.showerror(
                "Ошибка авторизации",
                "Неверный логин или пароль.\nТестовые данные: admin / 123",
                parent=self.root,
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = AuthApp(root)
    root.mainloop()