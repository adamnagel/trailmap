#!/bin/sh
find trailmaps -name *.json | xargs venv/bin/python create_graph.py