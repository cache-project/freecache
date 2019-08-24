#!/bin/bash

export PYTHONPATH="$PYTHONPATH:$(basename "$0")"
python3 -m "$@"
