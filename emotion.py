# ==========================
# Project NEON Emotion System
# ==========================

happy = 50
energy = 80

last_category = ""


def add_happy(amount):
    global happy

    happy += amount

    if happy > 100:
        happy = 100


def remove_happy(amount):
    global happy

    happy -= amount

    if happy < 0:
        happy = 0


def add_energy(amount):
    global energy

    energy += amount

    if energy > 100:
        energy = 100


def remove_energy(amount):
    global energy

    energy -= amount

    if energy < 0:
        energy = 0