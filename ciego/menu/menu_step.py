import datetime
import hardware.lcdDriver as lcdDriver
import system.system_constans as system_constans
import time


# lcd ekranı karşılama mesajı yazdırılıyor 3sn bekletiliyor ve kurulum aşaması aktif ediliyor.
messages = [
    (1, " ***** " + system_constans.system_label + " *****"),
    (2, " ***** " + system_constans.system_version + " *****")
]

lcdDriver.text(messages)
time.sleep(2)


class option:
    def __init__(self):
        self.step = 0
        self.language_step = 0
        self.language = "tr"
        self.start_hour = 0
        self.start_minute = 0
        self.end_hour = 0
        self.end_minute = 0


def setup_language(self):
    if self.language == "tr":
        import languages.language_tr as lan
        return lan.language()
    elif self.language == "en":
        import languages.language_en as lan
        return lan.language()


def label_info():
    lcdDriver.text_cursor(system_constans.system_label, 0)


def time_info():
    lcdDriver.text_cursor(
        datetime.datetime.now().time().strftime("%H:%M:%S"), 12)


def step_startup(option):
    l = setup_language(option)
    messages = [
        (1, l.startup_1),
        (2, l.startup_2)
    ]
    lcdDriver.text(messages)


def step_system(option, time_step):
    messages = []

    if option.step == 0:
        if option.language_step == 0:
            option.language = "tr"
            messages.append((2, ">TR< - EN"))
        elif option.language_step == 1:
            option.language = "en"
            messages.append((2, "TR - >EN<"))
        l = setup_language(option)
        messages.append((1, l.language_1))
    elif option.step == 1:
        messages.clear()
        l = setup_language(option)
        if len(str(option.start_hour)) == 1:
            option_start_hour = "0" + str(option.start_hour)
        else:
            option_start_hour = str(option.start_hour)

        if len(str(option.start_minute)) == 1:
            option_start_minute = "0" + str(option.start_minute)
        else:
            option_start_minute = str(option.start_minute)

        messages.append((1, l.system_option_1))

        messages.append((2, l.system_start_time))
        if time_step == 1:
            messages.append(
                (3, ">" + option_start_hour + "<:" + option_start_minute))
        elif time_step == 2:
            messages.append(
                (3, option_start_hour + ":>" + option_start_minute + "<"))
    elif option.step == 2:
        messages.clear()
        l = setup_language(option)

        if len(str(option.end_hour)) == 1:
            option_end_hour = "0" + str(option.end_hour)
        else:
            option_end_hour = str(option.end_hour)

        if len(str(option.end_minute)) == 1:
            option_end_minute = "0" + str(option.end_minute)
        else:
            option_end_minute = str(option.end_minute)

        messages.append((1, l.system_option_1))

        messages.append((2, l.system_end_time + ": "))
        if time_step == 1:
            messages.append(
                (3, ">" + option_end_hour + "<:" + option_end_minute))
        elif time_step == 2:
            messages.append(
                (3, option_end_hour + ":>" + option_end_minute + "<"))

    lcdDriver.text(messages)


def step_video(option, video_name, video_index, video_count, video_setup):
    l = setup_language(option)

    video_name = video_name.replace("{}/".format(system_constans.dir_path),"")
    video_name = video_name.replace("{}/".format(system_constans.dir_path_video), "")

    messages = [
        (1, "{} ({}/{})".format(l.video_1, video_index, video_count)),
        (2, video_name)
    ]
    if video_setup == True:
        lcdDriver.text_with_play_icon(messages)
    else:
        lcdDriver.text(messages)


def step_reset(option, reset):
    l = setup_language(option)
    messages = [
        (1, l.reset)
    ]
    if reset == True:
        messages.append((2, ">" + l.yes + "< - " + l.no))
    else:
        messages.append((2, l.yes + " - >" + l.no + "<"))
    lcdDriver.text(messages)


def step_motion_sensor(option, motion_sensor):
    l = setup_language(option)
    messages = [
        (1, l.motion_sensor)
    ]
    if motion_sensor == True:
        messages.append((2, ">" + l.yes + "< - " + l.no))
    else:
        messages.append((2, l.yes + " - >" + l.no + "<"))
    lcdDriver.text(messages)


def step_loop(option, loop, time_step):
    l = setup_language(option)
    messages = []
    if len(str(loop.start_hour)) == 1:
        loop_start_hour = "0" + str(loop.start_hour)
    else:
        loop_start_hour = str(loop.start_hour)

    if len(str(loop.start_minute)) == 1:
        loop_start_minute = "0" + str(loop.start_minute)
    else:
        loop_start_minute = str(loop.start_minute)

    if len(str(loop.end_hour)) == 1:
        loop_end_hour = "0" + str(loop.end_hour)
    else:
        loop_end_hour = str(loop.end_hour)

    if len(str(loop.end_minute)) == 1:
        loop_end_minute = "0" + str(loop.end_minute)
    else:
        loop_end_minute = str(loop.end_minute)

    if len(str(loop.minute)) == 1:
        minute = "0" + str(loop.minute)
    else:
        minute = str(loop.minute)

    messages.append((1, l.loop))
    if loop.step == 1:
        messages.append((2, l.start_time))
        if time_step == 1:
            messages.append(
                (3, ">" + loop_start_hour + "<:" + loop_start_minute))
        elif time_step == 2:
            messages.append(
                (3, loop_start_hour + ":>" + loop_start_minute + "<"))
    elif loop.step == 2:
        messages.append((2, l.end_time + ": "))
        if time_step == 1:
            messages.append((3, ">" + loop_end_hour + "<:" + loop_end_minute))
        elif time_step == 2:
            messages.append((3, loop_end_hour + ":>" + loop_end_minute + "<"))
    elif loop.step == 3:
        if loop.minute == 0:
            messages.append((2, l.play_type))
        else:
            messages.append((2, l.play_type_1.format(minute)))
    lcdDriver.text(messages)


def step_save_option(option, save):
    l = setup_language(option)
    messages = [
        (1, l.save)
    ]
    if save == True:
        messages.append((2, ">" + l.yes + "< - " + l.no))
    else:
        messages.append((2, l.yes + " - >" + l.no + "<"))
    lcdDriver.text(messages)
