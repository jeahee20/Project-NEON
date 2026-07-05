import customtkinter as ctk


BG = "#07070B"
PANEL = "#090912"
CARD = "#0E0E19"
PINK = "#FF2FD6"
CYAN = "#22F7FF"
GREEN = "#4CFF4C"
PURPLE = "#8A5CFF"
TEXT = "#F5F5FF"
SUB = "#A7A7C7"


class SideBar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=220, fg_color="transparent", corner_radius=0)
        self.pack_propagate(False)

        self.board = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=2, border_width=1, border_color="#30304E")
        self.board.pack(fill="both", expand=True, padx=(8, 8), pady=10)

        self.logo_panel = ctk.CTkFrame(self.board, fg_color=CARD, height=146, corner_radius=2, border_width=1, border_color="#3A2551")
        self.logo_panel.pack(fill="x", padx=10, pady=(12, 16))
        self.logo_panel.pack_propagate(False)

        top = ctk.CTkFrame(self.logo_panel, fg_color="transparent", height=12)
        top.pack(fill="x", padx=10, pady=(10, 0))
        ctk.CTkFrame(top, width=70, height=1, fg_color=PINK, corner_radius=0).pack(side="left")
        ctk.CTkFrame(top, width=22, height=1, fg_color=CYAN, corner_radius=0).pack(side="left", padx=5)
        ctk.CTkFrame(top, width=38, height=1, fg_color=GREEN, corner_radius=0).pack(side="right")

        logo = ctk.CTkLabel(self.logo_panel, text="NEON", font=("Consolas", 32, "bold"), text_color=TEXT)
        logo.pack(pady=(16, 0))
        sub = ctk.CTkLabel(self.logo_panel, text="OPERATING SYSTEM", font=("Consolas", 10, "bold"), text_color=SUB)
        sub.pack(pady=(0, 10))

        mini = ctk.CTkFrame(self.logo_panel, fg_color="transparent")
        mini.pack(fill="x", padx=18)
        for color in (PINK, CYAN, GREEN, PURPLE, CYAN):
            ctk.CTkFrame(mini, width=22, height=3, fg_color=color, corner_radius=1).pack(side="left", padx=2)

        self.chat_btn = self.create_button("CHAT", CYAN)
        self.memory_btn = self.create_button("MEMORY", PINK)
        self.emotion_btn = self.create_button("EMOTION", GREEN)
        self.activity_btn = self.create_button("ACTIVITY", CYAN)
        self.settings_btn = self.create_button("SETTINGS", PURPLE)

        spacer = ctk.CTkFrame(self.board, fg_color="transparent")
        spacer.pack(fill="both", expand=True)

        self.bottom_hint = ctk.CTkFrame(self.board, fg_color=CARD, height=116, corner_radius=2, border_width=1, border_color="#30304E")
        self.bottom_hint.pack(side="bottom", fill="x", padx=10, pady=12)
        self.bottom_hint.pack_propagate(False)

        ctk.CTkFrame(self.bottom_hint, height=1, fg_color=CYAN, corner_radius=0).pack(fill="x", padx=10, pady=(10, 0))
        hint = ctk.CTkLabel(
            self.bottom_hint,
            text="SIGNAL STABLE\nCORE READY\nLINK PRIVATE\nUSER: JAEHEE",
            font=("Consolas", 10, "bold"),
            text_color=SUB,
            justify="left",
        )
        hint.pack(anchor="w", padx=12, pady=11)

    def create_button(self, text, accent):
        frame = ctk.CTkFrame(self.board, fg_color="#0B0B14", height=50, corner_radius=2, border_width=1, border_color="#30304E")
        frame.pack(fill="x", pady=5, padx=10)
        frame.pack_propagate(False)
        ctk.CTkFrame(frame, width=3, fg_color=accent, corner_radius=0).pack(side="left", fill="y")
        button = ctk.CTkButton(
            frame,
            text=text,
            height=46,
            corner_radius=1,
            fg_color="transparent",
            hover_color="#1B1024",
            text_color=TEXT,
            border_width=0,
            anchor="w",
            font=("Consolas", 13, "bold"),
        )
        button.pack(side="left", fill="x", expand=True, padx=(12, 0), pady=1)
        return button
