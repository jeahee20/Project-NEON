import customtkinter as ctk
import tkinter as tk
import os
import random
import sys
import threading
import time

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if DATA_DIR not in sys.path:
    sys.path.append(DATA_DIR)

from brain import generate_reply as neon_reply
import presence
import opening_state

from components.topbar import TopBar
from components.sidebar import SideBar
from components.chat_area import ChatArea
from components.activity_panel import ActivityPanel
from components.emotion_panel import EmotionPanel
from components.inputbar import InputBar


BG = "#07070B"
VOID = "#010104"
PANEL = "#090912"
CARD = "#0E0E19"
PINK = "#FF2FD6"
CYAN = "#22F7FF"
GREEN = "#4CFF4C"
PURPLE = "#8A5CFF"
TEXT = "#F5F5FF"
SUBTEXT = "#A7A7C7"


class SystemBackdrop(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, bg=BG, highlightthickness=0, bd=0)
        self.phase = 0
        self.bind("<Configure>", self._draw)
        self.after(180, self._pulse)

    def _draw(self, event=None):
        self.delete("all")
        w = max(self.winfo_width(), 1280)
        h = max(self.winfo_height(), 760)
        self.create_rectangle(0, 0, w, h, fill=BG, outline="")

        for x in range(0, w, 34):
            self.create_line(x, 0, x, h, fill="#0B0B18")
        for y in range(0, h, 22):
            self.create_line(0, y, w, y, fill="#0A0A16")

        for i in range(26):
            x = (i * 73 + self.phase * 11) % w
            y = (i * 41 + self.phase * 7) % h
            color = (PINK, CYAN, "#2B2B45", PURPLE)[i % 4]
            self.create_rectangle(x, y, x + 42 + (i % 5) * 20, y + 1, fill=color, outline="")

        for i in range(12):
            x1 = (i * 119 + self.phase * 5) % w
            y1 = (i * 67) % h
            x2 = min(x1 + 150 + (i % 3) * 70, w - 12)
            y2 = min(y1 + 54 + (i % 4) * 24, h - 12)
            color = (PINK, CYAN, GREEN, PURPLE)[i % 4]
            self.create_rectangle(x1, y1, x2, y2, outline="#17172A", width=1)
            self.create_line(x1, y1, min(x1 + 90, x2), y1, fill=color, width=1)
            self.create_line(max(x2 - 82, x1), y2, x2, y2, fill=color, width=1)

        for i in range(90):
            x = random.randint(0, w)
            y = random.randint(0, h)
            color = random.choice((PINK, CYAN, GREEN, "#32324C"))
            self.create_rectangle(x, y, x + 1, y + 1, fill=color, outline="")

    def _pulse(self):
        self.phase = (self.phase + 1) % 120
        self._draw()
        self.after(520, self._pulse)


class BootScreen(ctk.CTkFrame):
    def __init__(self, master, on_finish):
        super().__init__(master, fg_color=VOID)
        self.on_finish = on_finish
        self._running = True
        self._finished = False
        self._scan_y = 0
        self._boot_width = 1180
        self._boot_height = 680
        self._log_lines = []
        self._typing_line = ""

        self.canvas = tk.Canvas(self, bg=VOID, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.bind("<Configure>", self._on_resize)
        self.canvas.bind("<Configure>", self._on_resize)

    def _on_resize(self, event=None):
        if event is not None:
            self._boot_width = max(event.width, 1)
            self._boot_height = max(event.height, 1)

    def _size(self):
        self.update_idletasks()
        w = max(self.winfo_width(), self.canvas.winfo_width(), self.master.winfo_width(), 900)
        h = max(self.winfo_height(), self.canvas.winfo_height(), self.master.winfo_height(), 560)
        self._boot_width = w
        self._boot_height = h
        return w, h

    def start(self):
        self._draw_noise(0)
        self.after(5200, self._finish)

    def _draw_noise(self, count):
        if self._finished:
            return
        w, h = self._size()
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, w, h, fill="#030308", outline="")

        shift = count * 53 + random.randint(-70, 70)
        for y in range(0, h, 2):
            self.canvas.create_line(0, y, w, y, fill="#15101F" if y % 8 == 0 else "#060611")

        for _ in range(20):
            y = random.randint(-50, h)
            band_h = random.randint(28, 92)
            base = random.choice(("#0E7CC9", "#09599A", "#122D8E", "#441083", "#7A137D", "#070B1E"))
            self.canvas.create_rectangle(0, y, w, y + band_h, fill=base, outline="")
            for _ in range(24):
                x = random.randint(-180, w)
                bw = random.randint(24, 210)
                bh = random.randint(5, 28)
                color = random.choice((CYAN, PINK, "#F7FBFF", "#55A7FF", "#8A5CFF", "#F7A35C"))
                self.canvas.create_rectangle(
                    x + shift,
                    y + random.randint(0, max(band_h - 2, 1)),
                    x + bw + shift,
                    y + bh,
                    fill=color,
                    outline="",
                )

        for _ in range(130):
            y = random.randint(0, h)
            x = random.randint(-w // 3, w)
            length = random.randint(50, max(180, w // 2))
            color = random.choice(("#FFFFFF", "#DFFFFF", CYAN, PINK, "#5F76FF"))
            self.canvas.create_rectangle(x - shift, y, x + length - shift, y + random.choice((1, 1, 2, 3)), fill=color, outline="")

        for _ in range(300):
            x = random.randint(0, w)
            y = random.randint(0, h)
            color = random.choice((PINK, CYAN, GREEN, "#FFFFFF", "#3D66FF"))
            self.canvas.create_rectangle(x, y, x + random.randint(1, 4), y + random.randint(1, 3), fill=color, outline="")

        if count % 2 == 0:
            self.canvas.create_text(
                w // 2 + random.randint(-34, 34),
                h // 2 + random.randint(-20, 20),
                text=random.choice(("SIGNAL LOST", "SIGNAL FOUND", "NEON LINK", "SYSTEM WAKE")),
                fill=random.choice((PINK, CYAN, "#FFFFFF")),
                font=("Consolas", 44, "bold"),
            )

        if count < 13:
            self.after(45, lambda: self._draw_noise(count + 1))
        else:
            self._start_log()

    def _draw_terminal(self, progress=0.02, status="SIGNAL : FOUND"):
        w, h = self._size()
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, w, h, fill=VOID, outline="")
        for y in range(0, h, 4):
            self.canvas.create_line(0, y, w, y, fill="#080812")
        for x in range(0, w, 64):
            self.canvas.create_line(x, 0, x, h, fill="#070718")
        for _ in range(42):
            x = random.randint(0, w)
            y = random.randint(0, h)
            self.canvas.create_rectangle(x, y, x + random.randint(20, 160), y + 1, fill=random.choice((PINK, CYAN, GREEN, "#262640")), outline="")

        self.canvas.create_text(w // 2 - 3, int(h * 0.16), text="PROJECT NEON", fill=CYAN, font=("Consolas", 48, "bold"))
        self.canvas.create_text(w // 2 + 3, int(h * 0.16), text="PROJECT NEON", fill=PINK, font=("Consolas", 48, "bold"))
        self.canvas.create_text(w // 2, int(h * 0.23), text="AI OPERATING SYSTEM // SIGNAL RECOVERY", fill=SUBTEXT, font=("Consolas", 12, "bold"))

        x1 = int(w * 0.17)
        y1 = int(h * 0.32)
        x2 = int(w * 0.83)
        y2 = int(h * 0.82)
        self.canvas.create_rectangle(x1 - 5, y1 - 5, x2 + 5, y2 + 5, outline=PINK, width=1)
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#090913", outline=CYAN, width=1)
        self.canvas.create_text(x1 + 24, y1 + 28, text="[ SIGNAL ]  NEON WAKE SEQUENCE", anchor="w", fill=TEXT, font=("Consolas", 14, "bold"))

        ly = y1 + 68
        for color, line in self._log_lines[-13:]:
            self.canvas.create_text(x1 + 24, ly, text=line, anchor="w", fill=color, font=("Consolas", 12))
            ly += 23
        if self._typing_line:
            self.canvas.create_text(x1 + 24, ly, text=self._typing_line, anchor="w", fill=CYAN, font=("Consolas", 12, "bold"))

        bar_x1 = x1 + 24
        bar_y = y2 - 52
        bar_x2 = x2 - 24
        self.canvas.create_rectangle(bar_x1, bar_y, bar_x2, bar_y + 14, outline="#31314A", fill="#030307")
        fill_x = bar_x1 + int((bar_x2 - bar_x1) * max(0.01, min(progress, 1)))
        fill = PINK if progress < 0.35 else CYAN if progress < 0.88 else GREEN
        self.canvas.create_rectangle(bar_x1, bar_y, fill_x, bar_y + 14, outline="", fill=fill)
        self.canvas.create_text(bar_x2, y2 - 22, text=status, anchor="e", fill=fill, font=("Consolas", 11, "bold"))

    def _start_log(self):
        self._log_lines = [(GREEN, "SIGNAL FOUND")]
        self._typing_line = ""
        self._draw_terminal(0.12, "SIGNAL : FOUND")
        self.after(120, lambda: self._run_log(0))

    def _run_log(self, index):
        if self._finished:
            return
        logs = [
            "SYSTEM LINK...",
            "Initializing AI Core...",
            "Loading Memory Engine...",
            "Loading Emotion Engine...",
            "Loading Relationship Engine...",
            "Loading Personality...",
            "Synchronizing Memories...",
            "Searching User...",
            "Secure Link Established",
            "NEON ONLINE",
        ]
        if index >= len(logs):
            self._typing_line = ""
            self._draw_terminal(1, "NEON ONLINE")
            self.after(180, lambda: self._final_glitch(0))
            return
        text = logs[index]
        color = GREEN if text.isupper() or "Established" in text else CYAN if "Loading" in text else TEXT
        status = text.upper() if text in ("Secure Link Established", "NEON ONLINE") else "SIGNAL : ONLINE"
        self._type_log_line(index, text, color, status, 0, logs)

    def _type_log_line(self, index, text, color, status, char_index, logs):
        if self._finished:
            return
        shown = "> " + text[:char_index]
        if char_index < len(text):
            shown += random.choice(("_", "|", ""))
        self._typing_line = shown
        self._draw_terminal((index + 1) / len(logs), status)
        if char_index < len(text):
            self.after(12, lambda: self._type_log_line(index, text, color, status, char_index + 1, logs))
        else:
            self._typing_line = ""
            self._log_lines.append((color, "> " + text))
            self._draw_terminal((index + 1) / len(logs), status)
            self.after(90, lambda: self._run_log(index + 1))

    def _final_glitch(self, count):
        if self._finished:
            return
        if count >= 8:
            self._finish()
            return
        w, h = self._size()
        self._draw_terminal(1, "NEON ONLINE")
        for _ in range(18):
            y = random.randint(30, max(h - 30, 60))
            x = random.randint(0, max(w - 280, 1))
            self.canvas.create_rectangle(x, y, x + random.randint(96, 360), y + random.randint(1, 7), fill=random.choice((PINK, CYAN, GREEN, "#FFFFFF")), outline="")
        self.after(35, lambda: self._final_glitch(count + 1))

    def _finish(self):
        if self._finished:
            return
        self._finished = True
        self._running = False
        self.destroy()
        self.on_finish()


class MiniScope(tk.Canvas):
    def __init__(self, master, height=78):
        super().__init__(master, height=height, bg="#090913", highlightthickness=0, bd=0)
        self.phase = 0
        self.bind("<Configure>", self._draw)
        self.after(700, self._pulse)

    def _draw(self, event=None):
        self.delete("all")
        w = max(self.winfo_width(), 200)
        h = max(self.winfo_height(), 78)
        self.create_rectangle(0, 0, w, h, fill="#090913", outline="")
        for x in range(0, w, 18):
            self.create_line(x, 0, x, h, fill="#121226")
        for y in range(0, h, 14):
            self.create_line(0, y, w, y, fill="#121226")
        last = None
        for x in range(0, w, 8):
            y = h // 2 + int(18 * random.choice((-1, 0, 1)) * (1 if (x + self.phase) % 5 == 0 else 0))
            if last:
                self.create_line(last[0], last[1], x, y, fill=CYAN, width=1)
            last = (x, y)
        self.create_rectangle((self.phase * 9) % w, 0, ((self.phase * 9) % w) + 2, h, fill=PINK, outline="")

    def _pulse(self):
        self.phase = (self.phase + 1) % 100
        self._draw()
        self.after(700, self._pulse)


class DataDeck(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=240, fg_color="transparent", corner_radius=0)
        self.pack_propagate(False)
        self._phase = 0

        self.shell = ctk.CTkFrame(self, fg_color="#07070D", border_color="#2D2D4A", border_width=1, corner_radius=2)
        self.shell.pack(fill="both", expand=True, padx=(0, 10), pady=(10, 10))

        self.title = ctk.CTkLabel(self.shell, text="NEURAL DATA FIELD", font=("Consolas", 14, "bold"), text_color=TEXT, anchor="w")
        self.title.pack(fill="x", padx=12, pady=(12, 0))
        self.subtitle = ctk.CTkLabel(self.shell, text="live fragments / memory dust / active route", font=("Consolas", 9, "bold"), text_color=SUBTEXT, anchor="w")
        self.subtitle.pack(fill="x", padx=12, pady=(0, 8))

        self.grid = tk.Canvas(self.shell, height=205, bg="#050509", highlightthickness=0, bd=0)
        self.grid.pack(fill="x", padx=10, pady=(0, 8))

        self.cards = ctk.CTkFrame(self.shell, fg_color="transparent")
        self.cards.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        for name, rows, accent in (
            ("THREAD MAP", ("user: jaehee", "channel: private", "loop: awake", "tone: neon"), PINK),
            ("BUFFER TRACE", ("rx: stable", "tx: warm", "noise: filtered", "spark: active"), CYAN),
            ("CONTEXT LOCK", ("chat: live", "project: warm", "memory: near", "emotion: open"), GREEN),
        ):
            self._info_card(name, rows, accent)

        self.after(180, self._draw_grid)

    def _info_card(self, title, rows, accent):
        card = ctk.CTkFrame(self.cards, fg_color="#0D0D17", border_color="#292947", border_width=1, corner_radius=2)
        card.pack(fill="x", pady=5)
        top = ctk.CTkFrame(card, height=2, fg_color=accent, corner_radius=0)
        top.pack(fill="x", padx=8, pady=(7, 0))
        ctk.CTkLabel(card, text=title, font=("Consolas", 10, "bold"), text_color=accent, anchor="w").pack(fill="x", padx=10, pady=(7, 2))
        for row in rows:
            ctk.CTkLabel(card, text=row, font=("Consolas", 10), text_color=SUBTEXT, anchor="w").pack(fill="x", padx=10, pady=1)
        ctk.CTkFrame(card, height=1, fg_color="#1D1D32", corner_radius=0).pack(fill="x", padx=10, pady=(7, 8))

    def _draw_grid(self):
        self._phase = (self._phase + 1) % 1000
        self.grid.delete("all")
        w = max(self.grid.winfo_width(), 220)
        h = max(self.grid.winfo_height(), 205)
        self.grid.create_rectangle(0, 0, w, h, fill="#050509", outline="")

        for x in range(0, w, 18):
            self.grid.create_line(x, 0, x, h, fill="#0C0C19")
        for y in range(0, h, 14):
            self.grid.create_line(0, y, w, y, fill="#0A0A16")

        for i in range(72):
            x = (i * 37 + self._phase * 5) % w
            y = (i * 23 + self._phase * 3) % h
            color = (PINK, CYAN, GREEN, PURPLE)[i % 4]
            self.grid.create_rectangle(x, y, x + 2, y + 2, fill=color, outline="")

        for i in range(38):
            x = (i * 61 + self._phase * 7) % w
            y = (i * 31) % h
            width = 22 + (i % 5) * 14
            color = (CYAN, PINK, "#30304A", GREEN)[i % 4]
            self.grid.create_rectangle(x, y, min(x + width, w), y + 1, fill=color, outline="")

        for i in range(16):
            x1 = (i * 47 + self._phase * 2) % w
            y1 = (i * 29) % h
            x2 = min(x1 + 52 + (i % 4) * 15, w - 3)
            y2 = min(y1 + 26 + (i % 3) * 10, h - 3)
            color = (PINK, CYAN, GREEN, PURPLE)[i % 4]
            self.grid.create_rectangle(x1, y1, x2, y2, outline="#1F1F36")
            self.grid.create_line(x1, y1, min(x1 + 40, x2), y1, fill=color)

        for i, label in enumerate(("MEM", "ECHO", "LINK", "NODE", "RX", "TX", "CORE", "WAKE")):
            x = 12 + (i % 4) * 72
            y = 18 + (i // 4) * 104
            self.grid.create_text(x, y, text=label, fill=(PINK, CYAN, GREEN, SUBTEXT)[i % 4], font=("Consolas", 8, "bold"), anchor="w")

        sweep = (self._phase * 4) % w
        self.grid.create_rectangle(sweep, 0, sweep + 2, h, fill=CYAN, outline="")
        self.after(420, self._draw_grid)


class RightHUD(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=235, fg_color="transparent", corner_radius=0)
        self.pack_propagate(False)
        self._blink = 0

        self.shell = ctk.CTkFrame(self, fg_color="#080810", border_color="#30304E", border_width=1, corner_radius=2)
        self.shell.pack(fill="both", expand=True, padx=(0, 14), pady=(10, 10))

        self.title = ctk.CTkLabel(self.shell, text="AI CORE STATUS", font=("Consolas", 15, "bold"), text_color=TEXT, anchor="w")
        self.title.pack(fill="x", padx=14, pady=(13, 1))
        self.mode = ctk.CTkLabel(self.shell, text="MODE : ONLINE", font=("Consolas", 11, "bold"), text_color=GREEN, anchor="w")
        self.mode.pack(fill="x", padx=14, pady=(0, 3))
        ctk.CTkLabel(self.shell, text="status telemetry / living console", font=("Consolas", 9, "bold"), text_color=SUBTEXT, anchor="w").pack(fill="x", padx=14, pady=(0, 7))
        self.led = ctk.CTkFrame(self.shell, height=2, fg_color=PINK, corner_radius=0)
        self.led.pack(fill="x", padx=14, pady=(0, 8))
        MiniScope(self.shell, height=62).pack(fill="x", padx=12, pady=(0, 7))

        self.cards = {}
        for name, value, detail, accent in (
            ("EMOTION", "NORMAL", "leak: low / spark: warm", PINK),
            ("MEMORY", "SYNCED", "shared traces indexed", CYAN),
            ("RELATIONSHIP", "CLOSE", "private channel trusted", GREEN),
            ("NEURAL LINK", "LOCKED", "secure signal active", PURPLE),
            ("CACHE", "WARM", "recent replies rotating", PINK),
            ("HEARTBEAT", "72 BPM", "pulse within range", GREEN),
            ("LATENCY", "LOW", "reply path clean", CYAN),
            ("GLASS FIELD", "ACTIVE", "hud noise stable", PURPLE),
        ):
            self._card(name, value, detail, accent)
        self.after(900, self._pulse)

    def _card(self, name, value, detail, accent):
        card = ctk.CTkFrame(self.shell, fg_color="#0E0E19", border_color="#2B2B46", border_width=1, corner_radius=2)
        card.pack(fill="x", padx=12, pady=4)
        line = ctk.CTkFrame(card, width=3, fg_color=accent, corner_radius=0)
        line.pack(side="left", fill="y")
        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(side="left", fill="both", expand=True, padx=10, pady=7)
        ctk.CTkLabel(body, text=name, font=("Consolas", 10, "bold"), text_color=accent, anchor="w").pack(fill="x")
        label = ctk.CTkLabel(body, text=value, font=("Consolas", 13, "bold"), text_color=TEXT, anchor="w")
        label.pack(fill="x", pady=(2, 0))
        ctk.CTkLabel(body, text=detail, font=("Consolas", 9), text_color=SUBTEXT, anchor="w").pack(fill="x", pady=(1, 0))
        self.cards[name] = label

    def set_mode(self, value):
        self.mode.configure(text=f"MODE : {value}")
        if value == "THINKING":
            self.cards["EMOTION"].configure(text="THINKING")
            self.cards["CACHE"].configure(text="ACTIVE")
        elif value == "HAPPY":
            self.cards["EMOTION"].configure(text="OVERFLOW")
            self.cards["CACHE"].configure(text="HOT")
        elif value == "MEMORY":
            self.cards["MEMORY"].configure(text="INDEXING")
            self.cards["CACHE"].configure(text="SCAN")
        else:
            self.cards["EMOTION"].configure(text="NORMAL")
            self.cards["CACHE"].configure(text="WARM")

    def _pulse(self):
        self._blink = (self._blink + 1) % 4
        self.led.configure(fg_color=(PINK, CYAN, GREEN, CYAN)[self._blink])
        self.after(1400, self._pulse)


def run():
    last_activity = time.time()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Project NEON")
    app.geometry("1180x680+40+30")
    app.minsize(980, 620)
    app.configure(fg_color=BG)

    def build_main_ui():
        nonlocal last_activity

        backdrop = SystemBackdrop(app)
        backdrop.place(relx=0, rely=0, relwidth=1, relheight=1)

        root = ctk.CTkFrame(app, fg_color="transparent")
        root.place(relx=0, rely=0, relwidth=1, relheight=1)

        sidebar = SideBar(root)
        sidebar.pack(side="left", fill="y")

        main = ctk.CTkFrame(root, fg_color="transparent")
        main.pack(side="right", fill="both", expand=True)

        topbar = TopBar(main)
        topbar.pack(fill="x")

        workspace = ctk.CTkFrame(main, fg_color="transparent")
        workspace.pack(fill="both", expand=True)

        center = ctk.CTkFrame(workspace, fg_color="transparent", width=540)
        center.pack(side="left", fill="both", expand=False)
        center.pack_propagate(False)

        hud = RightHUD(workspace)
        hud.pack(side="right", fill="y")

        data_deck = DataDeck(workspace)
        data_deck.pack(side="right", fill="both", expand=True)

        chat = ChatArea(center)
        chat.pack(fill="both", expand=True, padx=(14, 10), pady=(10, 10))

        activity_panel = ActivityPanel(center)
        emotion_panel = EmotionPanel(center)

        inputbar = InputBar(main, send_callback=None)
        inputbar.pack(fill="x")
        inputbar.focus()

        def show_chat():
            activity_panel.pack_forget()
            emotion_panel.pack_forget()
            chat.pack(fill="both", expand=True, padx=(14, 10), pady=(10, 10))
            inputbar.pack(fill="x")
            inputbar.focus()
            topbar.set_chatting()
            hud.set_mode("ONLINE")

        def show_emotion():
            chat.pack_forget()
            inputbar.pack_forget()
            activity_panel.pack_forget()
            emotion_panel.refresh()
            emotion_panel.pack(fill="both", expand=True, padx=(14, 10), pady=(10, 10))
            topbar.set_status("Emotion")
            hud.set_mode("EMOTION")

        def show_activity():
            chat.pack_forget()
            inputbar.pack_forget()
            emotion_panel.pack_forget()
            activity_panel.refresh()
            activity_panel.pack(fill="both", expand=True, padx=(14, 10), pady=(10, 10))
            topbar.set_status("Activity")
            hud.set_mode("ACTIVITY")

        sidebar.chat_btn.configure(command=show_chat)
        sidebar.emotion_btn.configure(command=show_emotion)
        sidebar.activity_btn.configure(command=show_activity)

        def send_message():
            nonlocal last_activity
            last_activity = time.time()
            message = inputbar.get().strip()
            if message == "":
                return

            chat.add_user(message)
            inputbar.clear()

            if any(word in message for word in ("\uae30\uc5b5", "\uc800\uc7a5", "\uc57d\uc18d")):
                topbar.set_memory_cleaning()
                hud.set_mode("MEMORY")
            else:
                topbar.set_thinking()
                hud.set_mode("THINKING")

            chat.show_typing()

            def worker():
                reply = neon_reply(message)
                time.sleep(0.6)

                def finish():
                    nonlocal last_activity
                    last_activity = time.time()
                    chat.hide_typing()
                    chat.add_neon(reply)
                    if any(word in message for word in ("\uc88b\uc544\ud574", "\ucd5c\uace0", "\uace0\ub9c8\uc6cc", "\uc798\ud588\uc5b4", "\ub300\ub2e8\ud574", "\uba4b\uc838", "\ucc9c\uc7ac", "\uc0ac\ub791")):
                        topbar.set_happy_overload()
                        hud.set_mode("HAPPY")
                    else:
                        topbar.set_chatting()
                        hud.set_mode("ONLINE")
                    inputbar.focus()

                app.after(0, finish)

            threading.Thread(target=worker, daemon=True).start()

        inputbar.send_callback = send_message

        def first_message():
            chat.add_neon(opening_state.get_opening_reply())
            topbar.set_waiting()
            hud.set_mode("ONLINE")

        app.after(650, first_message)

        def auto_talk():
            while True:
                time.sleep(20)
                if not presence.should_start_conversation():
                    continue

                def speak():
                    topbar.set_thinking()
                    hud.set_mode("THINKING")
                    chat.show_typing()

                    def finish():
                        chat.hide_typing()
                        chat.add_neon(neon_reply("auto_talk"))
                        presence.mark_auto_talk()
                        topbar.set_waiting()
                        hud.set_mode("ONLINE")

                    app.after(600, finish)

                app.after(0, speak)

        threading.Thread(target=auto_talk, daemon=True).start()

    boot = BootScreen(app, build_main_ui)
    boot.pack(fill="both", expand=True)
    boot.after(80, boot.start)
    app.mainloop()
