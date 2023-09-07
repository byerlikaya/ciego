import RPi.GPIO as GPIO
import time
import managers.fileManager as fileManager
import menu.menu_step as menu_step
import system.system_gpio as system_gpio
import system.system_constans as system_constans
import hardware.lcdDriver as lcdDriver
import os
#import datetime

# usb sisteme dahil ediliyor ve içeriği listeleniyor.
fileManager.usb_prepare()

GPIO.setmode(GPIO.BCM)

GPIO.setup(system_gpio.BTN_OK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(system_gpio.BTN_YES, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(system_gpio.BTN_NO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(system_gpio.BTN_BACK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(system_gpio.BTN_RESET, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# okunuyor ve dosya yolu listesi alınıyor.
video_list = fileManager.get_video_list_with_usb()

if len(video_list) == 0:
    video_list = fileManager.get_video_list_with_local()


class loop:
    step = 1
    start_hour = 0
    start_minute = 0
    end_hour = 0
    end_minute = 0
    minute = 0


loop = loop()

option = menu_step.option()


def create():
    if fileManager.options_file_control():
        savedOption = fileManager.get_system_options(option)
        option.language = savedOption.language.replace("\n", "")
        option.start_hour = int(savedOption.start_hour)
        option.start_minute = int(savedOption.start_minute)
        option.end_hour = int(savedOption.end_hour)
        option.end_minute = int(savedOption.end_minute)
        create_menu(system_constans.menu_step_startup,
                    0, False, False, False, 1)
    else:
        create_menu(system_constans.menu_step_system,
                    0, False, False, False, 1)


def create_menu(step, video_index, motion_sensor, save, reset, time_step):
    lcdDriver.clear()
    while True:
        os.system("clear") 
        menu_step.label_info()
        menu_step.time_info()
        # Başlangıç
        if step == system_constans.menu_step_startup:
            menu_step.step_startup(option)
        # Video Seçimi
        elif step == system_constans.menu_step_video:
            if len(video_list) > 0:
                contents = fileManager.get_jobs()
                video_setup = False
                for content in contents:
                    cvideo = content.video_path.replace(system_constans.dir_path,"").replace(system_constans.dir_path_video,"").replace("//","/")
                    vvideo = video_list[video_index].replace(system_constans.dir_path,"").replace(system_constans.dir_path_video,"")
                    if cvideo == vvideo:
                        video_setup = True
                menu_step.step_video(option, str(
                    video_list[video_index]), video_index+1, len(video_list), video_setup)
            else:
                step = 100000
        # Hareket Sensörü
        elif step == system_constans.menu_step_motion_sensor:
            menu_step.step_motion_sensor(motion_sensor)
        # Döngü Ayarı
        elif step == system_constans.menu_step_loop:
            menu_step.step_loop(option, loop, time_step)
        # Kaydet
        elif step == system_constans.menu_step_save_option:
            menu_step.step_save_option(option, save)
        # Sistem
        elif step == system_constans.menu_step_system:
            menu_step.step_system(option, time_step)
        # Reset
        elif step == system_constans.menu_step_reset:
            menu_step.step_reset(option, reset)
        else:
            if save == True:
                fm = fileManager.setup(
                    video_index, video_list[video_index], loop, motion_sensor)
                fileManager.save_setting(fm)
            create()

        button_ok_click(step, video_index, motion_sensor,
                        save,  reset, time_step)

        button_yes_click(step, video_index,  motion_sensor,
                         save,  reset, time_step)

        button_no_click(step, video_index,   motion_sensor,
                        save,  reset, time_step)

        button_back_click(step, video_index, motion_sensor,
                          save,  reset, time_step)

        button_reset_click(reset)


def button_ok_click(step, video_index, motion_sensor, save,  reset, time_step):
    if GPIO.input(system_gpio.BTN_OK) == GPIO.HIGH:
        time.sleep(0.1)
        if step == system_constans.menu_step_system:
            if option.step == 0:
                # fileManager.save_options(option)
                option.step += 1
                create_menu(step, video_index, motion_sensor,
                            save,  reset, time_step)
            elif option.step <= 2 and time_step == 1:
                time_step += 1
                create_menu(step, video_index, motion_sensor,
                            save,  reset, time_step)
            elif option.step < 2 and time_step == 2:
                time_step = 1
                option.step += 1
                create_menu(step, video_index, motion_sensor,
                            save,  reset, time_step)
            else:
                fileManager.save_options(option)
                time_step = 1
                option.step = 0
                create()
        elif step == system_constans.menu_step_reset:
            fileManager.reset(reset)
            create()
        else:
            if step != system_constans.menu_step_loop:
                step += 1
            elif step == system_constans.menu_step_loop and (loop.step == 1 or loop.step == 2) and time_step == 2:
                loop.step += 1
                time_step = 1
            elif step == system_constans.menu_step_loop and (loop.step == 1 or loop.step == 2) and time_step == 1:
                time_step += 1
            else:
                loop.step = 1
                time_step = 1
                step += 1
            create_menu(step, video_index, motion_sensor,
                        save,  reset, time_step)


def button_back_click(step, video_index, motion_sensor, save,  reset, time_step):
    if GPIO.input(system_gpio.BTN_BACK) == GPIO.HIGH:
        if step == system_constans.menu_step_system:
            if option.step == 0:
                pass
            elif (option.step == 1 or option.step == 2) and time_step == 1:
                option.step -= 1
            elif (option.step == 1 or option.step == 2) and time_step == 2:
                time_step -= 1
            create_menu(step, video_index, motion_sensor,
                        save,  reset, time_step)
        else:
            time.sleep(0.1)
            if step != system_constans.menu_step_loop:
                step -= 1
            elif step == system_constans.menu_step_loop and loop.step > 1:
                loop.step -= 1
            elif step == system_constans.menu_step_loop and time_step > 1:
                time_step -= 1
            else:
                loop.step = 1
                step -= 1
            create_menu(step, video_index, motion_sensor,
                        save,  reset, time_step)


def button_yes_click(step, video_index, motion_sensor, save,  reset, time_step):
    if GPIO.input(system_gpio.BTN_YES) == GPIO.HIGH:
        time.sleep(0.1)
        # her basımda sonraki videoya geçiş sağlanıyor.
        if step == system_constans.menu_step_video:
            video_index += 1
            if video_index < len(video_list):
                time.sleep(0.5)
                create_menu(step, video_index, motion_sensor,
                            save,  reset, time_step)
            else:
                video_index -= 1
        # hareket sensörü aktif ediliyor
        elif step == system_constans.menu_step_motion_sensor:
            create_menu(step, video_index, True, save,
                        reset, time_step)
        # döngü ayarında saat seçimi yaptırılıyor
        elif step == system_constans.menu_step_loop:
            # başlangıç saati artırılıyor
            if loop.step == 1 and time_step == 1:
                if loop.start_hour <= 22:
                    loop.start_hour += 1
                else:
                    loop.start_hour = 0
            # başlangıç dakikası artırılıyor.
            elif loop.step == 1 and time_step == 2:
                if loop.start_minute <= 58:
                    loop.start_minute += 1
                else:
                    loop.start_minute = 0
            # bitiş saati artırılıyor.
            elif loop.step == 2 and time_step == 1:
                if loop.end_hour <= 22:
                    loop.end_hour += 1
                else:
                    loop.end_hour = 0
            # bitiş dakikası artırılıyor.
            elif loop.step == 2 and time_step == 2:
                if loop.end_minute <= 58:
                    loop.end_minute += 1
                else:
                    loop.end_minute = 0
            elif loop.step == 3:
                if loop.minute <= 55:
                    loop.minute += 1
                else:
                    loop.minute = 0
            create_menu(step, video_index, motion_sensor,
                        save,  reset, time_step)
        # kaydedilsin evet
        elif step == system_constans.menu_step_save_option:
            create_menu(step, video_index,   motion_sensor,
                        True,  reset, time_step)
        # dil seçimi yaptırılıyor.
        elif step == system_constans.menu_step_system:
            if option.step == 0:
                if option.language_step == 1:
                    option.language_step = 0
            elif option.step == 1:
                # başlangıç saati artırılıyor
                if time_step == 1:
                    if option.start_hour <= 22:
                        option.start_hour += 1
                    else:
                        option.start_hour = 0
                # başlangıç dakikası artırılıyor.
                elif time_step == 2:
                    if option.start_minute <= 58:
                        option.start_minute += 1
                    else:
                        option.start_minute = 0
            elif option.step == 2:
                # bitiş saati artırılıyor.
                if time_step == 1:
                    if option.end_hour <= 22:
                        option.end_hour += 1
                    else:
                        option.end_hour = 0
                # bitiş dakikası artırılıyor.
                elif time_step == 2:
                    if option.end_minute <= 58:
                        option.end_minute += 1
                    else:
                        option.end_minute = 0

            create_menu(step, video_index, motion_sensor,
                        save,  reset, time_step)
        # sistem reset
        elif step == system_constans.menu_step_reset:
            create_menu(step, video_index, motion_sensor,
                        save,  True, time_step)


def button_no_click(step, video_index,  motion_sensor, save,  reset, time_step):
    if GPIO.input(system_gpio.BTN_NO) == GPIO.HIGH:
        time.sleep(0.1)
        # her basımda önceki videoya geçiş sağlanıyor.
        if step == system_constans.menu_step_video:
            video_index -= 1
            if video_index >= 0:
                time.sleep(0.5)
                create_menu(step, video_index,   motion_sensor,
                            save,  reset, time_step)
            else:
                video_index += 1
        # hareket sensörü pasif ediliyor
        elif step == system_constans.menu_step_motion_sensor:
            create_menu(step, video_index, False, save,  reset, time_step)
        # döngü ayarında dakika seçimi yaptırılıyor
        elif step == system_constans.menu_step_loop:
            # başlangıç saati azaltılıyor
            if loop.step == 1 and time_step == 1:
                if loop.start_hour > 1:
                    loop.start_hour -= 1
                elif loop.start_hour == 0:
                    loop.start_hour = 23
                else:
                    loop.start_hour = 0
            # başlangıç dakikası azaltılıyor.
            elif loop.step == 1 and time_step == 2:
                if loop.start_minute > 0:
                    loop.start_minute -= 1
                elif loop.start_minute == 0:
                    loop.start_minute = 59
                else:
                    loop.start_minute = 0
            # bitiş saati azaltılıyor.
            elif loop.step == 2 and time_step == 1:
                if loop.end_hour > 1:
                    loop.end_hour -= 1
                elif loop.end_hour == 0:
                    loop.end_hour = 23
                else:
                    loop.end_hour = 0
            # bitiş dakikası artırılıyor.
            elif loop.step == 2 and time_step == 2:
                if loop.end_minute > 0:
                    loop.end_minute -= 1
                elif loop.end_minute == 0:
                    loop.end_minute = 59
                else:
                    loop.end_minute = 0
            elif loop.step == 3:
                if loop.minute > 1:
                    loop.minute -= 1
                else:
                    loop.minute = 0
            create_menu(step, video_index, motion_sensor,
                        save,  reset, time_step)
        # kaydedilsin hayır
        elif step == system_constans.menu_step_save_option:
            create_menu(step, video_index, motion_sensor,
                        False,  reset, time_step)
        # dil seçimi yaptırılıyor.
        elif step == system_constans.menu_step_system:
            if option.step == 0:
                if option.language_step == 0:
                    option.language_step = 1
            elif option.step == 1:
                # başlangıç saati azaltılıyor
                if time_step == 1:
                    if option.start_hour > 1:
                        option.start_hour -= 1
                    elif option.start_hour == 0:
                        option.start_hour = 23
                    else:
                        loop.start_hour = 0
               # başlangıç dakikası azaltılıyor.
                elif time_step == 2:
                    if option.start_minute > 0:
                        option.start_minute -= 1
                    elif option.start_minute == 0:
                        option.start_minute = 59
                    else:
                        option.start_minute = 0
            elif option.step == 2:
                # bitiş saati azaltılıyor.
                if option.step == 2 and time_step == 1:
                    if option.end_hour > 1:
                        option.end_hour -= 1
                    elif option.end_hour == 0:
                        option.end_hour = 23
                    else:
                        loop.end_hour = 0
                # bitiş dakikası artırılıyor.
                elif option.step == 2 and time_step == 2:
                    if option.end_minute > 0:
                        option.end_minute -= 1
                    elif option.end_minute == 0:
                        option.end_minute = 59
                    else:
                        option.end_minute = 0

            create_menu(step, video_index, motion_sensor,
                        save,  reset, time_step)
        # sistem reset
        elif step == system_constans.menu_step_reset:
            create_menu(step, video_index, motion_sensor,
                        save,  False, time_step)


def button_reset_click(reset):
    if GPIO.input(system_gpio.BTN_RESET) == GPIO.HIGH:
        time.sleep(0.1)
        create_menu(system_constans.menu_step_reset,
                    0, False, False,  reset, 1)
