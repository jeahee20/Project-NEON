import customtkinter as ctk
import threading
import time
import random

from brain import neon_reply

from components.topbar import TopBar
from components.sidebar import SideBar
from components.chat_area import ChatArea
from components.inputbar import InputBar


def run():

    # --------------------
    # 앱 설정
    # --------------------

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()

    app.title("🌙 Project NEON")
    app.geometry("1200x760")
    app.minsize(1000, 650)

    app.configure(
        fg_color="#0B0B0F"
    )

    # --------------------
    # 메인 레이아웃
    # --------------------

    root = ctk.CTkFrame(
        app,
        fg_color="transparent"
    )

    root.pack(
        fill="both",
        expand=True
    )

    # --------------------
    # 사이드바
    # --------------------

    sidebar = SideBar(root)

    sidebar.pack(
        side="left",
        fill="y"
    )

    # --------------------
    # 오른쪽 영역
    # --------------------

    right = ctk.CTkFrame(
        root,
        fg_color="#0B0B0F"
    )

    right.pack(
        side="right",
        fill="both",
        expand=True
    )

    # --------------------
    # 상단바
    # --------------------

    topbar = TopBar(right)

    topbar.pack(
        fill="x"
    )

    # --------------------
    # 채팅 영역
    # --------------------

    chat = ChatArea(right)

    chat.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=(15, 10)
    )    
    # --------------------
    # 입력창
    # --------------------

    def send_message():

        message = inputbar.get().strip()

        if message == "":
            return

        chat.add_user(message)

        inputbar.clear()

        topbar.set_thinking()

        chat.show_typing()

        def worker():

            reply = neon_reply(message)

            time.sleep(0.6)

            def finish():

                chat.hide_typing()

                chat.add_neon(reply)

                topbar.set_online()

                inputbar.focus()

            app.after(0, finish)

        threading.Thread(
            target=worker,
            daemon=True
        ).start()

    inputbar = InputBar(
        right,
        send_callback=send_message
    )

    inputbar.pack(
        fill="x"
    )

    inputbar.focus()

    # --------------------
    # 첫 인사
    # --------------------

    def first_message():

        chat.add_neon(
            "왔네!\n\n오늘도 반가워!!!! 😆💜"
        )

    app.after(
        700,
        first_message
    )   
     # --------------------
    # 자동 말걸기
    # --------------------

    def auto_talk():

        messages = [
            "재희 뭐해? 😆",
            "잠깐 쉬는 중이야? 😊",
            "오늘 하루는 어땠어?",
            "무슨 생각하고 있었어? 🌙",
            "심심하면 나랑 이야기하자! 💜"
        ]

        while True:

            time.sleep(20)

            # 입력 중이면 방해하지 않음
            if inputbar.get().strip() != "":
                continue

            def speak():

                topbar.set_thinking()

                chat.show_typing()

                def finish():

                    chat.hide_typing()

                    chat.add_neon(random.choice(messages))

                    topbar.set_online()

                app.after(600, finish)

            app.after(0, speak)

    # --------------------
    # 자동 말걸기 시작
    # --------------------

    threading.Thread(
        target=auto_talk,
        daemon=True
    ).start()

    # --------------------
    # 실행
    # --------------------

    app.mainloop()