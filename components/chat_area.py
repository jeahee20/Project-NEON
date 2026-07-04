import customtkinter as ctk
import tkinter as tk
import random


BG = "#07070B"
VOID = "#010104"
GLASS = "#080810"
CARD = "#10101C"
CARD_USER = "#171125"
BORDER = "#282842"
PINK = "#FF2FD6"
CYAN = "#22F7FF"
GREEN = "#4CFF4C"
PURPLE = "#8A5CFF"
TEXT = "#F5F5FF"
SUB = "#A7A7C7"


class HudCanvas(tk.Canvas):
    def __init__(self, master, height=142):
        super().__init__(master, height=height, bg=BG, highlightthickness=0, bd=0)
        self._phase = 0
        self.bind("<Configure>", self._redraw)
        self.after(850, self._pulse)

    def _redraw(self, event=None):
        self.delete("all")
        width = max(self.winfo_width(), 900)
        height = max(self.winfo_height(), 142)
        self.create_rectangle(0, 0, width, height, fill=BG, outline="")

        for x in range(10, width, 34):
            self.create_line(x, 0, x, height, fill="#0B0B1A")
        for y in range(10, height, 20):
            self.create_line(0, y, width, y, fill="#0B0B18")

        for x in range(24, width, 108):
            top = 14 + (x // 7) % 28
            bottom = height - 18 - (x // 11) % 22
            color = (PINK, CYAN, PURPLE, GREEN)[(x // 108) % 4]
            self.create_rectangle(x, top, x + 62, bottom, outline="#23233C")
            self.create_rectangle(x + 4, top + 4, x + 58, bottom - 4, outline="#111125")
            self.create_line(x, top, x + 62, top, fill=color, width=1)
            self.create_line(x + 8, bottom - 8, x + 54, bottom - 8, fill=color, width=1)
            for yy in range(top + 13, bottom - 8, 12):
                self.create_line(x + 8, yy, x + 54, yy, fill="#15152A")

        shift = (self._phase * 31) % max(width, 1)
        for offset, color, thickness in ((0, PINK, 7), (42, CYAN, 5), (160, GREEN, 2)):
            x1 = (64 + shift + offset) % width
            x2 = min(x1 + 280, width)
            self.create_rectangle(x1, 62 + offset % 18, x2, 62 + offset % 18 + thickness, fill=color, outline="")

        for i in range(52):
            x = (i * 57 + self._phase * 13) % width
            y = (i * 29) % height
            self.create_rectangle(x, y, x + 2, y + 2, fill=(PINK, CYAN, GREEN)[i % 3], outline="")

    def _pulse(self):
        self._phase = (self._phase + 1) % 80
        self._redraw()
        self.after(850, self._pulse)


class LogBackdrop(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, bg="#050508", highlightthickness=0, bd=0)
        self._phase = 0
        self.bind("<Configure>", self._draw)
        self.after(1050, self._pulse)

    def _draw(self, event=None):
        self.delete("all")
        width = max(self.winfo_width(), 900)
        height = max(self.winfo_height(), 520)
        self.create_rectangle(0, 0, width, height, fill="#050508", outline="")
        for x in range(0, width, 32):
            self.create_line(x, 0, x, height, fill="#0A0A17")
        for y in range(0, height, 24):
            self.create_line(0, y, width, y, fill="#090915")
        for i in range(18):
            x = (i * 97 + self._phase * 9) % width
            y = (i * 53 + self._phase * 4) % height
            color = (PINK, CYAN, GREEN, PURPLE)[i % 4]
            self.create_rectangle(x, y, min(x + 120, width), min(y + 58, height), outline="#17172C")
            self.create_line(x, y, min(x + 82, width), y, fill=color)
        for i in range(34):
            x = (i * 41 + self._phase * 17) % width
            y = (i * 31) % height
            self.create_rectangle(x, y, x + random.randint(12, 80), y + 1, fill=(PINK, CYAN, "#30304A")[i % 3], outline="")

    def _pulse(self):
        self._phase = (self._phase + 1) % 120
        self._draw()
        self.after(1050, self._pulse)


class GlitchRail(ctk.CTkFrame):
    def __init__(self, master, reverse=False):
        super().__init__(master, fg_color="transparent", height=9)
        side = "right" if reverse else "left"
        for width, color in ((42, PINK), (9, CYAN), (26, GREEN), (64, PURPLE), (12, CYAN)):
            ctk.CTkFrame(self, width=width, height=1, fg_color=color, corner_radius=0).pack(side=side, padx=3, pady=4)


class MessageBubble(ctk.CTkFrame):
    def __init__(self, master, text, is_user=False):
        super().__init__(master, fg_color="transparent")
        self.pack(fill="x", padx=12, pady=7)

        anchor = "e" if is_user else "w"
        outer_pad = (140, 0) if is_user else (0, 140)
        accent = PURPLE if is_user else PINK
        second = PINK if is_user else CYAN
        bubble_color = CARD_USER if is_user else CARD

        self.columnconfigure(0, weight=1)
        outer = ctk.CTkFrame(self, fg_color=VOID, corner_radius=2, border_width=1, border_color=accent)
        outer.grid(row=0, column=0, sticky=anchor, padx=outer_pad)
        inner = ctk.CTkFrame(outer, fg_color=GLASS, corner_radius=1, border_width=1, border_color=second)
        inner.pack(fill="both", expand=True, padx=(3, 5), pady=(3, 5))
        GlitchRail(inner, reverse=is_user).pack(fill="x", padx=8, pady=(7, 0))

        body = ctk.CTkFrame(inner, fg_color=bubble_color, corner_radius=1, border_width=1, border_color="#2D2D48")
        body.pack(fill="both", expand=True, padx=6, pady=5)

        if not is_user:
            ctk.CTkLabel(body, text="NEON", text_color=PINK, font=("Consolas", 10, "bold")).pack(anchor="w", padx=14, pady=(12, 0))

        message = ctk.CTkLabel(
            body,
            text=text,
            text_color=TEXT,
            font=("Malgun Gothic", 14),
            justify="left",
            wraplength=390,
        )
        message.pack(anchor="w", padx=14, pady=(10 if not is_user else 14, 15))
        GlitchRail(inner, reverse=not is_user).pack(fill="x", padx=8, pady=(0, 7))


class TypingBubble(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._running = False
        self._hiding = False
        self._dot_index = 0

        self.bubble = ctk.CTkFrame(self, fg_color=CARD, corner_radius=2, border_width=1, border_color=CYAN)
        self.bubble.pack(anchor="w")
        self.inner = ctk.CTkFrame(self.bubble, fg_color="transparent")
        self.inner.pack(padx=14, pady=9)
        ctk.CTkLabel(self.inner, text="NEON", text_color=PINK, font=("Consolas", 10, "bold")).pack(side="left", padx=(0, 10))
        self.dots = []
        for _ in range(3):
            dot = ctk.CTkLabel(self.inner, text="\u25cf", text_color="#303049", font=("Consolas", 10, "bold"))
            dot.pack(side="left", padx=2)
            self.dots.append(dot)

    def show(self):
        self._running = True
        self.pack(fill="x", padx=12, pady=7)
        self._animate_dots()

    def hide(self):
        if self._hiding:
            return
        self._hiding = True
        self._running = False
        self._fade_out(0)

    def _animate_dots(self):
        if not self._running or self._hiding:
            return
        for index, dot in enumerate(self.dots):
            dot.configure(text_color=TEXT if index <= self._dot_index else "#303049")
        self._dot_index = (self._dot_index + 1) % 3
        self.after(280, self._animate_dots)

    def _fade_out(self, step):
        colors = ((CARD, CYAN), ("#090913", PINK), (BG, "#4A2448"))
        if step >= len(colors):
            self.destroy()
            return
        fg, border = colors[step]
        self.bubble.configure(fg_color=fg, border_color=border)
        self.after(55, lambda: self._fade_out(step + 1))


class ChatArea(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color=VOID,
            corner_radius=2,
            border_width=1,
            border_color="#202037",
        )
        self.typing = None
        self._pulse_index = 0

        self.surface = ctk.CTkFrame(self, fg_color=BG, corner_radius=2, border_width=1, border_color="#272741")
        self.surface.pack(fill="x", padx=12, pady=(12, 8))

        top = ctk.CTkFrame(self.surface, fg_color="transparent")
        top.pack(fill="x", padx=14, pady=(12, 4))
        ctk.CTkLabel(top, text="CONVERSATION TERMINAL", font=("Consolas", 13, "bold"), text_color=TEXT).pack(side="left")
        ctk.CTkLabel(top, text="LIVE LINK / PRIVATE SIGNAL", font=("Consolas", 10, "bold"), text_color=SUB).pack(side="right")

        self.line = ctk.CTkFrame(self.surface, height=1, fg_color=PINK, corner_radius=0)
        self.line.pack(fill="x", padx=14, pady=(0, 8))

        self.hud = HudCanvas(self.surface, height=92)
        self.hud.pack(fill="x", padx=14, pady=(0, 12))

        self.log_shell = ctk.CTkFrame(self, fg_color="#050508", corner_radius=2, border_width=1, border_color="#19192D")
        self.log_shell.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.backdrop = LogBackdrop(self.log_shell)
        self.backdrop.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.log = ctk.CTkScrollableFrame(
            self.log_shell,
            fg_color="#050508",
            corner_radius=0,
            border_width=0,
            scrollbar_button_color="#8E1C87",
            scrollbar_button_hover_color=CYAN,
        )
        self.log.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.after(1000, self._pulse)

    def _pulse(self):
        self._pulse_index = (self._pulse_index + 1) % 4
        self.line.configure(fg_color=(PINK, CYAN, GREEN, CYAN)[self._pulse_index])
        self.after(1400, self._pulse)

    def add_user(self, text):
        MessageBubble(self.log, text=text, is_user=True)
        self.scroll_bottom()

    def add_neon(self, text):
        MessageBubble(self.log, text=text, is_user=False)
        self.scroll_bottom()

    def show_typing(self):
        if self.typing is None:
            self.typing = TypingBubble(self.log)
            self.typing.show()
            self.scroll_bottom()

    def hide_typing(self):
        if self.typing is not None:
            self.typing.hide()
            self.typing = None

    def scroll_bottom(self):
        self.after(50, lambda: self.log._parent_canvas.yview_moveto(1.0))
