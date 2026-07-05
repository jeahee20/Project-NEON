import customtkinter as ctk
import ctypes
import sys


def _set_korean_ime(widget):
    if sys.platform != "win32":
        return
    try:
        hwnd = widget.winfo_id()
        imm32 = ctypes.windll.imm32
        context = imm32.ImmGetContext(hwnd)
        if not context:
            return
        IME_CMODE_NATIVE = 0x0001
        IME_SMODE_NONE = 0x0000
        imm32.ImmSetOpenStatus(context, True)
        imm32.ImmSetConversionStatus(context, IME_CMODE_NATIVE, IME_SMODE_NONE)
        imm32.ImmReleaseContext(hwnd, context)
    except Exception:
        pass


class InputBar(ctk.CTkFrame):
    def __init__(self, master, send_callback):
        super().__init__(master, fg_color="transparent", height=84, corner_radius=0)
        self.pack_propagate(False)

        self.shell = ctk.CTkFrame(self, fg_color="#090912", corner_radius=2, border_width=1, border_color="#30304E")
        self.shell.pack(fill="both", expand=True, padx=14, pady=(0, 12))
        self.left_bar = ctk.CTkFrame(self.shell, width=3, fg_color="#FF2FD6", corner_radius=0)
        self.left_bar.pack(side="left", fill="y", padx=(0, 10))

        self.entry = ctk.CTkEntry(
            self.shell,
            height=46,
            placeholder_text="\uba54\uc2dc\uc9c0\ub97c \uc785\ub825\ud558\uc138\uc694...",
            fg_color="#10101C",
            border_color="#22F7FF",
            border_width=1,
            text_color="#F5F5FF",
            placeholder_text_color="#8D8DAA",
            font=("Malgun Gothic", 14),
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=12)
        self.after(120, lambda: _set_korean_ime(self.entry))

        def on_enter(event):
            if self.send_callback is not None:
                self.send_callback()
            return "break"

        self.send_callback = send_callback
        self.entry.bind("<Return>", on_enter)
        self.entry.bind("<FocusIn>", lambda event: self._focus_style(True))
        self.entry.bind("<FocusOut>", lambda event: self._focus_style(False))

        self.send_button = ctk.CTkButton(
            self.shell,
            text="SEND",
            width=76,
            height=46,
            corner_radius=1,
            fg_color="#171124",
            hover_color="#2A1640",
            text_color="#F5F5FF",
            border_width=1,
            border_color="#FF2FD6",
            font=("Consolas", 12, "bold"),
            command=lambda: self.send_callback() if self.send_callback is not None else None,
        )
        self.send_button.pack(side="right", padx=(0, 12), pady=12)

    def _focus_style(self, focused):
        if focused:
            self.shell.configure(border_color="#3C315A")
            self.entry.configure(border_color="#FF2FD6")
            self.left_bar.configure(fg_color="#22F7FF")
            self.after(40, lambda: _set_korean_ime(self.entry))
        else:
            self.shell.configure(border_color="#30304E")
            self.entry.configure(border_color="#22F7FF")
            self.left_bar.configure(fg_color="#FF2FD6")

    def get(self):
        return self.entry.get()

    def clear(self):
        self.entry.delete(0, "end")

    def focus(self):
        self.entry.focus()
        self.after(80, lambda: _set_korean_ime(self.entry))
