import json
from six import iteritems
import operator
import pygraphviz as pgv


class Graph(object):
    def __init__(self):
        self.vertices = list()
        self.edges = list()

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def add_edge(self, edge):
        self.edges.append(edge)

    def visualize(self):
        G = pgv.AGraph()
        G.graph_attr['overlap'] = 'scale'
        G.node_attr['shape'] = 'box'
        G.edge_attr['fontsize'] = 10

        nodelist = [v.name for v in self.vertices]
        G.add_nodes_from(nodelist)
        for edge in self.edges:
            label = "{0}: {1}".format(edge.trail_name, edge.distance)
            G.add_edge(edge.point1.name, edge.point2.name, label=label)

        G.layout(prog='neato')
        G.draw('file.png')


class Vertex(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type


class Edge(object):
    def __init__(self, point1, point2, trail_name, distance):
        self.point1 = point1
        self.point2 = point2
        self.distance = distance
        self.trail_name = trail_name


if __name__ == "__main__":
    with open('traildata.json') as f:
        data = json.load(f)

    # Now we want to convert this to a graph.
    # The vertices will be intersections, trailheads, landmarks, and campgrounds.
    # So let's go through and turn each trail into its own graph.
    g = Graph()
    for t_name, t_data in iteritems(data['trails']):
        trail_vertex_locations = dict()

        ### Create vertices
        for kind, values in iteritems(t_data):
            if values is None:
                continue

            for v_raw_name, loc in iteritems(values):
                if kind == 'intersections':
                    # Name intersection by joining the names, alphabetically
                    sorted_names = sorted([t_name, v_raw_name])
                    v_name = "{0} intersects {1}".format(sorted_names[0], sorted_names[1])
                else:
                    v_name = v_raw_name

            v = Vertex(v_name, kind[:-1])
            g.add_vertex(v)
            trail_vertex_locations[v] = loc

        sorted_trail_items = sorted(trail_vertex_locations.items(), key=operator.itemgetter(1))
        last_v = None
        for idx, v in enumerate(sorted_trail_items):
            if idx != 0:
                e = Edge(last_v[0], v[0], t_name,
                         sorted_trail_items[idx][1] - sorted_trail_items[idx - 1][1])
                g.add_edge(e)

            last_v = v

g.visualize()
