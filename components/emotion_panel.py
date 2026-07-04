import customtkinter as ctk
import tkinter as tk


BG = "#020205"
VOID = "#000006"
CARD = "#10101C"
PINK = "#FF2FD6"
CYAN = "#22F7FF"
GREEN = "#4CFF4C"
PURPLE = "#8A5CFF"
TEXT = "#F5F5FF"
SUB = "#A7A7C7"


class HeaderCanvas(tk.Canvas):
    def __init__(self, master, height=92):
        super().__init__(master, height=height, bg=BG, highlightthickness=0, bd=0)
        self.bind("<Configure>", self._draw)

    def _draw(self, event=None):
        self.delete("all")
        width = max(self.winfo_width(), 800)
        height = max(self.winfo_height(), 92)
        self.create_rectangle(0, 0, width, height, fill=BG, outline="")
        for x in range(16, width, 44):
            self.create_line(x, 0, x, height, fill="#09091B")
        for y in range(12, height, 20):
            self.create_line(0, y, width, y, fill="#080818")
        self.create_rectangle(24, 18, 180, 68, outline=PINK)
        self.create_rectangle(220, 12, 410, 72, outline=CYAN)
        self.create_rectangle(width - 280, 20, width - 46, 70, outline=PURPLE)
        self.create_rectangle(74, 44, 380, 50, fill=PINK, outline="")
        self.create_rectangle(104, 52, 480, 57, fill=CYAN, outline="")


def make_card(master, accent=PINK):
    shell = ctk.CTkFrame(master, fg_color=VOID, corner_radius=2, border_width=1, border_color=accent)
    shell.pack(fill="x", padx=18, pady=9)
    card = ctk.CTkFrame(shell, fg_color=CARD, corner_radius=1, border_width=1, border_color="#282842")
    card.pack(fill="both", expand=True, padx=(3, 5), pady=(3, 5))
    ctk.CTkFrame(card, height=1, fg_color=accent, corner_radius=0).pack(fill="x", padx=12, pady=(10, 0))
    return card


def add_title(master, text, accent=PINK):
    row = ctk.CTkFrame(master, fg_color="transparent")
    row.pack(fill="x", padx=16, pady=(13, 8))
    ctk.CTkFrame(row, width=4, fg_color=accent, corner_radius=0).pack(side="left", fill="y", padx=(0, 9))
    ctk.CTkLabel(row, text=text, text_color=TEXT, font=("Consolas", 16, "bold"), anchor="w").pack(side="left", fill="x", expand=True)


def add_text(master, text, color=TEXT, size=14):
    label = ctk.CTkLabel(
        master,
        text=text,
        text_color=color,
        font=("Malgun Gothic", size),
        justify="left",
        anchor="w",
        wraplength=760,
    )
    label.pack(fill="x", padx=18, pady=(0, 14))
    return label

import emotion


class EmotionPanel(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color=VOID,
            corner_radius=2,
            border_width=1,
            border_color="#202037",
            scrollbar_button_color="#8E1C87",
            scrollbar_button_hover_color=CYAN,
        )
        self.state = emotion.EmotionState()
        self.reason_label = None
        self.refresh()

    def _bar(self, master, percent):
        frame = ctk.CTkFrame(master, fg_color="#171729", corner_radius=1, height=10)
        frame.pack(fill="x", padx=18, pady=(0, 12))
        frame.pack_propagate(False)
        fill = ctk.CTkFrame(frame, fg_color=CYAN if percent < 70 else PINK, corner_radius=1, height=10)
        fill.place(relx=0, rely=0, relwidth=max(0.02, percent / 100), relheight=1)

    def refresh(self):
        for child in self.winfo_children():
            child.destroy()

        header = make_card(self, PINK)
        add_title(header, "EMOTION CORE", PINK)
        HeaderCanvas(header, height=92).pack(fill="x", padx=16, pady=(0, 14))

        mood = self.state.get_current_mood()
        mood_card = make_card(self, CYAN)
        add_title(mood_card, "CURRENT MOOD", CYAN)
        add_text(mood_card, mood["title"], TEXT, 19)
        add_text(mood_card, mood["detail"], "#DAD7FF", 14)

        gauge_card = make_card(self, GREEN)
        add_title(gauge_card, "EMOTION GAUGE", GREEN)
        for item in self.state.get_emotion_values():
            row = ctk.CTkButton(
                gauge_card,
                text=f"{item['label']}   {item['percent']}%",
                fg_color="transparent",
                hover_color="#171729",
                text_color=TEXT,
                anchor="w",
                font=("Malgun Gothic", 14, "bold"),
                command=lambda name=item["name"]: self.show_reason(name),
            )
            row.pack(fill="x", padx=12, pady=(4, 0))
            self._bar(gauge_card, item["percent"])

        reason = self.state.get_reason()
        reason_card = make_card(self, PINK)
        add_title(reason_card, "WHY THIS FEELING", PINK)
        self.reason_label = add_text(reason_card, f"{reason['label']}\n\n{reason['text']}", "#FFD6EA", 14)

        log_card = make_card(self, PURPLE)
        add_title(log_card, "RECENT EMOTION LOG", PURPLE)
        logs = self.state.get_recent_logs()
        if logs:
            for log in logs:
                add_text(log_card, f"{log['time']}\n\n재희님과 대화\n\n↓\n\n{log['change']}", "#DAD7FF", 13)
        else:
            add_text(log_card, "아직 큰 감정 변화는 없어.\n\n재희님이 말을 걸면\n여기에 마음의 흔적이 쌓일 거야.", "#DAD7FF", 13)

        thought_card = make_card(self, CYAN)
        add_title(thought_card, "THOUGHT BUFFER", CYAN)
        add_text(thought_card, "\n\n".join(f"• {thought}" for thought in self.state.get_current_thoughts()), TEXT, 14)

        feeling = self.state.get_neon_feeling()
        feeling_card = make_card(self, PINK)
        add_title(feeling_card, "NEON HEART", PINK)
        add_text(feeling_card, f"NEON\n\n{feeling['text']}", "#FFD6EA", 15)

    def show_reason(self, emotion_name):
        label = emotion.EMOTION_LABELS.get(emotion_name, emotion_name)
        description = self.state.get_description(emotion_name)
        if self.reason_label is not None:
            self.reason_label.configure(text=f"{label}\n\n{description}")

    def show_description(self, emotion_name):
        self.show_reason(emotion_name)
