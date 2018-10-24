#!/bin/sh

echo "Checking type hints..."
docker-compose run --rm type-check
RESULT=$?
[ $RESULT -ne 0 ] && echo "COMMIT REJECTED. mypy errors" && exit 1

echo "Linting code..."
docker-compose run --rm iod flake8
RESULT=$?
[ $RESULT -ne 0 ] && echo "COMMIT REJECTED. Lint errors detected" && exit 1

echo "Verifying imports are sorted..."
docker-compose run --rm iod python -c "import sys; from isort.hooks import git_hook; sys.exit(git_hook(strict=True));"
RESULT=$?
[ $RESULT -ne 0 ] && echo "COMMIT REJECTED. iSort errors" && exit 1

echo "Updating requirements.txt"
pipenv lock -r | sort > requirements.txt
git add -N requirements.txt
REQUIREMENTS_DIFF=`git diff -- requirements.txt`

if [ ! -z "${REQUIREMENTS_DIFF// }" ]; then
  echo "Amend changes of requirements.txt to commit..."
  git add requirements.txt
fi

exit 0
