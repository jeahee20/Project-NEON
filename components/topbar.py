import customtkinter as ctk


BG = "#07070B"
PANEL = "#090912"
PINK = "#FF2FD6"
CYAN = "#22F7FF"
GREEN = "#4CFF4C"
PURPLE = "#8A5CFF"
TEXT = "#F5F5FF"
SUB = "#A7A7C7"


class TopBar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, height=78, fg_color="transparent", corner_radius=0)
        self.pack_propagate(False)
        self._pulse_index = 0

        self.shell = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=2, border_width=1, border_color="#30304E")
        self.shell.pack(fill="both", expand=True, padx=14, pady=(10, 7))

        self.top_line = ctk.CTkFrame(self.shell, height=1, fg_color=PINK, corner_radius=0)
        self.top_line.pack(fill="x", padx=12, pady=(8, 0))

        row = ctk.CTkFrame(self.shell, fg_color="transparent")
        row.pack(fill="both", expand=True, padx=14, pady=(0, 8))

        mark = ctk.CTkFrame(row, fg_color="transparent", width=42, height=30)
        mark.pack(side="left", padx=(0, 12))
        mark.pack_propagate(False)
        ctk.CTkFrame(mark, width=28, height=2, fg_color=PINK, corner_radius=0).place(x=0, y=6)
        ctk.CTkFrame(mark, width=38, height=2, fg_color=CYAN, corner_radius=0).place(x=4, y=14)
        ctk.CTkFrame(mark, width=18, height=2, fg_color=GREEN, corner_radius=0).place(x=18, y=22)

        title_box = ctk.CTkFrame(row, fg_color="transparent")
        title_box.pack(side="left", fill="y")

        self.title = ctk.CTkLabel(title_box, text="PROJECT NEON OS", font=("Consolas", 22, "bold"), text_color=TEXT, anchor="w")
        self.title.pack(anchor="w")
        self.sub = ctk.CTkLabel(
            title_box,
            text="AI CORE / NEURAL LINK / SECURE USER CHANNEL",
            font=("Consolas", 10, "bold"),
            text_color=SUB,
            anchor="w",
        )
        self.sub.pack(anchor="w", pady=(0, 1))

        self.emotion = ctk.CTkLabel(row, text="Emotion : NORMAL", font=("Consolas", 12, "bold"), text_color=CYAN)
        self.emotion.pack(side="right", padx=(0, 18))

        self.online_text = ctk.CTkLabel(row, text="ONLINE", font=("Consolas", 13, "bold"), text_color="#8AFFB5")
        self.online_text.pack(side="right", padx=(7, 16))

        self.online_dot = ctk.CTkLabel(row, text="\u25cf", font=("Consolas", 13, "bold"), text_color=GREEN)
        self.online_dot.pack(side="right")

        self.status = ctk.CTkLabel(row, text="", font=("Consolas", 11), text_color=SUB)
        self.status.pack(side="right", padx=(0, 16))
        self.after(600, self._pulse_online)

    def _pulse_online(self):
        colors = ("#1D5F32", "#2CD96F", GREEN, "#2CD96F")
        lines = (PINK, CYAN, PURPLE, CYAN)
        self.online_dot.configure(text_color=colors[self._pulse_index])
        self.top_line.configure(fg_color=lines[self._pulse_index])
        self._pulse_index = (self._pulse_index + 1) % len(colors)
        self.after(2600, self._pulse_online)

    def set_status(self, text, text_color=None):
        self.online_text.configure(text="ONLINE", text_color="#8AFFB5")
        self.emotion.configure(text="Emotion : NORMAL")
        self.status.configure(text=text if text in ("Emotion", "Activity") else "", text_color=text_color or SUB)

    def set_opening(self):
        self.online_dot.configure(text_color="#18351F")
        self.status.configure(text="")

    def set_online(self):
        self.set_status("ONLINE")

    def set_thinking(self):
        self.online_text.configure(text="ONLINE", text_color="#8AFFB5")
        self.emotion.configure(text="Emotion : THINKING")
        self.status.configure(text="CORE ACTIVE")

    def set_happy_overload(self):
        self.online_text.configure(text="ONLINE", text_color="#8AFFB5")
        self.emotion.configure(text="Emotion : OVERFLOW")
        self.status.configure(text="BUFFER HOT")

    def set_memory_cleaning(self):
        self.online_text.configure(text="ONLINE", text_color="#8AFFB5")
        self.emotion.configure(text="Emotion : MEMORY")
        self.status.configure(text="INDEXING")

    def set_waiting(self):
        self.set_status("ONLINE")

    def set_chatting(self):
        self.set_status("ONLINE")

    def set_offline(self):
        self.set_status("ONLINE")
