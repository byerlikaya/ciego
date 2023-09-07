import os
import datetime
import system.system_constans as system_constans
import shutil


class setup:
    def __init__(self, video, video_path, loop, motion_sensor):
        self.video = video
        self.video_path = video_path
        self.loop = loop
        self.motion_sensor = motion_sensor

# usb belleği sisteme dahil ediyor.


def usb_prepare():
    #print("----------------- " + system_constans.system_label + " " + system_constans.system_version + " -----------------")
    os.system("sudo umount {}".format(system_constans.dir_path))
    # os.system("lsblk")
    os.system("sudo mount /dev/sda {}".format(system_constans.dir_path))
    os.system("sudo mount /dev/sda1 {}".format(system_constans.dir_path))
    os.system("sudo mount /dev/sdb1 {}".format(system_constans.dir_path))
    os.system("sudo mount /dev/sdc1 {}".format(system_constans.dir_path))
    os.system("sudo mount /dev/sdd1 {}".format(system_constans.dir_path))
    os.system("sudo mount /dev/sde1 {}".format(system_constans.dir_path))
    os.system("sudo mount /dev/sdf1 {}".format(system_constans.dir_path))
    os.system("sudo mount /dev/sdg1 {}".format(system_constans.dir_path))
    os.system("sudo mount /dev/sdh1 {}".format(system_constans.dir_path))
    os.system("clear")
    # os.system("lsblk")
    #os.system("ls /mnt")

# kurulum dosyalarını kaydediyor.
def save_setting(self):

    directory_control()

    # seçilen video ya ait ayarları dosyaya yazdırıyoruz.
    file = open(system_constans.dir_path_video +
                "/video"+str(self.video+1)+".txt", "w+")

    video_name = self.video_path.replace(system_constans.dir_path, "")

    file.write(str(self.video)+"\n")  # 0
    file.write(video_name+"\n")  # 1

    shutil.copyfile(self.video_path,
                    "{}/{}".format(system_constans.dir_path_video, video_name))

    if self.loop.start_hour == 0 and self.loop.start_minute == 0:
        self.loop.start_hour = 0
        self.loop.start_minute = 0

    file.write(str(self.loop.start_hour)+"\n")  # 2
    file.write(str(self.loop.start_minute)+"\n")  # 3

    if self.loop.end_hour == 0 and self.loop.end_minute == 0:
        self.loop.end_hour = 0
        self.loop.end_minute = 0

    file.write(str(self.loop.end_hour)+"\n")  # 4
    file.write(str(self.loop.end_minute)+"\n")  # 5

    file.write(str(self.loop.minute)+"\n")  # 6

    file.write(str(self.motion_sensor)+"\n")  # 7
    file.close()
    print("Setting file saved.")
    save_job_restart(1)

# usb sürücüdeki video dosyalarının tam yolunu getirir.


def get_video_list_with_usb():
    video_list = []

    for path in os.listdir(system_constans.dir_path):
        file = os.path.join(system_constans.dir_path, path)
        if os.path.isfile(file):
            filename, file_extension = os.path.splitext(file)
            if file_extension != ".txt":
                video_list.append(file)

    return video_list


def get_video_list_with_local():
    video_list = []

    for path in os.listdir(system_constans.dir_path_video):
        file = os.path.join(system_constans.dir_path_video, path)
        if os.path.isfile(file):
            filename, file_extension = os.path.splitext(file)
            if file_extension != ".txt":
                video_list.append(file)

    return video_list

# usb sürücüdeki kurulum dosyalarının tam yolunu getirir.


def get_option_files():
    option_file_list = []

    directory_control()

    for path in os.listdir(system_constans.dir_path_video):
        file = os.path.join(system_constans.dir_path_video, path)
        if os.path.isfile(file):
            if path.startswith("video"):
                option_file_list.append(file)

    return option_file_list


def directory_control():
    # eğer usb bellek içerisinde ayar klasörü yok ise oluşturuyoruz.
    if os.path.exists(system_constans.dir_path_video) == False:
        os.mkdir(system_constans.dir_path_video)

    if os.path.exists(system_constans.dir_path_system_options_local) == False:
        os.mkdir(system_constans.dir_path_system_options_local)

    if os.path.exists(system_constans.dir_path_job_restart) == False:
        os.mkdir(system_constans.dir_path_job_restart)


def options_file_control():
    directory_control()

    if os.path.isfile("{}/options.txt".format(system_constans.dir_path_system_options_local)) == False:
        return False
    return True


def save_options(option):
    file = open(
        "{}/options.txt".format(system_constans.dir_path_system_options_local), "w+")

    file.write(option.language + "\n")

    file.write(str(option.start_hour) + "\n")
    file.write(str(option.start_minute) + "\n")

    file.write(str(option.end_hour) + "\n")
    file.write(str(option.end_minute) + "\n")

    file.close()
    print("Options file saved.")

def save_job_restart(status):
    directory_control()
    file = open("{}/job.txt".format(system_constans.dir_path_job_restart),"w+")
    file.write(str(status))
    file.close()
    print("Job restart status changed.")

def get_job_restart_status():
    file = open("{}/job.txt".format(system_constans.dir_path_job_restart))
    status=[]

    for f in file:
        status.append(f)
    
    file.close()

    return status

def get_system_options(option):
    options_file_control()
    file = open(
        "{}/options.txt".format(system_constans.dir_path_system_options_local))

    optionList = []

    for f in file:
        optionList.append(f)

    option.language = optionList[0]
    option.start_hour = optionList[1]
    option.start_minute = optionList[2]
    option.end_hour = optionList[3]
    option.end_minute = optionList[4]

    file.close()

    return option


def reset(reset):
    if reset:
        os.system("sudo rm -rf {}".format(system_constans.dir_path_video))
        print("Settings are reseted.")
        save_job_restart(1)
    else:
        pass


class job:
    video_path = ""
    start_time = datetime.time(0, 0, 0)
    end_time = datetime.time(0, 0, 0)
    repeat_minute = 0
    motion_sensor = False


def get_jobs():
    configs = []

    for option_file in get_option_files():
        config_infos = []
        file = open(option_file)
        for line in file:
            config_infos.append(line)
        file.close()
        configs.append(config_infos)

    job_list = []

    for config in configs:
        j = job()
        j.video_path = "{}/{}".format(system_constans.dir_path_video,
                                      config[1].strip())
        j.start_time = datetime.time(int(config[2]), int(config[3]), 0)
        j.end_time = datetime.time(int(config[4]), int(config[5]), 0)
        j.repeat_minute = int(config[6])
        j.motion_sensor = config[7].strip()
        job_list.append(j)

    return job_list
