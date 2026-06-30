import customtkinter as ctk


class TopBar(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            height=48,
            fg_color="#181820",
            corner_radius=0
        )

        self.pack_propagate(False)

        # --------------------
        # 프로젝트 이름
        # --------------------

        self.title = ctk.CTkLabel(
            self,
            text="🌙 Project NEON",
            font=("맑은 고딕", 17, "bold"),
            text_color="#FFFFFF"
        )

        self.title.pack(
            side="left",
            padx=18
        )

        # --------------------
        # 상태
        # --------------------

        self.status = ctk.CTkLabel(
            self,
            text="🟢 ONLINE",
            font=("Consolas", 13, "bold"),
            text_color="#62FF96"
        )

        self.status.pack(
            side="right",
            padx=18
        )

    # --------------------
    # 상태 변경
    # --------------------

    def set_online(self):

        self.status.configure(
            text="🟢 ONLINE",
            text_color="#62FF96"
        )

    def set_thinking(self):

        self.status.configure(
            text="🟡 THINKING...",
            text_color="#FFD35C"
        )

    def set_offline(self):

        self.status.configure(
            text="🔴 OFFLINE",
            text_color="#FF6666"
        )