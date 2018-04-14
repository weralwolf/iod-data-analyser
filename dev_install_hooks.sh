#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ln -s $DIR/.hooks/pre-commit.sh $DIR/.git/hooks/pre-commit
chmod a+x $DIR/.git/hooks/pre-commit