from threading import Thread, active_count
import eyed3
from tqdm import tqdm
from time import sleep
from os import listdir
from os.path import isfile, join

def add_metadata(track):
    try:
        files = [f for f in listdir("downloads") if f.startswith(track["yid"])]
        if len(files) > 1:
            raise ValueError("Found two files with the same ID!")

        file = eyed3.load(join("downloads", files[0]))
        file.tag.title = track["name"]
        file.tag.artist = ";".join(track["artists"], )
        file.tag.album = track["album"]["name"]
        file.tag.album_artist = ";".join(track["album"]["artists"])
        file.tag.track_num = track["track_number"]
        file.tag.save()
    except KeyError:
        return
    


def threaded_add_metadata(tracks, num_threads=10):
    for track in tqdm(tracks):
        while active_count() > num_threads-2: sleep(0.5)
        Thread(target=add_metadata, args=(track,)).start()
    while active_count() <= 2: sleep(1)
