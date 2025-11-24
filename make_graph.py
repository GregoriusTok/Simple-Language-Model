import networkx as nx
import matplotlib.pyplot as mpl
from ast import literal_eval

def file_to_dict(input_file: str, ouput_dict: dict = {}, debug = True) -> dict:

    with open(input_file, "r") as file:
        file_lines = file.readlines()
        for line in file_lines:
            line.strip()

            if not line:
                continue

            key, value = line.split(":", 1)
            key = key.strip()

            if not key:
                continue

            value = literal_eval(value)

            ouput_dict[key] = value

            if debug: 
                print(f"{file_lines.index(line)} : {len(file_lines)}")

        return ouput_dict
     

def gen_graph(pred_dict, freq_dict):
    graph = nx.Graph()

    for key in pred_dict:
        if key not in freq_dict or freq_dict[key] < word_cutoff:
            continue

        for connection in pred_dict[key]:
            if connection not in freq_dict or freq_dict[connection] < word_cutoff:
                continue

            graph.add_edge(key, connection)

        print(f"key {list(pred_dict.keys()).index(key)} : {len(list(pred_dict.keys()))}")

    return graph

if __name__ == "__main__":    
    pred_dict = {}
    freq_dict = {}

    word_cutoff = 100


    file_to_dict(r"FrequencyFiles\TestFreq.txt", freq_dict)
    file_to_dict(r"FrequencyFiles\TestPred.txt", pred_dict)
    
    