import adjacencytools
import cProfile
import math
import time

debug=False

def contract(graph,debug):
    graph_history=[]
    iter=0
    while graph.n > 2:
        edge = graph.pick_edge()
        if debug:
            static_edges=[]
            static_nodes={}
            for edge in graph.edges:
                static_edges.append(repr(edge))
            for ID, node in graph.nodes.items():
                static_nodes[ID]=[repr(x) for x in node.edges]
            edge = graph.pick_edge()
            graph_history.append([static_nodes,static_edges,repr(edge)])
        edge.node1.absorb(edge.node2)
        iter+=1
    return graph.m
    

def seek_min_cut(graph,debug):
    N=graph.n**2*math.log(graph.n,math.e)
    temp_graph = graph.duplicate()
    min_cut= contract(temp_graph,debug)
    for k in range(0,int(N-1)):
        temp_graph = graph.duplicate()
        if (temp_min := contract(temp_graph,debug)) < min_cut:
            min_cut=temp_min
    return min_cut

file_name='formattedKarger.txt'
#file_name='test2.txt'
graph = adjacencytools.importAdjacencyList(file_name,debug)
if debug:
    cProfile.run("min_cut=seek_min_cut(graph,debug)")
else:
    tick = time.perf_counter()
    min_cut=seek_min_cut(graph,debug)
    tock = time.perf_counter()
    print(f"time to execute: {tock-tick} seconds")
print(min_cut)
pass


