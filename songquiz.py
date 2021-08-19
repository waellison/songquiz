import random
from sq_classes import sq_game_difficulty, sq_song_database
from functools import reduce

score = 0
max_score = 0
count = 0
max_count = 0

scores = {
    "artist": 5,
    "title": 5
}

max_question_score = reduce((lambda x, y: x + y), scores.values())

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

db = sq_song_database("database.json")
print("database loaded: " + str(len(db.songs)) + " songs present")

print("\nSelect your difficulty:\n")
diff = sq_game_difficulty()
print(diff.value.title() + " difficulty chosen")
print(
    f"You earn {scores['artist']} points per correct artist and {scores['title']} points per correct title.  Have fun!\n")

try:
    max_count = int(input(f"How many? (max {len(db.songs)}) > "))
except ValueError:
    max_count = len(db.songs)

while True:
    songinfo = {
        "artist": {"guess": str(), "correct?": False},
        "title":  {"guess": str(), "correct?": False}
    }

    if(count == max_count):
        break

    this_question_score = 0

    try:
        song = db.pick_song()
        for line in song.pick_lines(diff):
            print(line)
    except ValueError:
        break

    for score_val in scores:
        max_score += scores[score_val]

    try:
        for key in songinfo.keys():
            songinfo[key]["guess"] = input(f"Guess the {key}! > ")
    except EOFError:
        break

    for key in songinfo.keys():
        if song.loose_match(songinfo[key]["guess"], key) == True:
            songinfo[key]["correct?"] = True
            this_question_score += scores[key]

    if this_question_score == max_question_score:
        print(random.choice(feedbacks["perfect"]))
    else:
        for key in songinfo.keys():
            if songinfo[key]["correct?"] == True:
                print(random.choice(feedbacks[key]))
                print(f"The correct {key} is {song.info[key]}")

    score += this_question_score
    count += 1
    print(f"{this_question_score} points added to your score.  {max_count - count} songs remain.")
    print(f"Current score: {str(score)}/{str(max_score)}\n")

print("Final score:", str(score) + "/" + str(max_score))
