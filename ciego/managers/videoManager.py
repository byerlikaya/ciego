import time
import vlc
import os
import hardware.displayRelay as display_relay

def start_video(video_path):  

    playing = set([1, 2, 3, 4])

    vlc_instance = vlc.Instance()

    player = vlc_instance.media_player_new()

    media = vlc_instance.media_new(video_path)

    player.set_media(media)

    player.audio_set_volume(100)    
    os.system("vcgencmd display_power 1")    
    os.system("clear")  

    display_relay.open()      
    time.sleep(2)
    player.play()
    os.system("clear") 
    time.sleep(2)
    os.system("clear") 

    while True:
        state = player.get_state()

        if state.value not in playing:
            os.system("clear")
            os.system("vcgencmd display_power 0") 
            
            display_relay.close()

            player.stop()                      
            break
        time.sleep(2)

    player.release()

    #print("Video Sonlandi..")
