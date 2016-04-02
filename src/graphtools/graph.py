import pygraphviz as pgv


class Edge(object):
    def __init__(self, point1, point2, trail_name, distance):
        self.point1 = point1
        self.point2 = point2
        self.distance = distance
        self.trail_name = trail_name


class Vertex(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type


class Graph(object):
    def __init__(self):
        self.vertices = list()
        self.edges = list()

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def add_edge(self, edge):
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
        G.write('{0}.dot'.format(name))
