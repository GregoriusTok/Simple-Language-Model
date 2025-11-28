import csv
from io import StringIO
import requests
import gzip
from string import punctuation
import re

class Book_Getter:

    @staticmethod
    def get_list(key: str="Shakespeare", selection: str="Authors") -> list:
        GUTENBERG_CSV_URL = "https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv.gz"

        r = requests.get(GUTENBERG_CSV_URL)
        r = gzip.decompress(r.content)

        csv_text = r.decode()
        csv_dict = csv.DictReader(StringIO(csv_text))

        book_list = [book for book in csv_dict 
                     if key in book[selection] and
                     "Indexes" not in book["Subjects"] and
                     book["Type"] == "Text" and
                     book["Language"] == "en"]

        return book_list
    
    @staticmethod
    def get_text(book) -> list:
        book_id = book["Text#"]
        base_url = f"https://www.gutenberg.org/files/{book_id}"

        candidate_url = [
            f"{base_url}/{book_id}.txt",
            f"{base_url}/{book_id}-0.txt",
            f"{base_url}/{book_id}-8.txt",
            f"{base_url}/{book_id}-0.txt.utf-8",
            f"{base_url}/{book_id}.txt.utf-8",
        ]

        for url in candidate_url:
            r = requests.get(url)
            if r.status_code == 200:

                break
            else:
                print(404)
                
        all_text = r.text
        book_text = re.split(r"\*\*\*.*?\*\*\*", all_text)[1].strip()

        # with open("test_text.txt", "w") as file:
        #     file.write(book_text)

        # Remove punctuation
        for char in punctuation:
            if char in "'-":
                pass
            else:
                book_text = book_text.replace(char, " ")

        # Get rid of new lines
        book_text = book_text.replace("\n", " ")
        book_text = book_text.replace("\r", " ")

        # Make everything upper case
        book_text = book_text.upper()

        # Seperate into list of words
        book_text_words = book_text.split(" ")

        return book_text_words


if __name__ == "__main__":
    book_list = Book_Getter.get_list()

    book = book_list[25]

    text = Book_Getter.get_text(book)

    print("done")
    