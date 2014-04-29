#!/bin/bash

scriptdir=$(dirname $(readlink -f $0))

export PYTHONPATH=$scriptdir:$PYTHONPATH
