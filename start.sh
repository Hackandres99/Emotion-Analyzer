#!/bin/sh
python download_models.py
waitress-serve --port=8000 run:app
