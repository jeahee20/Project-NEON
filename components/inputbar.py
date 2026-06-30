import customtkinter as ctk


class InputBar(ctk.CTkFrame):

    def __init__(self, master, send_callback):

        super().__init__(
            master,
            fg_color="#181820",
            height=65,
            corner_radius=0
        )

        self.pack_propagate(False)

        # --------------------
        # 입력창
        # --------------------

        self.entry = ctk.CTkEntry(
            self,
            height=42,
            placeholder_text="메시지를 입력하세요...",
            fg_color="#22222B",
            border_color="#343446",
            text_color="#ECECEC",
            font=("맑은 고딕", 14)
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(15, 10),
            pady=10
        )

        # Enter
        self.entry.bind(
            "<Return>",
            lambda e: send_callback()
        )

        # --------------------
        # 보내기 버튼
        # --------------------

        self.send_button = ctk.CTkButton(
            self,
            text="➤",
            width=46,
            height=42,
            corner_radius=10,
            fg_color="#7B61FF",
            hover_color="#9A7BFF",
            font=("맑은 고딕", 18, "bold"),
            command=send_callback
        )

        self.send_button.pack(
            side="right",
            padx=(0, 15),
            pady=10
        )

    # --------------------
    # 입력 가져오기
    # --------------------

    def get(self):

        return self.entry.get()

    # --------------------
    # 입력 지우기
    # --------------------

    def clear(self):

        self.entry.delete(0, "end")

    # --------------------
    # 포커스
    # --------------------

    def focus(self):

        self.entry.focus()