import numpy as np
import pandas as pd
from apyori import apriori
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import community


def dict_to_graph(data, weight=False):
    graph = nx.DiGraph()
    for item in data:
        if weight == True:
            graph.add_edge(item[0], item[1], weight=item[2])
        else:
            graph.add_edge(item[0], item[1])
    return graph


def show_scatter(x, y, title=None):
    # plt.style.use("_mpl-gallery")
    fig, ax = plt.subplots()
    if title is not None:
        ax.set_title(title)
    ax.scatter(x, y, 2)
    plt.show()


def data_minning(G):
    seed = 20160
    pos = nx.spring_layout(G, seed=seed)  # Seed for reproducible layout
    nx.draw_networkx(G, pos=pos)
    plt.show()

    # 用图挖掘
    # 计算度
    degree = dict(G.degree)
    plt.bar(degree.keys(), degree.values())
    plt.title("degree")
    plt.show()
    # print(f"节点度：{degree}")

    # 进行中心性挖掘：Betweenness Centrality
    betweenness_centrality = nx.betweenness_centrality(G)
    # print("Betweenness Centrality:", betweenness_centrality)
    plt.bar(
        betweenness_centrality.keys(),
        betweenness_centrality.values(),
    )
    plt.title("betweenness_centrality")
    plt.show()
    # show_scatter(
    #     betweenness_centrality.keys(),
    #     betweenness_centrality.values(),
    #     "betweenness_centrality",
    # )
    # print()

    # 进行接入中心性挖掘：Closeness Centrality
    closeness_centrality = nx.closeness_centrality(G)
    # print("Closeness Centrality:", closeness_centrality)
    plt.bar(
        closeness_centrality.keys(),
        closeness_centrality.values(),
    )
    plt.title("closeness_centrality")
    plt.show()
    # show_scatter(
    #     closeness_centrality.keys(),
    #     closeness_centrality.values(),
    #     "closeness_centrality",
    # )
    # print()

    # 进行度中心性挖掘：Degree Centrality
    degree_centrality = nx.degree_centrality(G)
    # print("Degree Centrality:", degree_centrality)
    plt.bar(degree_centrality.keys(), degree_centrality.values())
    plt.title("Degree Centrality")
    plt.show()
    # show_scatter(
    #     degree_centrality.keys(),
    #     degree_centrality.values(),
    #     "degree_centrality",
    # )
    print()

    # 进行优先中心性挖掘：Eigenvector Centrality
    eigenvector_centrality = nx.eigenvector_centrality(G)
    # print("Eigenvector Centrality:", eigenvector_centrality)
    plt.bar(
        eigenvector_centrality.keys(),
        eigenvector_centrality.values(),
    )
    plt.title("eigenvector_centrality")
    plt.show()
    # show_scatter(
    #     eigenvector_centrality.keys(),
    #     eigenvector_centrality.values(),
    #     "eigenvector_centrality",
    # )
    print()

    # 社区结构
    G0 = nx.Graph(G)
    partition = community.best_partition(G0)
    print(f"社区结构：{partition}")

    pos = nx.spring_layout(G0)

    # 根据其分区对节点进行着色
    cmap = cm.get_cmap("viridis", max(partition.values()) + 1)
    nx.draw_networkx_nodes(
        G0,
        pos,
        partition.keys(),
        node_size=40,
        cmap=cmap,
        node_color=list(partition.values()),
    )
    nx.draw_networkx_edges(G0, pos, alpha=0.5)
    plt.show()


if __name__ == "__main__":
    # # 读取数据
    congress_network_data = pd.read_json(
        "./data/congress_network/congress_network_data.json"
    )
    congress_edges = pd.read_csv("./data/congress_network/congress copy.edgelist.csv")
    # 用aprior进行挖掘
    frequent_itemsets1 = list(
        apriori(congress_network_data["inList"][0], min_support=0.5, use_colnames=True)
    )
    d = np.array(congress_edges)
    frequent_itemsets2 = list(apriori(d, min_support=0.5, use_colnames=True))
    # 打印出频繁项集
    for itemset in frequent_itemsets2:
        print(itemset)

    G = dict_to_graph(d, weight=True)
    data_minning(G)

    # 读取数据
    lasftm_asia_edges = pd.read_csv("./data/lastfm_asia/lastfm_asia_edges.csv")
    # lasftm_asia_features = pd.read_json("./data/lastfm_asia/lastfm_asia_features.json")
    lasftm_asia_target = pd.read_csv("./data/lastfm_asia/lastfm_asia_target.csv")

    G = dict_to_graph(np.array(lasftm_asia_edges), weight=False)
    data_minning(G)

    pass
