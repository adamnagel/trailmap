#!/bin/sh
find trailmaps -name *.json | xargs venv/bin/python src/create_graph.py
