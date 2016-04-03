import json
from six import iteritems
import operator
import argparse
import os
from graphtools.graph import Graph, Edge, Vertex
import pickle


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
        loop_distance = None
        for kind, values in iteritems(t_data):
            if kind == "loop":  # Special keyword
                loop_distance = values
                continue
            if values is None:
                continue

            for name, loc in iteritems(values):
                # Intersections have a special naming scheme. Otherwise, just use the name.
                if kind == 'intersections':
                    sorted_names = sorted([t_name, name])  # 'name' is other trail's name
                    v_name = "{0} intersects {1}".format(sorted_names[0], sorted_names[1])
                else:
                    v_name = name

                # Check for existing vertex
                dupes = [v_ for v_ in g.vertices if v_.name == v_name]
                if len(dupes) == 1:
                    v = dupes[0]
                elif len(dupes) > 1:
                    raise ValueError('More than 1 instance of vertex name {} found'.format(v_name))
                else:
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

        if loop_distance is not None:
            v_origin = sorted_trail_items[0]
            e = Edge(v_origin[0], last_v[0],
                     t_name,
                     loop_distance - last_v[1])
            g.add_edge(e)

    print("Vertices Found:")
    for v in sorted(g.vertices, key=lambda vert: (vert.type, vert.name)):
        print("{0}:\t{1}".format(v.type, v.name))

    basename = os.path.splitext(filename)[0]
    g.render(basename)

    with open('{}.pkl'.format(basename), 'w') as f:
        pickle.dump(g, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process trail definitions into a graph')
    parser.add_argument('trail_definition_files', metavar='file', type=str,
                        nargs='+', help='Trail definition file to parse')

    args = parser.parse_args()
    print (args.trail_definition_files)

    for filename in args.trail_definition_files:
        if '_render.json' in filename:
            continue

        print(filename)
        ParseTrailDefinition(filename)
