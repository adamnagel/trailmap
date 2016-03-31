import json
from six import iteritems
import operator
import pygraphviz as pgv
import argparse
import sys
import os


class Graph(object):
    def __init__(self):
        self.vertices = list()
        self.edges = list()

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def add_edge(self, edge):
        self.edges.append(edge)

    def render(self, name):
        G = pgv.AGraph()
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


def ParseTrailDefinition(filename):
    with open(filename) as f:
        data = json.load(f)

    # Now we want to convert this to a graph.
    # The vertices will be intersections, trailheads, landmarks, and campgrounds.
    # So let's go through and turn each trail into its own graph.
    g = Graph()
    for t_name, t_data in iteritems(data['trails']):
        trail_vertex_locations = dict()

        # Create vertices from key points
        for kind, values in iteritems(t_data):
            if values is None:
                continue

            v_name = None
            for name, loc in iteritems(values):
                # Intersections have a special naming scheme. Otherwise, just use the name.
                if kind == 'intersections':
                    sorted_names = sorted([t_name, name])  # 'name' is other trail's name
                    v_name = "{0} intersects {1}".format(sorted_names[0], sorted_names[1])
                else:
                    v_name = name

                v = Vertex(v_name, kind[:-1])
                g.add_vertex(v)
                trail_vertex_locations[v] = loc

        sorted_trail_items = sorted(trail_vertex_locations.items(), key=operator.itemgetter(1))
        last_v = None
        for idx, v in enumerate(sorted_trail_items):
            if idx != 0:
                e = Edge(last_v[0], v[0],
                         t_name,
                         sorted_trail_items[idx][1] - sorted_trail_items[idx - 1][1])
                g.add_edge(e)

            last_v = v

    print("Vertices Found:")
    for v in sorted(g.vertices, key=lambda vert: (vert.type, vert.name)):
        print("{0}:\t{1}".format(v.type, v.name))

    basename = os.path.splitext(filename)[0]
    g.render(basename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process trail definitions into a graph')
    parser.add_argument('trail_definition_files', metavar='file', type=str,
                        nargs='+', help='Trail definition file to parse')

    args = parser.parse_args()
    print (args.trail_definition_files)

    for filename in args.trail_definition_files:
        ParseTrailDefinition(filename)

