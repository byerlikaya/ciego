#import os
import schedule
import time
import datetime
import managers.fileManager as fileManager
import managers.videoManager as videoManager

scheduler1 = schedule.Scheduler()
scheduler2 = schedule.Scheduler()


def schedule_jobs():

    scheduler1.clear()
    scheduler2.clear()

    # print("-----------------------------------------------")
    # os.system("sudo date")

    for jb in fileManager.get_jobs():
        # print("-----------------------------------------------")
        # print("video path : " + jb.video_path)
        # print("start time : " + jb.start_time.strftime("%H:%M"))
        # print("end time : " + jb.end_time.strftime("%H:%M"))
        # print("repeat minute : " + str(jb.repeat_minute))
        # print("motion sensor : " + jb.motion_sensor)

        # print(datetime.datetime.now().time())

        nowTime = datetime.datetime.now().time()

        now = datetime.datetime.now()
        delta = datetime.timedelta(seconds=2)
        now_Time = (datetime.datetime.combine(
            datetime.date(1, 1, 1), now.time()) + delta).time()

        if jb.start_time == jb.end_time:
            if jb.start_time >= nowTime and jb.end_time >= nowTime:
                scheduler1.every().day.at(now_Time.strftime("%H:%M:%S")).do(setup_job, sjb=jb)
            else:
                scheduler1.every().day.at(jb.start_time.strftime("%H:%M")).do(setup_job, sjb=jb)
        else:
            if jb.start_time <= nowTime and nowTime <= jb.end_time:
                scheduler1.every().day.at(now_Time.strftime("%H:%M:%S")).do(setup_job, sjb=jb)
            else:
                scheduler1.every().day.at(jb.start_time.strftime("%H:%M")).do(setup_job, sjb=jb)

    while True:
        scheduler1.run_pending()
        scheduler2.run_pending()
        if job_restart_control() == True:
            job_restart()
            break
        time.sleep(1)

    time.sleep(1)
    schedule_jobs()


def setup_job(sjb):
    if sjb.repeat_minute == 0:
        # bitiş saatine kadar sürekli oynat
        if sjb.motion_sensor == False:
            scheduler2.every().second.until(sjb.end_time.strftime(
                "%H:%M")).do(video_job, video_path=sjb.video_path)
        else:
            scheduler2.every().second.until(sjb.end_time.strftime("%H:%M")).do(
                video_job_motion_sensor, video_path=sjb.video_path)
    else:
        # bitiş saatine kadar her x dakikada bir oynat
        if sjb.motion_sensor == False:
            scheduler2.every(sjb.repeat_minute).minutes.until(
                sjb.end_time.strftime("%H:%M")).do(video_job, video_path=sjb.video_path)
        else:
            scheduler2.every(sjb.repeat_minute).minutes.until(sjb.end_time.strftime(
                "%H:%M")).do(video_job_motion_sensor, video_path=sjb.video_path)
    # return scheduler1.cancel_job(scheduler1)


def video_job(video_path):
    # print("-----------------------------------------------")
    # print(video_path + " is playing")
    # print(str(datetime.datetime.now()))
    videoManager.start_video(video_path)


def video_job_motion_sensor(video_path):
    # print("-----------------------------------------------")
    # print(video_path + " is playing (motion_sensor)")
    # print(str(datetime.datetime.now()))
    videoManager.start_video(video_path)


def cancel_all_jobs():
    schedule.clear()
    scheduler1.clear()
    scheduler2.clear()


def job_restart_control():
    status = fileManager.get_job_restart_status()
    time.sleep(1)
    if len(status) > 0:
        if status[0] == "1":
            return True
        return False
    return False


def job_restart():
    fileManager.save_job_restart(0)
    print("Jobs restart")
