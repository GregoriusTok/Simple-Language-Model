import tkinter as tk
from tkinter import ttk
from download_books import Book_Getter
from get_numbers import Analyze_Book
import os
from make_graph import Graph_Generator

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
    
    def search_button_pressed(self):
        print(f"Search for the {self.search_type_key.get()}, {self.search_key.get()}")

        if os.path.isfile(rf"FrequencyFiles\Freq-{self.search_type_key.get()}-{self.search_key.get()}.txt") and os.path.isfile(rf"FrequencyFiles\Rel-{self.search_type_key.get()}-{self.search_key.get()}.txt"):
            self.child_window.append(File_Exists(self))
        else:
            self.book_list = Book_Getter.get_list(self.search_key.get(), self.search_type_key.get())

            self.child_window.append(List_Vet_Window(self, self.book_list))

    def book_list_confirmed(self, child, book_list):
        self.book_list = book_list
        child.destroy()

        for book in self.book_list:
            book_text_words = Book_Getter.get_text(book) 

            self.freq_dict = Analyze_Book.frequency(book_text_words, rf"FrequencyFiles\Freq-{self.search_type_key.get()}-{self.search_key.get()}.txt", self.freq_dict)
            self.rel_dict = Analyze_Book.relation(book_text_words, self.freq_dict, rf"FrequencyFiles\Rel-{self.search_type_key.get()}-{self.search_key.get()}.txt", self.rel_dict)

            print(f"{self.book_list.index(book)} / {len(self.book_list)} done")

        print("done")

        self.add_chat_and_graph()
    
    def add_chat_and_graph(self):
        self.graph_button = ttk.Button(self.layout, text="SEE GRAPH OF WORDS", command=self.graph_button_pressed)
        self.graph_button.grid_configure(column=0, row=2, columnspan=3, sticky="news")

        self.chat_button = ttk.Button(self.layout, text="CHATBOT", command=self.chat_button_pressed)
        self.chat_button.grid_configure(column=0, row=3, columnspan=3, sticky="news")

    def graph_button_pressed(self):
        self.child_window.append(Graph_Window(self))

    def chat_button_pressed(self):
        self.child_window.append(Chat_Window(self))
        
class List_Vet_Window(tk.Toplevel):
    def __init__(self, parent, book_list):
        super().__init__()

        self.parent = parent
        self.book_list = book_list

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

class File_Exists(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.freq_file = rf"FrequencyFiles\Freq-{self.parent.search_type_key.get()}-{self.parent.search_key.get()}.txt"
        self.rel_file = rf"FrequencyFiles\Rel-{self.parent.search_type_key.get()}-{self.parent.search_key.get()}.txt"

        self.title("DATA ALREADY COLLECTED")
        self.geometry("300x50+200+100")
        self.resizable=False

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
    
        self.layout = ttk.Frame(self, relief="sunken", borderwidth=1)
        self.layout.grid_configure(column=0, row=0, sticky="news")

        self.layout.columnconfigure(0, weight=1)
        self.layout.rowconfigure(0, weight=1)

        self.old_button = ttk.Button(self.layout, text="USE EXISTING DATA", command=self.old_button_pressed)
        self.old_button.grid_configure(column=0, row=0, sticky="news")

        self.new_button = ttk.Button(self.layout, text="GET NEW DATA", command=self.new_button_pressed)
        self.new_button.grid_configure(column=0, row=1, sticky="news")


    def new_button_pressed(self):
        self.parent.child_window.append(List_Vet_Window(self.parent, Book_Getter.get_list(self.parent.search_key.get(), self.parent.search_type_key.get())))
        self.destroy()

    def old_button_pressed(self):
        self.parent.freq_dict = Analyze_Book.file_to_dict(self.freq_file)
        self.parent.rel_dict = Analyze_Book.file_to_dict(self.rel_file)
        
        self.parent.add_chat_and_graph()

        self.destroy()

class Graph_Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.title("What is the word limit?")
        self.geometry("300x50+100+50")
        self.resizable=False

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
    
        self.layout = ttk.Frame(self, relief="sunken", borderwidth=1)
        self.layout.grid_configure(column=0, row=0, sticky="news")

        self.layout.columnconfigure(0, weight=3)
        self.layout.columnconfigure(0, weight=1)
        self.layout.rowconfigure(0, weight=1)
        self.layout.rowconfigure(1, weight=1)

        self.word_limit = tk.IntVar(value=1000)

        self.slider = tk.Scale(self.layout, from_=0, to=len(list(parent.freq_dict.keys())), variable=self.word_limit, resolution=1, orient="horizontal")
        self.slider.grid_configure(column=0, row=0, sticky="nsew")

        self.gen_graph_button = ttk.Button(self.layout, text="Generate Graph", command=self.gen_graph)
        self.gen_graph_button.grid_configure(column=0, row=1, sticky="news")

    def gen_graph(self):
        Graph_Generator.gen_graph(self.parent.rel_dict, self.parent.freq_dict, self.word_limit.get())


class Chat_Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()

if __name__ == "__main__":
   root = Search_Window()

   root.mainloop()