import json


def mergeTracks():
    files = ['tracks2.json', 'tracks1.json',
             'tracks.json']  # list all files generated from getTracks.py in reverse order
    with open(files[0], mode='r', encoding='utf-8') as f:
        tracks = json.load(f)  # load the last file
    for file in files[1:]:  # merge other files to the last one
        with open(file, mode='r', encoding='utf-8') as f:
            tmp = json.load(f)
        for genre in tracks:
            if genre in tmp:
                tracks[genre].update(tmp[genre])
    with open('alltracks.json', mode='w', encoding='utf-8') as f:
        json.dump(tracks, f)  # write data to file


if __name__ == '__main__':
    mergeTracks()
