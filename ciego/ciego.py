import managers.jobManager as jobManager
import menu.menu_creator as menu
import threading
import os
import time

os.system("vcgencmd display_power 0")
os.system("clear")

t1 = threading.Thread(target=jobManager.schedule_jobs)
t2 = threading.Thread(target=menu.create)

t1.start()
t2.start()
