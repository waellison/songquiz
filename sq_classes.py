import sys
import json
import random


class sq_song_database:
    songs = list()

    def decode_entry(self, db_entry):
        print(db_entry)

    def __init__(self, path="./database.json"):
        fh = open(path, "r")
        db = json.load(fh)
        for entry in db["songs"]:
            song = sq_song(entry)
            self.songs.append(song)

    def pick_song(self):
        subscr = random.randint(0, len(self.songs) - 1)
        song = self.songs[subscr]
        del self.songs[subscr]
        return song


class sq_song:
    title = ""
    artist = ""
    lines = None

    def __init__(self, dbentry):
        self.title = dbentry["title"]
        self.artist = dbentry["artist"]
        fh = open(dbentry["source"], "r")
        self.lines = fh.read().splitlines()

    def pick_lines(self, difficulty):
        retval = list()
        subscr = random.randint(0, len(self.lines) - (difficulty.context))
        for i in range(subscr, subscr + difficulty.context):
            retval.append(self.lines[i])
        return retval


class sq_game_difficulty:
    value = None
    context = 0
    diff_dict = {
        "easy": {"context": 4},
        "medium": {"context": 3},
        "hard": {"context": 2},
        "evil": {"context": 1}
    }

    def __init__(self):
        for diff in self.diff_dict:
            context = self.diff_dict[diff]["context"]
            line_str = " line" if context == 1 else " lines"

            print(diff + ": " + str(context) + line_str + " of context")

        while True:
            try:
                tmp = input("> ").lower()
                self.value = tmp
                self.context = self.diff_dict[tmp]["context"]
                break
            except KeyError:
                print("Invalid option, please try again.")
                continue
            except EOFError:
                sys.exit(0)
