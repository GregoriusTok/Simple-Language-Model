from download_books import BookGetter
from string import punctuation

freq_dict = {}
pred_dict = {}

author = "Shakespeare"

authors_list = BookGetter.get_list(author)

book_text = BookGetter.get_text(authors_list[0])

book_text_words = book_text.split(" ")

for word in book_text_words:
    word = word.replace("\n", "")

    letter_list = list(word)
    char_index = 0
    while char_index < len(letter_list):
        if letter_list[char_index] in punctuation:
            if letter_list[char_index] in freq_dict.keys():
                freq_dict[letter_list[char_index]] += 1
            else:
                freq_dict[letter_list[char_index]] = 1

            letter_list.pop(char_index)
        else: 
            char_index += 1

    if len(letter_list) == 0:
        continue        
    else: 
        word = "".join(letter_list).upper()

    if word in freq_dict.keys():
        freq_dict[word] += 1
    else:
        freq_dict[word] = 1


lines = []
for key in freq_dict:
    lines.append(f"{key}: {freq_dict[key]}\n")

with open(r"FrequencyFiles\TestFreq.txt", "w") as file:
    file.writelines(lines)


print("done")