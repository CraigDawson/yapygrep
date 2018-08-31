#!/bin/sh
# pyan from https://github.com/davidfraser/pyan
pyan.py gui/*.py --uses --no-defines --colored --grouped --annotated --dot >yapgrep.dot
dot -Tsvg yapgrep.dot > yapgrep.svg
rm yapgrep.dot
