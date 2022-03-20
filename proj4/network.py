# -*- coding:utf-8 -*-

import pickle
import networkx as nx
import matplotlib.pyplot as plt
import community


def main():
    with open('Data/graph.pkl','rb') as f:
        graph=pickle.load(f)

    sta_graph(graph)
    plot_graph(graph)


def sta_graph(graph):
    # generate nodes and edges
    nodes = list(graph.keys())
    edges = []
    for i in graph:
        for j in graph[i]:
            edges.append((i, j))

    G = nx.DiGraph()
    for edge in edges:
        G.add_edge(edge[0], edge[1])

    # cluster coeffient
    cluster = nx.clustering(G)
    cluster = [(i, j) for i, j in cluster.items()]
    # average cluster coeffienct
    print('The graph average cluster coeffient is:', nx.average_clustering(G))
    print('-' * 50)

    # betweeness
    betweeness = nx.betweenness_centrality(G)
    betweeness = [(i, j) for i, j in betweeness.items()]
    values = [i[1] for i in betweeness]
    print('The graph average betweeness is:', sum(values) / len(values))
    betweeness = sorted(betweeness, reverse=True, key=lambda x: x[1])
    print('the top ten musicians with highest betweeness are:')
    for i in betweeness[:10]:
        print(i)
    print('-' * 50)

    # degree
    degrees = G.degree()
    degrees = sorted(degrees, reverse=True, key=lambda x: x[1])
    print('the top ten musicians with highest degrees are:')
    for i in degrees[:10]:
        print(i)
    temp = [i[1] for i in degrees]
    print('The graph average degree is:', sum(temp) / len(temp))
    print('-' * 50)

    # correlations
    sums = {i: [j] for i, j in cluster}
    for i in betweeness:
        sums[i[0]].append(i[1])
    for i in degrees:
        sums[i[0]].append(i[1])
    values = sums.values()
    values1, values2, values3 = [i[0] for i in values], [i[1] for i in values], [i[2] for i in values]
    plt.scatter(values3, values1)
    plt.scatter(values3, values2)
    plt.legend(labels=['Cluster coefficient', 'Betweeness'])
    plt.xlabel('Degree')
    plt.ylabel('Betweeness & Cluster coefficient')
    plt.show()

    # density
    print('The graph density is: ', nx.density(G))
    undirected = G.to_undirected()

    # triangles
    triangles = nx.triangles(undirected)
    triangles = [(i, j) for i, j in triangles.items()]
    triangles = sorted(triangles, reverse=True, key=lambda x: x[1])
    print('the top ten musicians with highest triangles are:')
    for i in triangles[:10]:
        print(i)
    print('-' * 50)

    # modularity
    unweighted_SG = nx.Graph()
    for u, v in undirected.edges():
        unweighted_SG.add_edge(u, v)
    partition = community.best_partition(unweighted_SG)
    values = [partition.get(node) for node in unweighted_SG.nodes()]
    modValue = community.modularity(partition, unweighted_SG)
    print("modularity: {}".format(modValue))


def plot_graph(graph):
    nodes = list(graph.keys())
    edges = []
    for i in graph:
        for j in graph[i]:
            edges.append((i, j))
    G = nx.DiGraph()
    for edge in edges:
        G.add_edge(edge[0], edge[1])

    degrees = G.degree()

    names=['The Beatles','Bob Dylan','The Rolling Stones']
    for j in names:
        G_new = nx.Graph()
        plt.figure(figsize=(20, 20))
        temp = graph[j]
        for i in temp:
            G_new.add_node(j,nodesize=degrees[j])
            G_new.add_node(i, nodesize=degrees[i])
            G_new.add_weighted_edges_from([(j, i, 1)])
        sizes = [G_new.nodes[node]['nodesize'] * 50 for node in G_new]
        pos = nx.spring_layout(G_new)

        nx.draw(G_new, pos=pos, with_labels=False, node_size=sizes, width=1, edge_color="#FFDEA2", font_weight='regular')
        for node, (x, y) in pos.items():
            plt.text(x, y, node, fontsize=degrees[node] / 15, ha='center', va='center')
        plt.show()


if __name__ == '__main__':
    main()