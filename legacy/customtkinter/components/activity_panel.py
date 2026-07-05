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

import time
import presence


class ActivityPanel(ctk.CTkScrollableFrame):
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
        self.refresh()

    def _last_message_text(self):
        diff = int(time.time() - presence.last_message_time)
        if diff < 60:
            return "방금"
        minutes = diff // 60
        if minutes < 60:
            return f"{minutes}분 전"
        hours = minutes // 60
        return f"{hours}시간 전"

    def refresh(self):
        for child in self.winfo_children():
            child.destroy()

        header = make_card(self, CYAN)
        add_title(header, "ACTIVITY HUD", CYAN)
        HeaderCanvas(header, height=92).pack(fill="x", padx=16, pady=(0, 14))

        status = presence.get_status()
        activity = presence.get_activity()

        current_card = make_card(self, GREEN)
        add_title(current_card, "CURRENT SIGNAL", GREEN)
        add_text(current_card, f"상태 : {status}\n\n활동 : {activity}\n\n마지막 대화 : {self._last_message_text()}", "#8AFFB5", 15)

        presence_card = make_card(self, PINK)
        add_title(presence_card, "NEON WATCH", PINK)
        add_text(presence_card, f"재희님 신호를 보고 있어.\n\n지금은 {activity} 흐름으로 잡혀 있어.", TEXT, 14)

        log_card = make_card(self, PURPLE)
        add_title(log_card, "RECENT ACTIVITY LOG", PURPLE)
        logs = presence.get_logs()
        if logs:
            for log in reversed(logs[-30:]):
                add_text(log_card, f"{log['time']}  {log['event']}\n상태 {log['status']} / 활동 {log['activity']}", "#DAD7FF", 13)
        else:
            add_text(log_card, "아직 움직임 로그는 없어.\n\n재희님이 말을 걸면\n여기에 신호가 쌓일 거야.", "#DAD7FF", 13)
