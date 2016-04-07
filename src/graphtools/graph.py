import pygraphviz as pgv
import os
import json
import time


class Edge(object):
    def __init__(self, point1, point2, trail_name, distance):
        self.point1 = point1
        self.point2 = point2
        self.distance = distance
        self.trail_name = trail_name

    def to_dict(self):
        return {'point1': self.point1.name,
                'point2': self.point2.name,
                'distance': self.distance,
                'trail_name': self.trail_name}


class Vertex(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def to_dict(self):
        return {'type': self.type}


class Graph(object):
    def __init__(self):
        self.vertices = list()
        self.edges = list()
        self._uptodate = False
        self._skiena = None

    def add_vertex(self, vertex):
        self._uptodate = False
        self.vertices.append(vertex)

    def add_edge(self, edge):
        self._uptodate = False
        self.edges.append(edge)

    def render(self, name):
        G = pgv.AGraph(strict=False)
        G.graph_attr['overlap'] = 'scale'
        G.node_attr['shape'] = 'box'
        G.edge_attr['fontsize'] = 10

        for vertex in self.vertices:
            G.add_node(vertex.name)

        for edge in self.edges:
            label = '{0}: {1}'.format(edge.trail_name, edge.distance)
            G.add_edge(edge.point1.name, edge.point2.name, label=label)

        G.layout(prog='neato')
        G.draw('{0}.png'.format(name))
        G.draw('{0}.svg'.format(name))
        G.write('{0}.dot'.format(name))

        # Create JSON extract
        with open('{0}_render.json'.format(name), 'w') as f:
            d = {'vertices': dict(), 'edges': list()}
            for v in self.vertices:
                type = v.type
                if type not in d['vertices']:
                    d['vertices'][type] = dict()

                d['vertices'][type][v.name] = v.to_dict()

            for e in self.edges:
                d['edges'].append(e.to_dict())

            json.dump(d, f, indent=2)

        # Create Skiena representation
        self._skiena = self.ToSkiena()
        self._uptodate = True

    def ToSkiena(self):
        if self._uptodate:
            return self._skiena

        rtn = dict()
        rtn['nvertices'] = len(self.vertices)
        rtn['nedges'] = len(self.edges)
        rtn['directed'] = False
        rtn['degree'] = []
        rtn['edges'] = []

        for i, v in enumerate(self.vertices):
            # Find the outdegree (number of edges for this vertex)
            outdegree = sum([1 for e in self.edges
                             if e.point1.name == v.name or e.point2.name == v.name])
            rtn['degree'].append(outdegree)

            edges = []
            for e in self.edges:
                if e.point1.name == v.name:
                    edge = {
                        'y': self.vertices.index(e.point2),
                        'weight': e.distance
                    }
                    edges.append(edge)
                elif e.point2.name == v.name:
                    edge = {
                        'y': self.vertices.index(e.point1),
                        'weight': e.distance
                    }
                    edges.append(edge)

            rtn['edges'].append(edges)

        return rtn


def Dijkstra(G, s, t):
    """Use Dijkstra's algorithm to find the shortest path between two points.

    :param G: The problem graph, according to the Skiena convention
    :param s: The index of the start node
    :param t: The index of the end node
    :return: The shortest path as an array of vertex indeces
    """
    print ('Dijkstra from:\n\t{}\n\t\tto\n\t{}'.format(s, t))

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
