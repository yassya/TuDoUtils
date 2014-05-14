#!/bin/bash

scriptdir=$(dirname $(readlink -f $BASH_SOURCE))

export PYTHONPATH=$scriptdir:$PYTHONPATH
