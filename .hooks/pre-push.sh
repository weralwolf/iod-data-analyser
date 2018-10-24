#!/bin/sh

PROJECT_DIR=`git rev-parse --show-toplevel`

echo "Running tests..."
docker-compose run --rm test

RESULT=$?
[ $RESULT -ne 0 ] && echo "PUSH REJECTED. Please fix tests of code" && exit 1

exit 0
