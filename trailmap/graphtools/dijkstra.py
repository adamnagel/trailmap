import time


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
