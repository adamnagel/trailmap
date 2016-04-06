import glob
import os
import json
from flask import Flask, send_from_directory

app = Flask(__name__)
path_thisfile = os.path.dirname(__file__)
path_static = os.path.join(path_thisfile, 'static')
print ('Static files being served from: {}'.format(path_static))
path_trailmaps = os.path.join(path_thisfile, '..', 'trailmaps')


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


if __name__ == '__main__':
    # static.run(debug=True)
    app.run()
