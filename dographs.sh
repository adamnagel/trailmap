#!/bin/sh
find data -name *.json | xargs venv/bin/python trailmap/build_trail_graphs.py
