import json
import csv
import os

def library_converter(json_file, csv_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

#Edit the fieldnames to separate the values by the headers of the json file
#this one specifically is tailored for my spotify data files

#2.0 now opens the file in "append" mode (a) to keep on adding items even after reading
#each file
    with open(csv_file, 'a', newline = '') as f:
        writer = csv.DictWriter(f, fieldnames=["type", "artist", "track_name", "album", "publisher", "uri"])
        if has_headers(csv_file) == False: writer.writeheader()

        for item in data["tracks"]:
            content_type = "song"
            artist_name = item["artist"]
            song_name = item["track"]
            album = item["album"]
            uri = item["uri"]

            writer.writerow({
                "type": content_type,
                "artist": artist_name,
                "track_name": song_name,
                "album": album,
                "uri": uri,
            })
        
        for item in data["albums"]:
            content_type = "album"
            artist_name = item["artist"]
            album = item["album"]
            uri = item["uri"]

            writer.writerow({
                "type": content_type,
                "artist": artist_name,
                "album": album,
                "uri": uri,
            })
        
        for item in data["shows"]:
            content_type = "podcast"
            name = item["name"]
            publisher = item["publisher"]
            uri = item["uri"]

            writer.writerow({
                "type": content_type,
                "artist": name,
                "publisher": publisher,
                "uri": uri,
            })

        for item in data["episodes"]:
            content_type = "episode"
            name = item["name"]
            show = item["show"]
            uri = item["uri"]
            
            writer.writerow({
                "type": content_type,
                "artist": show,
                "track_name": name,
                "uri": uri,
            })

        for item in data["artists"]:
            content_type = "artist"
            artist = item["name"]
            uri = item["uri"]
            
            writer.writerow({
                "type": content_type,
                "artist": artist,
                "uri": uri,
            })


def playlist_converter(json_file, csv_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    with open(csv_file, 'a', newline = '') as f:
        writer = csv.DictWriter(f, fieldnames=["playlist_name", "last_modified_date", "song_name", "artist_name", "album_name", "track_uri", "added_date"])
        if has_headers(csv_file) == False: writer.writeheader()

        playlists = data.get("playlists", [])
        #kept getting a keyError when using
        #for playlist in data["playlists"]
        #so i had to handle it with "data.get"
        
        for playlist in playlists:
            playlist_name = playlist["name"]
            playlist_last_modified = playlist["lastModifiedDate"]

            for item in playlist["items"]:
                track = item["track"]
                song_name = track["trackName"]
                artist_name = track["artistName"]
                album_name = track["albumName"]
                track_uri = track["trackUri"]
                added_date = item["addedDate"]

                writer.writerow({
                    "playlist_name": playlist_name,
                    "last_modified_date": playlist_last_modified,
                    "song_name": song_name,
                    "artist_name": artist_name,
                    "album_name": album_name,
                    "track_uri": track_uri,
                    "added_date": added_date,
                })



def history_converter(json_file, csv_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    with open(csv_file, 'a', newline = '') as f:
        writer = csv.DictWriter(f, fieldnames=["end_time", "artist_name", "track_name", "ms_played"])
        if has_headers(csv_file) == False: writer.writeheader()
        #writer.writerow(data)
        #tried to work this one out without typing it all but it didnt work
        #don't have enough time to look deeply into it
        
        for song in data:
            end_time = song["endTime"]
            artist = song["artistName"]
            track_name = song["trackName"]
            time_played = song["msPlayed"]

            writer.writerow({
                "end_time": end_time,
                "artist_name": artist,
                "track_name": track_name,
                "ms_played": time_played,
            })




def has_headers(csv_file):
    #reads the first row to know if there are headers
    #I assume that if it is a new file, first row
    #will be empty, so no need to check for characters
    with open(csv_file, 'r', newline = '') as f:
        reader = csv.reader(f)
        header = next(reader, None)

        if header == None:
            return False
        return True

#There is other content such as "banned tracks", "banned artists", and "other"
#but none came with my spotify data, so I don't know the structure of the object
#feel free to add it if you know said structure.




#Add the path of the files to convert here
folder_path = "/path/to/folder/my_spotify_data/MyData"

#Creating a list of all the filenames in the folder:
files = os.listdir(folder_path)

#Converting for all the files called Playlist (previous version just converted a single file)
#Same for all the files called library (my own spotify data only contained one; just in case.)
#And for all the files of your streaming history.

for file_name in files:
    if file_name.startswith("YourLibrary"):
        library_converter(os.path.join(folder_path, file_name), 'library.csv')

for file_name in files:
    if file_name.startswith("Playlist"):
        playlist_converter(os.path.join(folder_path, file_name), 'playlist.csv')

for file_name in files:
    if file_name.startswith("StreamingHistory"):    
        history_converter(os.path.join(folder_path, file_name), 'history.csv')

