from download_books import Book_Getter
from time import sleep

class Analyze_Book:
    @staticmethod
    def frequency(book_text_words: list[str], output_file: str, current_freq: dict = {}, book_name: str = "") -> dict:
        freq_dict = current_freq

        # Count the occurances of each word
        for word in book_text_words:
            word.strip()
            if not word or len(word) == 1 and word not in "AI":
                continue

            # Add 1 to the frequency count
            if word in freq_dict.keys():
                freq_dict[word] += 1
            else:
                freq_dict[word] = 1


        sorted_freq_keys = sorted(freq_dict, key = lambda k: freq_dict[k], reverse=True)

        # Write frequency to file
        lines = []
        for key in sorted_freq_keys:
            lines.append(f"{key}: {freq_dict[key]}")

        with open(output_file, "w") as file:
            for line in lines:
                try:
                    file.write(f"{line}\n")
                except UnicodeEncodeError:
                    print(line)
                    sleep(2)

        print("Freq done")

        return freq_dict

    @staticmethod
    def relation(book_text_words: list[str], freq_dict: dict, output_file: str, current_rel: dict = {}, book_name: str = "") -> dict:
        rel_dict = current_rel

        # Count the occurances of words that go after other words
        for word_index in range(len(book_text_words) - 1):
            word = book_text_words[word_index]
            next_word = book_text_words[word_index + 1]

            if word not in rel_dict:
                rel_dict[word] = {}

            if not next_word:
                continue
            
            rel_dict[word][next_word] = rel_dict[word].get(next_word, 0) + 1

            print(f"{word_index} : {len(book_text_words)}")

        # Write ^ to file
        lines = []
        for key in freq_dict:
            lines.append(f"{key}: {rel_dict[key]}\n")

        with open(output_file, "w") as file:
            for line in lines:
                try:
                    file.write(f"{line}")
                except UnicodeEncodeError:
                    print(line)
                    sleep(2)

        return rel_dict

if __name__ == "__main__":
    author = "Shakespeare"

    authors_list = Book_Getter.get_list(author)

    print(authors_list[25]["Title"])
    book_text_words = Book_Getter.get_text(authors_list[25])


    freq = Analyze_Book.frequency(book_text_words, r"FrequencyFiles\TestFreq.txt")
    rel = Analyze_Book.relation(book_text_words, freq, r"FrequencyFiles\TestPred.txt")