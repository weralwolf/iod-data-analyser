#!/bin/sh

PROJECT_DIR=`git rev-parse --show-toplevel`

echo "Clean up pycaches..."
rm -rf `find $PROJECT_DIR -name "*.py[c|o]" -o -name __pycache__`

echo "Running tests..."
docker-compose run --rm iod pytest

RESULT=$?
[ $RESULT -ne 0 ] && echo "PUSH REJECTED. Please fix tests of code" && exit 1

exit 0