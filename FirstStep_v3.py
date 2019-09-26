import Node
import random
import networkx as nx
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections import namedtuple


peer_pressure_multiplier = 1


network = nx.Graph()
nodes = dict()
edges = dict()
def create_graph():
    file = open('karate_edgelist.txt')

    for line in file:
        edge = line.split()
        network.add_edge(edge[0],edge[1],weight=int(random.random()*10) / 10.0)
create_graph()
print(network.nodes(data=True))
for node in network.nodes():
    network.nodes[node]['Xi_plus']=round(random.uniform(0.1, 1.0), 10)
    network.nodes[node]['Xi']=network.nodes[node]['Xi_plus']
    network.nodes[node]['stubbornness']=round(random.uniform(0.1, 1.0), 10)

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
    updated_node = (stubborness_value*network.nodes[node]['Xi_plus']+peer_pressure_multiplier*num_sum)/(stubborness_value+peer_pressure_multiplier*den_sum)
    network.nodes[node]['Xi'] = updated_node
    return updated_node


def comfort_function(node):
    return network.nodes[node]['stubbornness']*(abs(network.nodes[node]['Xi']-network.nodes[node]['Xi_plus'])**2)

def peer_function(edge,peer_pressure_multiplier):
    node=edge[0]
    peer=edge[1]
    return peer_pressure_multiplier*network[node][peer]['weight']*(abs(network.nodes[node]['Xi']-network.nodes[peer]['Xi'])**2)

i=0
comfort_output_values = dict()
peer_output_value = dict()
while i<200:
    comfort_index = namedtuple('comfort_index',['node_x','time'])
    peer_index = namedtuple('peer_index',['node_x','node_y','time'])

    for node in network.nodes():
        comfort_output_values[(node,i)] = comfort_function(node)
        for edge in network.edges(node):
            peer_output_value[(node,edge,i)] = peer_function(edge,peer_pressure_multiplier)
        degroot_model(node,peer_pressure_multiplier)
    i= i+1
    peer_pressure_multiplier = peer_pressure_multiplier + 1

'''df_nodes=(pd.DataFrame(network.nodes(data=True)))
df_nodes.to_csv('nodes.csv', header=False, index=False)

df_edges=(pd.DataFrame(network.edges(data=True)))
df_edges.to_csv('edges.csv', header=False, index=False)'''

data=(pd.Series(comfort_output_values).unstack())
data_pf = (pd.Series(peer_output_value).unstack())
'''data.to_csv('comfort_values.csv')
'''
'''print(data)
print(data_pf)'''

data_transpose = data.transpose()
'''print(data)'''
data_transpose.plot(kind = "line")
plt.show()
