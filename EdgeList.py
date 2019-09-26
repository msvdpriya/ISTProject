'''the Node class which represents each of our network's vertex'''
class EdgeList:
    def __init__(self, label):
        self.label = label
        self.peers = list()
