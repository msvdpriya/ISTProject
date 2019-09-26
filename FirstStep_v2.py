import Node
import random
import networkx as nx
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

network = nx.Graph()
nodes = dict()
edges = dict()
def create_graph():
    file = open('karate_edgelist.txt')

    for line in file:
        edge = line.split()

        comfort = int(random.random()*10) / 10.0
        stubbornness = int(random.random()*10) / 10.0
        network.add_node(edge[0],intial_comfort = comfort,Xi_plus=comfort,Xi=comfort,stubbornness = stubbornness+0.01)
        network.add_node(edge[1],initial_comfort = comfort,Xi_plus=comfort,Xi=comfort,stubbornness = stubbornness+0.01)

        '''assuming directed graph'''
        network.add_edge(edge[0],edge[1],weight=int(random.random()*10) / 10.0,peer_pressure = comfort)


def degroot_model(node):
    num_sum = 0
    den_sum = 0
    stubborness_value = network.nodes[node]['stubbornness']
    for edge in network.edges(node):
        x = edge[0]
        y = edge[1]
        num_sum = num_sum + network[x][y]['weight']*network.nodes[y]['Xi']
        den_sum = den_sum + network[x][y]['weight']
    updated_node = (stubborness_value*network.nodes[node]['Xi_plus']+num_sum)/(stubborness_value+den_sum)
    network.nodes[node]['Xi'] = updated_node
    return updated_node

def comfort_function(node):
    return network.nodes[node]['stubbornness']*(abs(network.nodes[node]['Xi']-network.nodes[node]['Xi_plus'])**2)

def peer_function(node,peer):
    return network[node][peer]['weight']*(abs(network.nodes[node]['Xi']-network.nodes[peer]['Xi'])**2)

'''
Example total_time = 5 min, discrete_level = 1 i.e every 1 min for a total of 5 min
'''
cf = dict()
def optimize_stress(total_time,discrete_level):
    n=total_time/discrete_level
    iter = discrete_level
    while(iter <= total_time):
        for node in network.nodes():
            degroot_model(node)
            cf[(node,iter)]=(comfort_function(node))
            '''for peer in network.edges(node):
                print(peer_function(node,peer[1]))'''

        iter = iter + discrete_level



create_graph()
optimize_stress(1000,1)
'''df= pd.DataFrame(cf,index=network.nodes,columns=[0,1,2,3,4,5])
'''

data=(pd.Series(cf).unstack())
data = data.transpose()
'''print(data)'''
data.plot(kind = "line")
'''nx.draw_networkx(network)
'''
plt.show()
