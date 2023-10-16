from threading import Thread, active_count
from ytmusicapi import YTMusic
from time import sleep
from tqdm import tqdm
import yt_dlp

class YoutubeMusic:
    def __init__(self):
        self.ytm = YTMusic()
        self.base_url = "https://www.youtube.com/watch?v="
        self.ydl = yt_dlp.YoutubeDL({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'outtmpl': 'downloads/%(id)s-%(title)s.%(ext)s',
            'quiet': True
        })

    def search(self, track):
        query = track["name"] + " - "
        for artist in track["artists"]:
            query += artist + ", "
        results = self.ytm.search(query, filter="songs")
        for item in results:
            try:
                if item["duration_seconds"] == track["duration"]:
                    track["yid"] = item["videoId"]
                    return
            except KeyError:
                continue
        for item in results:
            try:
                for artist in item["artists"]:
                    if artist["name"] in track["artists"]:
                        track["yid"] = item["videoId"]
                        return
            except KeyError:
                continue
        print("Failed to find id for item:", track["name"])

    def threaded_search(self, tracks, num_threads=10):
        for track in tqdm(tracks):
            while active_count() > num_threads-2: sleep(0.5)
            Thread(target=self.search, args=(track,)).start()
            while active_count() <= 2: sleep(1)

    def download(self, tracks, num_threads=10):
        for track in tqdm(tracks, position=1):
            while active_count() > num_threads-2: sleep(0.5)
            Thread(target=self.ydl.download, args=(self.base_url + track["yid"],)).start()
            while active_count() <= 2: sleep(1)