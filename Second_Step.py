import Node
import random
import networkx as nx
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections import namedtuple


peer_pressure_multiplier = 1
learning_rate_values = [0.3,0.6]

network = nx.Graph()
nodes = dict()
edges = dict()
def create_graph():
    file = open('karate_edgelist.txt')

    for line in file:
        edge = line.split()
        network.add_edge(edge[0],edge[1],weight=int(random.random()*10) / 10.0)
create_graph()

for node in network.nodes():
    network.nodes[node]['Xi_plus']=round(random.uniform(0.1,1.0), 10)
    network.nodes[node]['Xi']=network.nodes[node]['Xi_plus']

    network.nodes[node]['stubbornness']=round(random.uniform(0.1, 1.0), 10)+0.5 if round(random.uniform(0.1, 1.0), 10)+0.5<1 else 0.9
for x,y in network.edges():
    network.edges[x, y]['weight'] = round(random.uniform(0.1, 1.0), 10)


def degroot_model(node,peer_pressure_multiplier):
    num_sum = 0
    den_sum = 0
    stubborness_value = network.nodes[node]['stubbornness']
    for edge in network.edges(node):
        x = edge[0]
        y = edge[1]
        num_sum = num_sum + network[x][y]['weight']*network.nodes[y]['Xi']
        den_sum = den_sum + network[x][y]['weight']
    updated_node_num = (stubborness_value*network.nodes[node]['Xi_plus']+peer_pressure_multiplier*num_sum)
    updated_node_den=(stubborness_value+peer_pressure_multiplier*den_sum)
    network.nodes[node]['Xi'] = updated_node_num/updated_node_den
    return network.nodes[node]['Xi']

def behavioural_model(node,peer_pressure_multiplier,learning_rate):
    print(learning_rate)
    num_sum = 0
    den_sum = 0
    stubborness_value = network.nodes[node]['stubbornness']
    for edge in network.edges(node):
        x = edge[0]
        y = edge[1]
        num_sum = num_sum + network[x][y]['weight']*(network.nodes[y]['Xi']-network.nodes[x]['Xi'])
        den_sum = den_sum + network[x][y]['weight']
    updated_node_num = (stubborness_value*(network.nodes[node]['Xi_plus']-network.nodes[node]['Xi'])+peer_pressure_multiplier*num_sum)
    updated_node_den=(stubborness_value+peer_pressure_multiplier*den_sum)
    network.nodes[node]['Xi'] = network.nodes[node]['Xi']+updated_node_num/updated_node_den
    return network.nodes[node]['Xi']

def comfort_function(node):
    return network.nodes[node]['stubbornness']*(abs(network.nodes[node]['Xi']-network.nodes[node]['Xi_plus'])**2)

def peer_function(edge,peer_pressure_multiplier):
    node=edge[0]
    peer=edge[1]
    return peer_pressure_multiplier*network[node][peer]['weight']*(abs(network.nodes[node]['Xi']-network.nodes[peer]['Xi'])**2)
diff_learning_rate_Xi_values = dict()
diff_learning_rate_comfort_values = dict()
diff_learning_rate_peer_values = dict()

for lr in learning_rate_values:
    i=0
    comfort_output_values = dict()
    peer_output_value = dict()
    xi_output_values = dict()
    while i<1000:
        for node in network.nodes():
            comfort_output_values[(node,i)] = comfort_function(node)
            for edge in network.edges(node):
                peer_output_value[(node,edge,i)] = peer_function(edge,peer_pressure_multiplier)
                '''called behaviour model instead of de groot model'''
            xi_output_values[(node,i)] = behavioural_model(node,peer_pressure_multiplier,lr)
        i= i+1
        peer_pressure_multiplier = peer_pressure_multiplier + 1
    diff_learning_rate_Xi_values[lr] = xi_output_values
    diff_learning_rate_comfort_values[lr]= comfort_output_values
    diff_learning_rate_peer_values[lr] = peer_output_value


pd.Series(diff_learning_rate_Xi_values[0.6]).unstack().transpose().plot(kind = "line")

'''nx.draw(network)
'''
plt.show()
