import pickle
from graphtools.graph import Graph, Edge, Vertex
import os
import unittest
import json


def Convert(trail_g):
    rtn = dict()
    rtn['nvertices'] = len(trail_g.vertices)
    rtn['nedges'] = len(trail_g.edges)
    rtn['directed'] = False
    rtn['degree'] = []
    rtn['edges'] = []

    for i, v in enumerate(trail_g.vertices):
        # Find the outdegree (number of edges for this vertex)
        outdegree = sum([1 for e in trail_g.edges
                         if e.point1.name == v.name or e.point2.name == v.name])
        rtn['degree'].append(outdegree)

        edges = []
        for e in trail_g.edges:
            if e.point1.name == v.name:
                edge = {
                    'y': trail_g.vertices.index(e.point2),
                    'weight': e.distance
                }
                edges.append(edge)
            elif e.point2.name == v.name:
                edge = {
                    'y': trail_g.vertices.index(e.point1),
                    'weight': e.distance
                }
                edges.append(edge)

        rtn['edges'].append(edges)

    # print (json.dumps(rtn, indent=2))
    return rtn


def Dijkstra(G, s, t):
    print ('Dijkstra from:\n\t{}\n\t\tto\n\t{}'.format(s, t))
    print

    intree = [False for i in range(G['nvertices'])]
    distance = [float('inf') for i in range(G['nvertices'])]
    parent = [-1 for i in range(G['nvertices'])]
    print (intree)
    print (distance)
    print (parent)

    distance[s] = 0
    v = s

    while intree[v] is False:
        intree[v] = True

        for p in G['edges'][v]:
            w = p['y']
            weight = p['weight']
            if distance[w] > (distance[v] + weight):
                distance[w] = distance[v] + weight
                parent[w] = v

        v = 0
        dist = float('inf')
        for i in range(G['nvertices']):
            if intree[i] == False and dist > distance[i]:
                dist = distance[i]
                v = i

    print (distance)
    print (parent)
    print (distance[t])

    path = [t]
    iter = t
    while iter != s:
        iter = parent[iter]
        path.append(iter)
    print(path)

    return distance[t]


class TestMe(unittest.TestCase):
    def test_Dijkstra(self):
        with open(os.path.join('trailmaps', 'percywarner.pkl')) as f:
            g = pickle.load(f)

        newg = Convert(g)
        # print (json.dumps(newg, indent=2))

        all_v_names = [v.name for v in g.vertices]
        v_names = [v.name for v in g.vertices if v.type == 'trailhead']
        for name in v_names:
            print (name)

        print
        print v_names[0], 'to', v_names[-1]
        Dijkstra(newg, all_v_names.index(v_names[0]), all_v_names.index(v_names[-1]))


if __name__ == '__main__':
    # Let's have some fun'
    unittest.main()
