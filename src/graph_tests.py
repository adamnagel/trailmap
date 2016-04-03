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

    results = dict()
    results['distance'] = distance
    results['intree'] = intree
    results['parent'] = parent

    path = [t]
    iter = t
    while iter != s:
        iter = parent[iter]
        path.append(iter)

    results['path'] = path

    return results


class TestMe(unittest.TestCase):
    def test_Dijkstra_PercyWarner(self):
        with open(os.path.join('trailmaps', 'percywarner.pkl')) as f:
            g = pickle.load(f)

        g_skiena = g.ToSkiena()

        v_names = [v.name for v in g.vertices]
        th_names = [v.name for v in g.vertices if v.type == 'trailhead']

        results = Dijkstra(g_skiena, v_names.index(th_names[0]), v_names.index(th_names[-1]))

        self.assertSequenceEqual(results['path'], [7, 3, 2, 4, 8, 0, 1])

    def test_Dijkstra_GSMNP(self):
        with open(os.path.join('trailmaps', 'gsmnp.pkl')) as f:
            g = pickle.load(f)

        g_skiena = g.ToSkiena()

        v_names = [v.name for v in g.vertices]
        th_names = [v.name for v in g.vertices if v.type == 'trailhead']

        results = Dijkstra(g_skiena, v_names.index(th_names[0]), v_names.index(th_names[-1]))

        self.assertSequenceEqual(results['path'], [25, 24, 18, 6, 7, 5, 3])

    def test_PercyWarner(self):
        with open(os.path.join('trailmaps', 'percywarner.pkl')) as f:
            g = pickle.load(f)

        v_names = [v.name for v in g.vertices]
        print (json.dumps(sorted(v_names), indent=2))
        self.assertSequenceEqual(sorted(v_names),
                                 sorted(set(v_names)),
                                 'Duplicate vertices exist')

    def test_GSMNP(self):
        with open(os.path.join('trailmaps', 'gsmnp.pkl')) as f:
            g = pickle.load(f)

        v_names = [v.name for v in g.vertices]
        print (json.dumps(sorted(v_names), indent=2))
        self.assertSequenceEqual(sorted(v_names),
                                 sorted(set(v_names)),
                                 'Duplicate vertices exist')


if __name__ == '__main__':
    # Let's have some fun'
    unittest.main()
