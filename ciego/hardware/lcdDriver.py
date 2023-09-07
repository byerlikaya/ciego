import time
from RPLCD.i2c import CharLCD
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=20, rows=4, dotsize=8,
              charmap='A02',
              auto_linebreaks=True,
              backlight_enabled=True)


def text_cursor(messeage, cursor_pos):
    lcd.cursor_pos = (0, cursor_pos)
    lcd.write_string(messeage[0:40])
    time.sleep(0.02)


def text_with_play_icon(messages):
    play = (0b10000,
            0b11000,
            0b11100,
            0b11110,
            0b11100,
            0b11000,
            0b10000,
            0b00000)
    lcd.create_char(0, play)
    index = 0
    for message in messages:
        lcd.cursor_pos = (message[0], 0)
        if index == 1:
            lcd.write_string(("\x00" + message[1])[0:40])
        else:
            lcd.write_string(message[1][0:40])
        index+=1

    time.sleep(0.02)


def text(messages):
    for message in messages:
        lcd.cursor_pos = (message[0], 0)
        lcd.write_string(message[1][0:40])
    time.sleep(0.02)


def clear():
    lcd.clear()
