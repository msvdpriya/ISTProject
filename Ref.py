    # Use a list comprehension to get the nodes of interest: noi
noi = [n for n, d in T.nodes(data=True) if d['occupation'] == 'scientist']

# Use a list comprehension to get the edges of interest: eoi
eoi = [(u, v) for u, v, d in T.edges(data=True) if d['date'] < date(2010, 1, 1)]
print(noi)
print(eoi)



//
# Set the weight of the edge
T.edges[1,10]['weight'] = 2

# Iterate over all the edges (with metadata)
for u, v, d in T.edges(data=True):

    # Check if node 293 is involved
    if 293 in [u,v]:

        # Set the weight to 1.1
        T.edges[u,v]['weight'] = 1.1



//
for node, node_data in network.nodes(data=True):
    nodes[node] = node_data
    eoi = [(i, j,edge_data) for i, j, edge_data in network.edges(data=True) if node in [i,j]]
    print(node,eoi)

//

createnodes
nx.draw(network,with_labels=True)
plt.show()

//
def degroot_model(node,eoi):
    num_sum = sum(edge[2]['weight']*nodes[edge[1]]['comfort']for edge in eoi)
    den_sum = sum(edge[2]['weight'] for edge in eoi)
    return (nodes[node]['stubbornness']*nodes[node]['comfort']+num_sum)/(nodes[node]['stubbornness']+den_sum)

for node in nodes:
    eoi = [(i, j,edge_data) for i, j, edge_data in network.edges(data=True) if node in [i,j]]
    print(degroot_model(node,eoi))


//

for node in network.nodes():
    nodes[node] = dict()
    nodes[node][node] = network.nodes[node]['Xi']
    for peer in network.edges(node):
        nodes[node][peer[1]]=peer_function(node,peer[1])
nodes_df =[value for key,value in nodes.items()]


print(nodes)
print(nodes_df)
df =  pd.DataFrame(nodes_df,index = network.nodes,columns = network.nodes)
df['Base_Comfort'] = [value['intial_comfort'] for key,value in network.nodes(data=True)]
df['Current_Comfort'] = [comfort_function(key) for key,value in network.nodes(data=True)]
print(df)

//
'''
    comfort_index = namedtuple('comfort_index',['node_x','time'])
    peer_index = namedtuple('peer_index',['node_x','node_y','time'])'''

            '''for edge in network.edges(node):
                peer_output_value[peer_index(node_x=edge[0],node_y=edge[1],time=i)] = peer_function(edge)'''



//

'''df_nodes=(pd.DataFrame(network.nodes(data=True)))
df_nodes.to_csv('nodes.csv', header=False, index=False)

df_edges=(pd.DataFrame(network.edges(data=True)))
df_edges.to_csv('edges.csv', header=False, index=False)'''

data=(pd.Series(xi_output_values).unstack())
data_pf = (pd.Series(peer_output_value).unstack())
'''data.to_csv('comfort_values.csv')
'''
'''print(data)
print(data_pf)'''
'''print(network.edges())
'''
data_transpose = data.transpose()
'''print(data)'''
data_transpose.plot(kind = "line")
'''nx.draw(network)
'''
plt.show()
