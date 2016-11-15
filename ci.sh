#!/usr/bin/env bash

set -euo pipefail

PYTHON="$(which python3 2>/dev/null || which python)"

echo "Tests and code coverage"
"$PYTHON" -m nose2 --with-coverage --coverage-report=html
echo "PEP8"
"$PYTHON" -m pep8 *.py
echo "PyLint"
"$PYTHON" -m pylint *.py
echo "OK!"