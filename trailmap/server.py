import glob
import os
import json
from flask import Flask, send_from_directory
from graphtools.graph import Dijkstra
import pickle

app = Flask(__name__)
path_thisfile = os.path.dirname(__file__)
path_static = os.path.join(path_thisfile, 'static')
print ('Static files being served from: {}'.format(path_static))
path_trailmaps = os.path.join(path_thisfile, '..', 'data')


@app.route('/')
def return_home():
    return static_proxy('index.html')


@app.route('/<path:path>')
def static_proxy(path):
    print (path_static, path)
    return send_from_directory(path_static, str(path))


@app.route('/api/list_trailsystems')
def list_trailsystems():
    rtn = dict()
    files = glob.glob(path_trailmaps + '/*.json')
    rtn['trailsystems'] = [os.path.basename(os.path.splitext(f)[0])
                           for f in files if not '_render' in f]
    return json.dumps(rtn)


@app.route('/api/<trailsystem>/data')
def fetch_traildata(trailsystem):
    return send_from_directory(path_trailmaps, '{}_render.json'.format(trailsystem))


@app.route('/api/<trailsystem>/svg')
def fetch_trailgraph_svg(trailsystem):
    return send_from_directory(path_trailmaps, '{}.svg'.format(trailsystem))


@app.route('/api/<trailsystem>/navigate/<src>/<dst>')
def navigate(trailsystem, src, dst):
    with open(os.path.join(path_trailmaps, '{}.pkl'.format(trailsystem))) as f:
        g = pickle.load(f)

    v_names = [v.name for v in g.vertices]

    results = Dijkstra(g.ToSkiena(), v_names.index(src), v_names.index(dst))
    path = reversed(results['path'])
    path_asnames = [v_names[i] for i in path]

    return json.dumps(path_asnames)


if __name__ == '__main__':
    # static.run(debug=True)
    app.run()
