import pygame
import os
import time

MUSIC_DIR = os.path.join(os.path.dirname(__file__), "music")

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.playlist = self._load_playlist()
        self.current_index = 0
        self.playing = False
        self.start_time = 0
        self.track_length = 10  # default seconds if unknown

    def _load_playlist(self):
        if not os.path.exists(MUSIC_DIR):
            os.makedirs(MUSIC_DIR)
        files = sorted([
            f for f in os.listdir(MUSIC_DIR)
            if f.endswith((".mp3", ".wav", ".ogg"))
        ])
        return files

    def _get_track_path(self):
        if not self.playlist:
            return None
        return os.path.join(MUSIC_DIR, self.playlist[self.current_index])

    def play(self):
        path = self._get_track_path()
        if path is None:
            return
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        self.playing = True
        self.start_time = time.time()
        # Try to get sound length
        try:
            sound = pygame.mixer.Sound(path)
            self.track_length = sound.get_length()
        except Exception:
            self.track_length = 30

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False

    def next_track(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        if self.playing:
            self.play()

    def prev_track(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        if self.playing:
            self.play()

    def get_current_track_name(self):
        if not self.playlist:
            return "No tracks found"
        return self.playlist[self.current_index]

    def get_playlist_names(self):
        return self.playlist if self.playlist else ["No tracks"]

    def get_status(self):
        if not self.playlist:
            return "No tracks"
        if self.playing and pygame.mixer.music.get_busy():
            return "Playing"
        elif self.playing:
            self.playing = False
            return "Stopped"
        return "Stopped"

    def get_progress(self):
        if not self.playing or not pygame.mixer.music.get_busy():
            return 0.0
        elapsed = time.time() - self.start_time
        if self.track_length > 0:
            return min(elapsed / self.track_length, 1.0)
        return 0.0

    def get_position_str(self):
        if not self.playing:
            return "0:00 / 0:00"
        elapsed = int(time.time() - self.start_time)
        total = int(self.track_length)
        def fmt(s): return f"{s//60}:{s%60:02d}"
        return f"{fmt(elapsed)} / {fmt(total)}"