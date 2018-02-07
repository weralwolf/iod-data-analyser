#!/bin/bash

export PYVERSION="3.5.4"
export LC_ALL=C
PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install $PYVERSION
pyenv local $PYVERSION
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install -r dev-requirements.txt