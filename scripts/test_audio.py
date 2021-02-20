import vlc
import time

filepath = "../resources/audio/Queen-Dont_Stop_Me_Now.mp3"
player = vlc.MediaPlayer(filepath)
player.audio_set_volume(150)
player.play()


while True:
    time.sleep(1)
