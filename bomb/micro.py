# Imports go at the top
from microbit import *
import time
import log
import music

def format_fives(num_fives: int) -> str:
    """
    Produce a string of '5's grouped in fives, separated by colons.

    Parameters:
        num_fives (int): The total number of '5's to include in the output.

    Returns:
        str: A string of '5's in groups of five, separated by colons.
    """
    fives_str = '5' * num_fives + '0' * (25 - num_fives)
    # Slice the string into chunks of 5, and join them with colons
    formatted_str = ':'.join(fives_str[i:i+5] for i in range(0, len(fives_str), 5))
    log.add({"formatted": formatted_str})
    return formatted_str

def get_button_presses(button) -> int:
    if button == "A":
        if button_b.get_presses() > 0:
            return 0
        return button_a.get_presses() or 0
    if button == "B":
        if button_a.get_presses() > 0:
            return 0
        return button_b.get_presses() or 0
    return 0

minutes_left:int = 25
start_time = time.ticks_ms()
code = [("A", 4), ("B", 2), ("A", 3)]
code_entry_step:int = 0

cycles = 0
while True:
    if pin_logo.is_touched():
        break

    display.show("welcome to the party! "[cycles % 22])
    sleep(142)
    cycles += 1
music.pitch(200, 1000)

# Code in a 'while True:' loop repeats forever
while True:
    seconds_left = (26 * 60) - int((time.ticks_ms() - start_time) // 1000)
    minutes_left = int(seconds_left / 60)

    # seconds_left = seconds_left - 1530
    if seconds_left < 10:
        for i in range(9):
            display.show(str(9 - i))
            music.pitch(200, 1000)
            sleep(800)
        while True:
            display.show("BANG! ")
    
    log.add({"minutes_left": minutes_left, "seconds_left": seconds_left})
    display.show(Image(format_fives(minutes_left)))
    sleep(2900)

    if button_a.was_pressed() or button_b.was_pressed():
        button, presses = code[code_entry_step]
        button_presses = get_button_presses(button)
        if button_presses == presses:
            code_entry_step = code_entry_step + 1
            display.show(Image.YES)
            music.play(music.POWER_UP)
            sleep(1000)
            if code_entry_step == len(code):
                break
        else:
            code_entry_step = 0
            display.show(Image.NO)
            music.play(music.POWER_DOWN)
    else:
        display.show(Image('99999:99999:99999:99999:99999'))
        music.pitch(2000, 100)

while True:
    display.show("DIFFUSED ")
