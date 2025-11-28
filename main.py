import tkinter as tk
from tkinter import ttk
from download_books import Book_Getter
from get_numbers import Analyze_Book

class Search_Window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Simple Language Model")

        self.child_window = []

        self.freq_dict = {}
        self.rel_dict = {}

        self.geometry("+50+50")
        self.resizable = False

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.layout = ttk.Frame(self, relief="sunken", borderwidth=1)
        self.layout.grid_configure(column=0, row=0, sticky="news")

        self.layout.columnconfigure(0, weight=1)
        self.layout.columnconfigure(1, weight=1)
        self.layout.columnconfigure(2, weight=1)
        self.layout.rowconfigure(0, weight=1)
        self.layout.rowconfigure(1, weight=1)
        self.layout.rowconfigure(2, weight=1)

        self.heading = ttk.Label(self.layout, text="Get Books", anchor="center")
        self.heading.grid_configure(column=0, row=0, sticky="ew", columnspan=3)

        self.search_type_key = tk.StringVar()
        self.search_type_droopbox = ttk.Combobox(self.layout, textvariable=self.search_type_key, values=("Authors", "Subjects", "Title"))
        self.search_type_droopbox.grid_configure(column=0, row=1, sticky="ew")

        self.search_key = tk.StringVar()
        self.search_bar = ttk.Entry(self.layout, textvariable=self.search_key)
        self.search_bar.grid_configure(column=1, row=1, sticky="ew")

        self.search_button = ttk.Button(self.layout, text="SEARCH", command=self.search_button_pressed)
        self.search_button.grid_configure(column=2, row=1, sticky="ew")

        self.status_text = tk.StringVar()
        self.status_text.set("ENTER SEARCH")
        self.status_label = ttk.Label(self.layout, textvariable=self.status_text, anchor="center")
        self.status_label.grid_configure(column=0, row=2, columnspan=3, sticky="ew")
    
    def search_button_pressed(self):
        print(f"Search for the {self.search_type_key.get()}, {self.search_key.get()}")

        self.status_text.set("SEARCHING...")

        self.book_list = Book_Getter.get_list(self.search_key.get(), self.search_type_key.get())

        self.status_text.set("SEARCH COMPLETE, CONFIRMING TEXTS")

        self.child_window.append(List_Vet_Window(self, self.book_list))

    def book_list_confirmed(self, child, book_list):
        self.book_list = book_list
        child.destroy()

        self.status_text.set("CONFIRMED, GETTING TEXTS")

        for book in self.book_list:
            book_text_words = Book_Getter.get_text(book) 

            self.freq_dict = Analyze_Book.frequency(book_text_words, rf"FrequencyFiles\Freq-{self.search_type_key.get()}-{self.search_key.get()}.txt", self.freq_dict)
            self.rel_dict = Analyze_Book.relation(book_text_words, self.freq_dict, rf"FrequencyFiles\Rel-{self.search_type_key.get()}-{self.search_key.get()}.txt", self.rel_dict)

        print("done")
        self.status_text.set("ANALYZED TEXTS")
        
class List_Vet_Window(tk.Toplevel):
    def __init__(self, parent, book_list):
        super().__init__()

        self.book_list = book_list
        self.parent = parent

        self.title("Are these the right books?")
        self.geometry("+100+50")
        self.resizable=False

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
    
        self.layout = ttk.Frame(self, relief="sunken", borderwidth=1)
        self.layout.grid_configure(column=0, row=0, sticky="news")

        self.layout.columnconfigure(0, weight=1)
        self.layout.rowconfigure(0, weight=1)

        self.textbox = tk.Text(self.layout)
        self.textbox.grid_configure(column=0, row=0, sticky="news")
        
        starting_text = ""
        for book in self.book_list:
            starting_text += f"{book["Title"]} || by {book["Authors"]}\n"

        self.textbox.insert("1.0", starting_text)

        self.scrollbar = ttk.Scrollbar(self.layout, orient="vertical", command=self.textbox.yview)
        self.scrollbar.grid_configure(column=1, row=0,sticky="news")      

        self.confirm_button = ttk.Button(self.layout, text="Confirm Texts", command=self.confirm_pressed)
        self.confirm_button.grid_configure(column=0, row=1, columnspan=2, sticky="nesw")

    def confirm_pressed(self):
        text = self.textbox.get("1.0", "end")

        text_lines = text.split("\n")

        titles = []
        for line in text_lines:
            titles.append(line.split("||")[0])

        for book in self.book_list:
            if book["Title"] not in titles:
                self.book_list.remove(book)

        self.parent.book_list_confirmed(self, self.book_list)

if __name__ == "__main__":
   root = Search_Window()

   root.mainloop()