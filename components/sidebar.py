import customtkinter as ctk


class SideBar(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            width=180,
            fg_color="#111118",
            corner_radius=0
        )

        self.pack_propagate(False)

        # --------------------
        # 로고
        # --------------------

        logo = ctk.CTkLabel(
            self,
            text="🌙\nPROJECT\nNEON",
            font=("맑은 고딕", 22, "bold"),
            text_color="#FFFFFF",
            justify="center"
        )

        logo.pack(pady=(30, 35))

        # --------------------
        # 메뉴
        # --------------------

        self.chat_btn = self.create_button("💬 Chat")
        self.memory_btn = self.create_button("🧠 Memory")
        self.emotion_btn = self.create_button("😊 Emotion")
        self.activity_btn = self.create_button("🎮 Activity")
        self.settings_btn = self.create_button("⚙ Settings")

    def create_button(self, text):

        button = ctk.CTkButton(
            self,
            text=text,
            width=150,
            height=42,
            corner_radius=10,
            fg_color="transparent",
            hover_color="#232330",
            text_color="#DDDDDD",
            anchor="w",
            font=("맑은 고딕", 15)
        )

        button.pack(pady=5, padx=12)

        return button