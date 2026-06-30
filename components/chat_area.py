import customtkinter as ctk

from old.bubble import MessageBubble
from old.typing import TypingBubble

class ChatArea(ctk.CTkScrollableFrame):

    def __init__(self, master):

        super().__init__(
            master,
            fg_color="#121218",
            corner_radius=0
        )

        self.typing = None

    # --------------------
    # 사용자 메시지
    # --------------------

    def add_user(self, text):

        MessageBubble(
            self,
            text=text,
            is_user=True
        )

        self.scroll_bottom()

    # --------------------
    # 네온 메시지
    # --------------------

    def add_neon(self, text):

        MessageBubble(
            self,
            text=text,
            is_user=False
        )

        self.scroll_bottom()

    # --------------------
    # THINKING...
    # --------------------

    def show_typing(self):

        if self.typing is None:

            self.typing = TypingBubble(self)
            self.typing.show()

            self.scroll_bottom()

    # --------------------
    # THINKING 제거
    # --------------------

    def hide_typing(self):

        if self.typing is not None:

            self.typing.hide()
            self.typing = None

    # --------------------
    # 맨 아래 자동 스크롤
    # --------------------

    def scroll_bottom(self):

        self.after(
            50,
            lambda: self._parent_canvas.yview_moveto(1.0)
        )