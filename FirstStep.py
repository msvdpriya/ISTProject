import Node
import random
import networkx as nx
import matplotlib.pyplot as plt

network = nx.Graph()
nodes = dict()
edges = dict()
def create_graph():
    file = open('D:\My Project\IST_IA\karate_edgelist.txt')

    for line in file:
        edge = line.split()

        comfort = int(random.random()*10) / 10.0
        stubbornness = int(random.random()*10) / 10.0
        network.add_node(edge[0],base_comfort = comfort,current_comfort=comfort,stubbornness = stubbornness)
        '''assuming undirected graph'''
        network.add_node(edge[1],base_comfort = comfort,current_comfort=comfort,stubbornness = stubbornness)
        network.add_edge(edge[0],edge[1],weight=int(random.random()*10) / 10.0,peer_pressure = comfort)


def populate_data():
    for node, node_data in network.nodes(data=True):
        nodes[node] = node_data
    for i,j,data in network.edges(data=True):
        edges[(i,j)] = data


create_graph()
populate_data()
'''
edge_tuple[1]]['current_comfort'] to be changed as its undirected graph
refer get_peers
'''
def degroot_model(node):
    num_sum = sum(edge_data['weight']*nodes[edge_tuple[1 if node == edge_tuple[0] else 0]]['current_comfort']for edge_tuple,edge_data in edges.items() if node in edge_tuple)
    den_sum = sum(edge_data['weight'] for edge_tuple,edge_data in edges.items() if node in edge_tuple)
    updated_node = (nodes[node]['stubbornness']*nodes[node]['base_comfort']+num_sum)/(nodes[node]['stubbornness']+den_sum)
    nodes[node]['current_comfort'] = updated_node
    return updated_node

def comfort_function(node):
    return nodes[node]['stubbornness']*(abs(nodes[node]['current_comfort']-nodes[node]['base_comfort'])**2)

def peer_function(node,peer):
    return edges[(node,peer)]['weight']*(abs(nodes[node]['current_comfort']-nodes[peer]['current_comfort'])**2)

def get_peers(node):
    peer_indexes = []
    for edge_tuple,edge_data in edges.items() :
        if node in edge_tuple:
            peer_indexes.append(edge_tuple[1] if node == edge_tuple[0] else edge_tuple[0])
    return peer_indexes
'''
first cycle
'''

for node in nodes:
    peer_indexes = get_peers(node)
    degroot_model(node)
    print('for node ', node)
    print('comfort function is',comfort_function)
    print('peer pressures are')
    for peer in peer_indexes:
        '''     print('peer is', peer)
        print(edges[(node,peer)])
        print(edges[(node,peer)]['weight']*(abs(nodes[node]['current_comfort']-nodes[peer]['current_comfort'])**2))'''
        print(peer_function(node,peer)) '''fix it'''
