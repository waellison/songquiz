from sq_classes import sq_game_difficulty, sq_song_database, sq_song

score = 0
max_score = 0

scores = {
    "artist": 5,
    "title": 5
}

db = sq_song_database("tests/database.json")
print("database loaded: " + str(len(db.songs)) + " songs present")

print("\nSelect your difficulty:\n")
diff = sq_game_difficulty()
print(diff.value.title() + " difficulty chosen")
print("Maximum score is " + str(max_score) + " points.  Have fun!\n")

while True:
    this_question_score = 0
    correct = {
        "artist": False,
        "title": False
    }

    try:
        song = db.pick_song()
        for line in song.pick_lines(diff):
            print(line)
    except ValueError:
        break

    for score_val in scores:
        max_score += scores[score_val]

    try:
        artist_guess = input("Guess the artist! > ")
        title_guess = input("Guess the title! > ")
    except EOFError:
        break
    if artist_guess.lower() == song.artist.lower():
        this_question_score += scores["artist"]
        correct["artist"] = True
    if title_guess.lower() == song.title.lower():
        this_question_score += scores["title"]
        correct["title"] = True

    if correct["artist"] == True and correct["title"] == True:
        print("Excellent!  You got that one totally right.")

    if correct["artist"] == False:
        print("Oops!  The correct artist is", song["artist"])

    if correct["title"] == False:
        print("Darn!  The correct title is \"" + song["title"] + "\"")

    print(str(this_question_score) + " added to your score out of " +
          str(max_score) + " possible.\n")

print("Final score:", str(score) + "/" + str(max_score))
