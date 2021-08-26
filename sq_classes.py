import sys
import json
import random
from tr import tr
from functools import reduce


class sq_util:
    @staticmethod
    def make_match_candidate(string):
        """
        Prepare a string for fuzzy matching.

        Removes punctuation, articles, and conjunctions to allow for some
        measure of leniency in matching user input.

        Argument:
        string: the string to operate on

        Returns: the match candidate string with punctuation, articles, and
        conjunctions removed
        """
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

    feedbacks = {
        "perfect":
        ["Excellent!",
         "Awesome!",
         "Nailed it!",
         "Ding-ding-ding!",
         "You got it!"],
        "title":
        ["You got the song, but not the artist.",
         "You knew the song, just not who sang it.",
         "Nice, you got the title."],
        "artist":
        ["You got the artist, but not the title.",
         "You knew the singer, just not the name of the song.",
         "Nice, you got the artist."],
    }


class sq_song_database:
    songs = list()

    def decode_entry(self, db_entry):
        print(db_entry)

    def __init__(self, path="./database.json"):
        """
        Create a new song database.

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
        """
        Pick a random song from the database.

        Then remove it from the database and return it to the caller.
        """
        subscr = random.randint(0, len(self.songs) - 1)
        song = self.songs[subscr]
        del self.songs[subscr]
        return song


class sq_song:
    info = None
    lines = None
    avg_line_len = 0

    def __init__(self, dbentry):
        """
        Create a new song object, and read the lyrics from disk.

        Argument:
        dbentry -- the database entry referring to this song
        """
        self.info = dict()
        self.info["title"] = dbentry["title"]
        self.info["artist"] = dbentry["artist"]
        fh = open(dbentry["source"], "r")
        self.lines = fh.read().splitlines()
        linecount = len(self.lines)
        self.avg_line_len = int(reduce(
            (lambda x, y: x + y), map(lambda str: len(str), self.lines)) / linecount)
        fh.close()

    def pick_lines(self, difficulty):
        """
        Pick random lines from the song lyrics.

        Takes into account the passed difficulty level and returns the
        chosen lines in a list.

        Argument:
        difficulty -- the sq_difficulty object representing the active difficulty level
        """
        retval = list()
        subscr = None

        while True:
            tmp = random.randint(0, len(self.lines) - difficulty.context)
            if len(self.lines[tmp]) >= self.avg_line_len:
                subscr = tmp
                break

        for i in range(subscr, subscr + difficulty.context):
            retval.append(self.lines[i])
        return retval

    def loose_match(self, other, which):
        """
        Test for a loose match between input and what is in memory.

        Removes punctuation, conjunctions, and articles from the song
        title and user input, and test for equality.

        Arguments:
        other: the string to compare
        which: which attribute to compare (valid values are keys in self.info)

        Returns:
        True if the loose match is equal, False otherwise
        """
        try:
            thing = self.info[which]
        except KeyError:
            return False

        match_str = sq_util.make_match_candidate(thing)
        candidate_str = sq_util.make_match_candidate(other)

        return match_str.lower() == candidate_str.lower()


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
        print("\nSelect your difficulty:\n")
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


class sq_game:
    difficulty = None
    db = None
    scores = {
        "artist": 5,
        "title": 5
    }
    max_question_score = 0
    max_count = 0
    max_score = 0
    current_score = 0

    def __init__(self, filename="./database.json"):
        self.db = sq_song_database(filename)
        self.max_question_score = reduce(
            (lambda x, y: x + y), self.scores.values())
        print(f"database loaded: {str(len(self.db.songs))} songs present")

    def get_max_count(self):
        while True:
            try:
                self.max_count = int(
                    input(f"How many? (max {len(self.db.songs)}) > "))
                break
            except ValueError:
                self.max_count = len(self.db.songs)

    def run(self):
        count = 0
        self.difficulty = sq_game_difficulty()
        print(f"\"{self.difficulty.value.title()}\" difficulty chosen\n")
        print("Scoring is as follows:")
        for k, v in self.scores.items():
            print(f"\t{v} points per correct {k}")
        self.get_max_count()
        self.max_score = self.max_count * self.max_question_score
        while count < self.max_count:
            this_question_score = self.do_question()
            self.current_score += this_question_score
            count += 1
            what = "song" if self.max_count - count == 1 else "songs"
            remains = "remains" if self.max_count - count == 1 else "remain"
            print(
                f"{this_question_score} points added to your score.  {self.max_count - count} {what} {remains}.")
            print(
                f"Current score: {str(self.current_score)}/{str(self.max_score)}\n")
        print("Final score:", str(self.current_score) + "/" + str(self.max_score))

    def do_question(self):
        songinfo = {
            "artist": {"guess": str(), "correct?": False},
            "title":  {"guess": str(), "correct?": False}
        }

        this_question_score = 0

        try:
            song = self.db.pick_song()
            for line in song.pick_lines(self.difficulty):
                print(line)
        except ValueError:
            return None

        try:
            for key in songinfo.keys():
                songinfo[key]["guess"] = input(f"Guess the {key}! > ")
        except EOFError:
            return None

        for key in songinfo.keys():
            if song.loose_match(songinfo[key]["guess"], key) is True:
                songinfo[key]["correct?"] = True
                this_question_score += self.scores[key]

        if this_question_score == self.max_question_score:
            print(random.choice(sq_util.feedbacks["perfect"]))
        else:
            for key in songinfo.keys():
                if songinfo[key]["correct?"] is True:
                    print(random.choice(sq_util.feedbacks[key]))
                elif songinfo[key]["correct?"] is False:
                    print(f"The correct {key} is {song.info[key]}.")

        return this_question_score


def test_make_match_candidate():
    test_strings = [
        "Earth, Wind, & Fire",
        "Love And Tenderness",
        "Here Comes the Sun",
        "Modern-Day Bonnie & Clyde",
        "Wham!",
        "Don't You Want Me, Baby?",
        "Long Way to the Top (If You Wanna Rock N' Roll)"
    ]

    correct_strings = [
        "Earth Wind Fire",
        "Love Tenderness",
        "Here Comes Sun",
        "Modern-Day Bonnie Clyde",
        "Wham",
        "Dont You Want Me Baby",
        "Long Way to Top If You Wanna Rock N Roll"
    ]

    answer_strings = []

    for string in test_strings:
        answer_strings.append(sq_util.make_match_candidate(string))

    for correct, result in zip(correct_strings, answer_strings):
        assert(correct == result)
