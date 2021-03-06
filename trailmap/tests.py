import pickle
from graphtools.dijkstra import Dijkstra
import os
import unittest
import json

path_thisfile = os.path.dirname(os.path.realpath(__file__))
path_traildata = os.path.join(path_thisfile, '..', 'data')


class TestMe(unittest.TestCase):
    def setUp(self):
        pass

    @unittest.skip("Test needs updating. Node numbers will change as the trail system develops.")
    def test_Dijkstra_PercyWarner(self):
        with open(os.path.join(path_traildata, 'percywarner.pkl')) as f:
            g = pickle.load(f)

        g_skiena = g.ToSkiena()

        v_names = [v.name for v in g.vertices]
        th_names = [v.name for v in g.vertices if v.type == 'trailhead']

        results = Dijkstra(g_skiena, v_names.index(th_names[0]), v_names.index(th_names[-1]))

        self.assertSequenceEqual(results['path'], [7, 3, 2, 4, 8, 0, 1])
        print(results['path'])

    @unittest.skip("Test needs updating. Node numbers will change as the trail system develops.")
    def test_Dijkstra_GSMNP(self):
        with open(os.path.join(path_traildata, 'gsmnp.pkl')) as f:
            g = pickle.load(f)

        g_skiena = g.ToSkiena()

        v_names = [v.name for v in g.vertices]
        th_names = [v.name for v in g.vertices if v.type == 'trailhead']

        results = Dijkstra(g_skiena, v_names.index(th_names[0]), v_names.index(th_names[-1]))

        self.assertSequenceEqual(results['path'], [25, 24, 18, 6, 7, 5, 3])

    def test_Dijkstra_WithPath(self):
        with open(os.path.join(path_traildata, 'edwinwarner.pkl')) as f:
            g = pickle.load(f)

        results = g.ShortestPath('Owl Hollow Trailhead', 'Quarry')
        print(json.dumps(results, indent=2))

        expected = [
            {"distance": 0, "point": "Owl Hollow Trailhead"},
            {"distance": 0.0, "point": "Harpeth Woods Trail intersects Owl Hollow Trail"},
            {"distance": 0.3999999999999999, "point": "Quarry"}
        ]
        self.assertSequenceEqual(results, expected)

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
