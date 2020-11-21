import random

class Link:
    def __init__(self, parent, ID, node1, node2):
        self.ID=ID
        self.node1 = node1
        self.node2 = node2
        self.parent = parent
    
    """ def generate_view(self):
        #links node IDs to other nodes for fast reference
        self.view={self.node1.ID:self.node2,self.node2.ID:self.node1}
        pass """

    def other_node(self,node):
        return self.view(node.ID)

    def replace(self, old, new):
        if self.parent.debug:
            temp0= repr(self)
            temp1 = [repr(edge) for edge in old.edges.values()]
            temp2 = [repr(edge) for edge in new.edges.values()]
        #replace reference to old node with new node
        if self.node1==old:
            self.node1=new
        else:
            self.node2=new
        #if closed loop: self destruct
        if self.node1 == self.node2:
            self.parent.remove_edge(self,old,new)
            return False
        #self.generate_view()
        return True

    def __repr__(self):
        return f"L{self.ID}: {self.node1.ID}-{self.node2.ID}"

class Node:
    def __init__(self, parent, ID):
        self.ID=ID
        self.parent = parent
        self.edges={}

    def empty(self):
        self.edges={}

    def remove_edge(self,edge):
        self.edges.pop(edge.ID)
        
    def add(self,edge):
        self.edges[edge.ID]=edge

    def absorb(self,v):
        if self.parent.debug:
            temp1 = [repr(edge) for edge in self.edges.values()]
            temp2 = [repr(edge) for edge in v.edges.values()]
        temp=list(v.edges.values())
        for edge in temp:
            if edge.replace(v,self): #returns false when edge became a self loop
                self.add(edge)
        self.parent.remove_node(v)

    def __repr__(self):
        return f"V{self.ID}: {len(self.edges.values())}"

class Graph:
    def __init__(self,debug):
        self.debug=debug
        self.edges={}
        self.nodes={}
        self.n=0
        self.m=0

    def add_node(self,ID):
        self.nodes[ID]=Node(self, ID)
        self.n+=1

    def remove_node(self,node):
        node.empty()
        self.nodes.pop(node.ID)
        self.n-=1

    def add_edge(self,node1_ID,node2_ID):
        self.edges[self.m]=Link(self,self.m,self.nodes[node1_ID],self.nodes[node2_ID])
        self.nodes[node1_ID].edges[self.m]=self.edges[self.m]
        self.nodes[node2_ID].edges[self.m]=self.edges[self.m] #store link reference at other end of link
        self.m+=1        

    def remove_edge(self,edge,node1,node2):
        if self.debug:
            temp1 = [repr(edge) for edge in node1.edges]
            temp2 = [repr(edge) for edge in node2.edges]
        node1.remove_edge(edge)
        node2.remove_edge(edge)
        self.edges.pop(edge.ID)
        self.m-=1

    def pick_edge(self):
        return random.choice(list(self.edges.values()))

    def duplicate(self):
        graph = Graph(self.debug)
        graph.n=self.n
        graph.m=self.m
        graph.edges={x:Link(graph,x,0,0) for x in range(0,self.m)}
        graph.nodes={x:Node(graph,x) for x in range(1,self.n+1)}
        for edge in self.edges.values():
            graph.edges[edge.ID].node1=graph.nodes[edge.node1.ID]
            graph.edges[edge.ID].node2=graph.nodes[edge.node2.ID]
        for ID, node in self.nodes.items():
            for edgeID, edge in node.edges.items():
                graph.nodes[ID].edges[edgeID]=graph.edges[edgeID]
        return graph

def importAdjacencyList(fileName, debug):
    with open (fileName) as inputFile:
        #need to hcnage back for karger.txt
        proto_nodes = {int(a.split(' ')[0]): [int(x) for x in a.split(' ')[1:-1]] for a in inputFile.readlines()}
        #proto_nodes = {int(a.split(' ')[0]): [int(x) for x in a.split(' ')[1:]] for a in inputFile.readlines()}
    
    graph=Graph(debug)
    for nodeID in proto_nodes.keys():
        graph.add_node(nodeID)
    
    for nodeID, proto_edges in proto_nodes.items():
        temp=proto_edges[:]
        for j in temp:
                #if not isinstance(node.proto_edges[j],Link): #if this element is a Link object, skip it
                graph.add_edge(nodeID,j)  #create a Link object from the active node (node) to the node listed at element j (linked_value)
                proto_nodes[j].remove(nodeID)
    if debug:
        for edge in graph.edges.values():
            if not edge in edge.node2.edges.values():
                print("wtf")
            if not edge in edge.node2.edges.values():
                print("wtf")
        for node in graph.nodes.values():
            for edge in node.edges.values():
                if edge.node1==node:
                    edge_target=edge.node2
                else:
                    edge_target=edge.node1
                if not edge in edge_target.edges.values():
                    print('wtf')
    return graph