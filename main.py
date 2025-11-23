from download_books import BookGetter
from string import punctuation

freq_dict = {}
pred_dict = {}

author = "Shakespeare"

authors_list = BookGetter.get_list(author)

print(authors_list[25]["Title"])
book_text = BookGetter.get_text(authors_list[25])

# Remove punctuation
for char in punctuation:
    book_text = book_text.replace(char, " ")

# Get rid of new lines
book_text = book_text.replace("\n", " ")

# Make everything upper case
book_text = book_text.upper()

# Seperate into list of words
book_text_words = book_text.split(" ")

# Count the occurances of each word
for word in book_text_words:
    # Add 1 to the frequency count
    if word in freq_dict.keys():
        freq_dict[word] += 1
    else:
        freq_dict[word] = 1

# Write frequency to file
lines = []
for key in freq_dict:
    lines.append(f"{key}: {freq_dict[key]}\n")

with open(r"FrequencyFiles\TestFreq.txt", "w") as file:
    file.writelines(lines)

print("Freq done")

# Count the occurances of words that go after other words
for word_index in range(len(book_text_words) - 1):
    word = book_text_words[word_index]
    next_word = book_text_words[word_index + 1]

    if word not in pred_dict:
        pred_dict[word] = {}

    pred_dict[word][next_word] = pred_dict[word].get(next_word, 0) + 1

    print(f"{word_index} : {len(book_text_words)}")

# Write ^ to file
lines = []
for key in freq_dict:
    lines.append(f"{key}: {pred_dict[key]}\n")

with open(r"FrequencyFiles\TestPred.txt", "w") as file:
    file.writelines(lines)


print("done")