import json
import csv

def json2csv(json_file, csv_file):
    with open(json_file, 'r') as f:
        data = json.load(f)


### Edit the fieldnames to separate the values by the headers of the json file
### this one specifically is tailored for my spotify data files
    with open(csv_file, 'w', newline = '') as f:
        writer = csv.DictWriter(f, fieldnames=["playlist_name", "last_modified_date", "song_name", "artist_name", "album_name", "track_uri", "added_date"])
        writer.writeheader()

        for playlist in data["playlists"]:
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

###Add the path of the files to convert here, or run the program moving directly
###the path where the json file is stored
json2csv('Playlist1.json', 'playlist.csv')