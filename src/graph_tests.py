import pickle
from graphtools.graph import Graph, Edge, Vertex
import os
import unittest
import json
import time


def Dijkstra(G, s, t):
    print ('Dijkstra from:\n\t{}\n\t\tto\n\t{}'.format(s, t))
    print

    start = time.time()

    intree = [False for i in range(G['nvertices'])]
    distance = [float('inf') for i in range(G['nvertices'])]
    parent = [-1 for i in range(G['nvertices'])]
    # print (intree)
    # print (distance)
    # print (parent)

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

    end = time.time()
    print ('Dijkstra time: {0:.3f}ms'.format((end - start) * 1000))
    # print (distance)
    # print (parent)
    # print (distance[t])

    path = [t]
    iter = t
    while iter != s:
        iter = parent[iter]
        path.append(iter)
    print(path)

    return path


class TestMe(unittest.TestCase):
    def test_Dijkstra(self):
        with open(os.path.join('trailmaps', 'percywarner.pkl')) as f:
            g = pickle.load(f)

        start = time.time()
        # newg = Convert(g)
        newg = g.ToSkiena()
        end = time.time()
        print('Conversion time: {0:.3f}ms'.format((end - start) * 1000))
        # print (json.dumps(newg, indent=2))

        all_v_names = [v.name for v in g.vertices]
        v_names = [v.name for v in g.vertices if v.type == 'trailhead']
        for name in v_names:
            print (name)

        print
        print v_names[0], 'to', v_names[-1]
        dist = Dijkstra(newg, all_v_names.index(v_names[0]), all_v_names.index(v_names[-1]))

        self.assertSequenceEqual(dist, [9, 3, 4, 12, 11, 0, 1])


if __name__ == '__main__':
    # Let's have some fun'
    unittest.main()
