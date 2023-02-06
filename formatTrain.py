with open("archive/train.txt", "r") as f:
    train_data = f.read()

train_data = train_data.split("\n")
emotions_table = {
        "fear" : -1,
        "anger" : -1,
        "sadness" : -1,
        "joy" : 1,
        "love" : 1,
        "surprise" : 1,
        }

possible_aspect = "i" # Set the main aspect, in this example, it is "I"

f = open("archive/format_train.txt", "w")
for x, line in enumerate(train_data):
    text, emotion = line.split(";")
    if possible_aspect in line.split():
        user_text = []
        # Replace the aspect with "$T$"
        for y in text.split():
            if y == possible_aspect:
                user_text.append("$T$")
            else:
                user_text.append(y)
        
        # Writing to "format_train.txt"
        f.write(" ".join(user_text) + "\n")
        f.write(possible_aspect + "\n")
        f.write(str(emotions_table[emotion]) + "\n")
f.close()
print("Done!")