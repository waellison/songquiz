import sys
import json
import random
from tr import tr


def make_match_candidate(string):
    punct = "!$&()-\"\';:,./?"
    articles = ["a", "an", "the", "but", "and", "or"]
    tmp = string

    # Remove common punctuation from candidate strings
    tmp = tr(punct, "", tmp, 'd')

    # Now remove articles and conjunctions from candidate strings
    tmp_words = tmp.split()
    for a_word in articles:
        for s_word in tmp_words:
            if s_word.lower() == a_word and len(tmp_words) > 1:
                tmp_words.remove(s_word)

    # And return the result
    return " ".join(tmp_words)


class sq_song_database:
    songs = list()

    def decode_entry(self, db_entry):
        print(db_entry)

    def __init__(self, path="./database.json"):
        """Create a new song database.

        Keyword argument:
        path -- the pathname a JSON database (defaults to './database.json')
        """
        fh = open(path, "r")
        db = json.load(fh)
        fh.close()
        for entry in db["songs"]:
            song = sq_song(entry)
            self.songs.append(song)

    def pick_song(self):
        """Pick a random song from the database.

        Then remove it from the database and return it to the caller.
        """
        subscr = random.randint(0, len(self.songs) - 1)
        song = self.songs[subscr]
        del self.songs[subscr]
        return song


class sq_song:
    info = None
    lines = None

    def __init__(self, dbentry):
        """Create a new song object, and read the lyrics from disk.

        Argument:
        dbentry -- the database entry referring to this song
        """
        self.info = dict()
        self.info["title"] = dbentry["title"]
        self.info["artist"] = dbentry["artist"]
        fh = open(dbentry["source"], "r")
        self.lines = fh.read().splitlines()
        fh.close()

    def pick_lines(self, difficulty):
        """Pick random lines from the song lyrics.

        Takes into account the passed difficulty level and returns the
        chosen lines in a list.

        Argument:
        difficulty -- the sq_difficulty object representing the active difficulty level
        """
        retval = list()
        subscr = random.randint(0, len(self.lines) - (difficulty.context))
        for i in range(subscr, subscr + difficulty.context):
            retval.append(self.lines[i])
        return retval

    def loose_match(self, other, which):
        try:
            thing = self.info[which]
        except KeyError:
            return False

        match_str = make_match_candidate(thing)
        candidate_str = make_match_candidate(other)

        return match_str == candidate_str


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
