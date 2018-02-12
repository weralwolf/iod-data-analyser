#!/bin/bash

pylint --disable=missing-docstring --rcfile=./ionospheredata/.pylintrc ionospheredata/
pylint --disable=missing-docstring --rcfile=./ionospheredata/.pylintrc iod/
