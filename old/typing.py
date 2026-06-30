import customtkinter as ctk


class TypingBubble(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            fg_color="#1A1A22",
            corner_radius=14
        )

        self.name = ctk.CTkLabel(
            self,
            text="🌙 네온",
            text_color="#CFCFCF",
            font=("맑은 고딕", 11, "bold")
        )

        self.name.pack(
            anchor="w",
            padx=10,
            pady=(6, 0)
        )

        self.status = ctk.CTkLabel(
            self,
            text="● THINKING...",
            text_color="#52FF8F",
            font=("Consolas", 13, "bold")
        )

        self.status.pack(
            anchor="w",
            padx=10,
            pady=(2, 0)
        )

        self.typing = ctk.CTkLabel(
            self,
            text="...",
            text_color="#E5E5E5",
            font=("맑은 고딕", 15)
        )

        self.typing.pack(
            anchor="w",
            padx=10,
            pady=(0, 8)
        )

    def show(self):

        self.pack(
            fill="x",
            padx=10,
            pady=4
        )

    def hide(self):

        self.destroy()