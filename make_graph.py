import networkx as nx
import matplotlib.pyplot as mpl
     
class Graph_Generator:
    @staticmethod
    def gen_graph(pred_dict, freq_dict, word_cutoff = 1000):
        G = nx.Graph()

        for word in freq_dict:
            if word in pred_dict and freq_dict[word] > word_cutoff:
                for related in pred_dict[word]:
                    if related in freq_dict and freq_dict[related] > word_cutoff:
                        G.add_edge(word, related, weight=pred_dict[word][related])

        pos = nx.spring_layout(G, weight="weight", k=2, seed=3, iterations=1000)
        weights = [G[u][v]["weight"] for u, v in G.edges()]

        nx.draw_networkx_nodes(G, pos, node_size=5)
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edges(G, pos, edge_color="#a1a1a1")

        mpl.axis("off")
        mpl.show()

    