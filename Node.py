'''the Node class which represents each of our network's vertex'''
class Node:
    def __init__(self, label):
        self.label = label
        self.peer_pressure =[]
        self.comfort = 0
        self.stubbornness = 0
        self.peers = []
