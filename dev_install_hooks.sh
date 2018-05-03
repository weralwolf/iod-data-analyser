#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ln -sf $DIR/.hooks/pre-commit.sh $DIR/.git/hooks/pre-commit
ln -sf $DIR/.hooks/pre-push.sh $DIR/.git/hooks/pre-push
chmod a+x $DIR/.git/hooks/pre-commit
chmod a+x $DIR/.git/hooks/pre-push