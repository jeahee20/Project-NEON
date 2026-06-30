import customtkinter as ctk


class MessageBubble(ctk.CTkFrame):

    def __init__(self, master, text, is_user=False):

        if is_user:
            bubble_color = "#5A3B8C"
            name = "😊 재희"
            anchor = "e"
        else:
            bubble_color = "#1A1A22"
            name = "🌙 네온"
            anchor = "w"

        super().__init__(
            master,
            fg_color=bubble_color,
            corner_radius=14
        )

        self.pack(
            fill="x",
            pady=4,
            padx=10,
            anchor=anchor
        )

        self.name_label = ctk.CTkLabel(
            self,
            text=name,
            text_color="#CFCFCF",
            font=("맑은 고딕", 11, "bold")
        )

        self.name_label.pack(
            anchor="w",
            padx=10,
            pady=(6, 0)
        )

        self.text_label = ctk.CTkLabel(
            self,
            text=text,
            text_color="#ECECEC",
            font=("맑은 고딕", 14),
            wraplength=680,
            justify="left"
        )

        self.text_label.pack(
            anchor="w",
            padx=10,
            pady=(2, 8)
        )