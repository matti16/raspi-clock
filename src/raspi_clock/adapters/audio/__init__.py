import vlc

from raspi_clock.setting import AudioSettings

class SongPlayer():

    def __init__(self, filepath=AudioSettings.FILE_PATH):
        self.filepath = filepath
        self.player = vlc.MediaPlayer(filepath)
    
    def play(self):
        self.player.audio_set_volume(100)
        self.player.play()
    
    def stop(self):
        self.player.stop()
    
    def pause(self):
        self.player.stop()