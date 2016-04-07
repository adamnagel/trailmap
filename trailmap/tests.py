import pickle
from graphtools.graph import Dijkstra
import os
import unittest
import json

path_thisfile = os.path.dirname(os.path.realpath(__file__))
path_traildata = os.path.join(path_thisfile, '..', 'data')

class TestMe(unittest.TestCase):
    def setUp(self):
        pass

    def test_Dijkstra_PercyWarner(self):
        with open(os.path.join(path_traildata, 'percywarner.pkl')) as f:
            g = pickle.load(f)

        g_skiena = g.ToSkiena()

        v_names = [v.name for v in g.vertices]
        th_names = [v.name for v in g.vertices if v.type == 'trailhead']

        results = Dijkstra(g_skiena, v_names.index(th_names[0]), v_names.index(th_names[-1]))

        self.assertSequenceEqual(results['path'], [7, 3, 2, 4, 8, 0, 1])

    def test_Dijkstra_GSMNP(self):
        with open(os.path.join(path_traildata, 'gsmnp.pkl')) as f:
            g = pickle.load(f)

        g_skiena = g.ToSkiena()

        v_names = [v.name for v in g.vertices]
        th_names = [v.name for v in g.vertices if v.type == 'trailhead']

        results = Dijkstra(g_skiena, v_names.index(th_names[0]), v_names.index(th_names[-1]))

        self.assertSequenceEqual(results['path'], [25, 24, 18, 6, 7, 5, 3])

    def test_PercyWarner(self):
        with open(os.path.join(path_traildata, 'percywarner.pkl')) as f:
            g = pickle.load(f)

        v_names = [v.name for v in g.vertices]
        print (json.dumps(sorted(v_names), indent=2))
        self.assertSequenceEqual(sorted(v_names),
                                 sorted(set(v_names)),
                                 'Duplicate vertices exist')

    def test_GSMNP(self):
        with open(os.path.join(path_traildata, 'gsmnp.pkl')) as f:
            g = pickle.load(f)

        v_names = [v.name for v in g.vertices]
        print (json.dumps(sorted(v_names), indent=2))
        self.assertSequenceEqual(sorted(v_names),
                                 sorted(set(v_names)),
                                 'Duplicate vertices exist')


if __name__ == '__main__':
    # Let's have some fun'
    unittest.main()
