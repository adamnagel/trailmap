import glob
import os
import json
from flask import Flask, send_from_directory, make_response
from graphtools.dijkstra import Dijkstra
import pickle
from functools import wraps, update_wrapper
from datetime import datetime


# From http://arusahni.net/blog/2014/03/flask-nocache.html
def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)


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


@nocache
@app.route('/api/<trailsystem>/data')
def fetch_traildata(trailsystem):
    return send_from_directory(path_trailmaps, '{}_render.json'.format(trailsystem))


@nocache
@app.route('/api/<trailsystem>/svg')
def fetch_trailgraph_svg(trailsystem):
    return send_from_directory(path_trailmaps, '{}.svg'.format(trailsystem))


@nocache
@app.route('/api/<trailsystem>/navigate/<src>/<dst>')
def navigate(trailsystem, src, dst):
    with open(os.path.join(path_trailmaps, '{}.pkl'.format(trailsystem))) as f:
        g = pickle.load(f)

    results = g.ShortestPath(src, dst)
    return json.dumps(results)


if __name__ == '__main__':
    # static.run(debug=True)
    app.run()
