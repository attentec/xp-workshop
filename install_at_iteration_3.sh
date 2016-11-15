#!/usr/bin/env bash

set -euo pipefail

pip3 --version
pip3 install pylint
pip3 install pep8
pip3 install nose2
pip3 install cov-core

echo "Installing hook..."
cp ci.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
echo "All done!"