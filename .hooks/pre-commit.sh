#!/bin/sh

echo "Linting code..."
docker-compose run --rm iod flake8

RESULT=$?
[ $RESULT -ne 0 ] && echo "COMMIT REJECTED. Lint errors detected" && exit 1

echo "Verifying imports are sorted..."
docker-compose run --rm iod python -c "import sys; from isort.hooks import git_hook; sys.exit(git_hook(strict=True));"

RESULT=$?
[ $RESULT -ne 0 ] && echo "COMMIT REJECTED. iSort errors" && exit 1

exit 0
