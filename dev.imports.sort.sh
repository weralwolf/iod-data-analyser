#!/bin/bash
isort --virtual-env env --dont-skip __init__.py  -rc -y -ac -sl ionospheredata/
isort --virtual-env env --dont-skip __init__.py  -rc -y -ac -sl iod/
isort --virtual-env env -y -ac -sl ./a001_method_spectral_analysis.py
