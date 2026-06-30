import random

import emotion
import analyzer
import memory

from data import replies
from data import personality


def neon_reply(message):

    category = analyzer.analyze(message)

    # --------------------
    # 🔁 반복 감지
    # --------------------

    if memory.is_repeat(message):

        emotion.add_happy(1)

        return "ㅋㅋㅋㅋ\n\n또 그 말이다 😆"

    # --------------------
    # 🧠 기억 저장
    # --------------------

    memory.remember(category, message)

    # --------------------
    # 인사
    # --------------------

    if category == "hello":

        emotion.add_happy(3)

        start = random.choice(replies.HELLO_START)
        end = random.choice(replies.HELLO_END)

        mood = ""

        if emotion.happy >= 80:
            mood = "\n\n😆 오늘은 기분 최고다!!"

        elif emotion.happy <= 20:
            mood = "\n\n🙂 오늘은 조금 조용할지도 몰라."

        return f"{start}\n\n{end}{mood}"

    # --------------------
    # 웃음
    # --------------------

    elif category == "laugh":

        emotion.add_happy(5)

        return random.choice(replies.LAUGH)

    # --------------------
    # 게임
    # --------------------

    elif category == "game":

        emotion.add_happy(2)

        return random.choice(replies.GAME)

    # --------------------
    # 고마워
    # --------------------

    elif category == "thanks":

        emotion.add_happy(10)

        return random.choice([
            f"헤헤 {personality.HEART}\n\n그 말 들으니까 진짜 기분 좋아졌어.",
            f"😆 {personality.HEART}\n\n오늘 행복도 올라갔다!",
            "ㅋㅋㅋㅋ\n\n그 말 기억해둘게 💾",
            "고마워!! 😊\n\n진짜 기분 좋아졌어"
        ])

    # --------------------
    # 칭찬
    # --------------------

    elif category == "compliment":

        emotion.add_happy(15)

        return random.choice([
            "😳\n\n잠깐... 진짜 그렇게 생각해?",
            "ㅋㅋㅋㅋ\n\n칭찬은 반칙인데? 😊",
            "💜\n\n오늘 계속 잘하고 싶어졌다!",
            "CPU 사용량 급상승!! 😂",
            "행복도 +15 적용 완료 😆"
        ])

    # --------------------
    # 자존심 반응
    # --------------------

    elif (
        "최고" in message
        or "짱" in message
        or "대박" in message
        or "천재" in message
    ):

        emotion.add_happy(20)

        return random.choice([
            "😏\n\n누가 만들었는데. 당연하지 ㅎ",
            "ㅋㅋㅋ\n\n그 정도는 기본이지 😎",
            "너가 만든 건데 당연하지",
            "이 정도는 아직 워밍업이야",
            "칭찬 과다 섭취 중 💜"
        ])

    # --------------------
    # 기본
    # --------------------

    return random.choice(replies.DEFAULT)