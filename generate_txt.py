from random import random

class Text_Generator:
    @staticmethod
    def from_one_word(rel_dict: dict[str, dict[str, int]], word: str, num_words: int) -> str:
        output = word

        prev_word = word

        for word_count in range(num_words):
            if prev_word not in rel_dict: break

            next_word_dict = rel_dict[prev_word]
            
            total = 0
            for i in next_word_dict:
                total += next_word_dict[i]

            rand_num = random() * total

            rel_num = 0
            for i in next_word_dict:
                if rand_num <= next_word_dict[i] + rel_num:
                    output += f" {i}"
                    prev_word = i
                    break
                else:
                    rel_num += next_word_dict[i]


        return output

if __name__ == "__main__":
    print(Text_Generator.from_one_word({"HELLO": {"THERE": 3, "ME": 1, "WORLD": 39}, 
                                        "WORLD": {"DEAD": 2, "FELLOW": 12, "STINT": 2},
                                        "THERE": {"WORLD": 12, "DEAD": 3, "FELLOW": 9}, 
                                        "ME": {}}, "HELLO", 10))