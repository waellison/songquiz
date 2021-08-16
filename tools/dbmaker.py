db = list()
output = ""

print("Type Ctrl+D to end input")
while True:
    print("DB size: " + str(len(db)))
    try:
        title = input("Title> ")
        artist = input("Artist> ")
    except EOFError:
        break
    db.append((title, artist))

output += "{ \"songs\": [\n"
for entry in db:
    title = entry[0]
    artist = entry[1]
    output += "{ \"title\": \"" + title + \
        "\", \"artist\": \"" + artist + "\" },\n"
output += "]}\n"

print(output)
