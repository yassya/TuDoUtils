#!/bin/bash

if [[ ${BASH_SOURCE} = "" ]]; then
	echo "Cannot determine location of package dir"
	exit 1
else
	scriptdir=$(dirname $(readlink -f $BASH_SOURCE))

	export PYTHONPATH=$scriptdir:$PYTHONPATH
fi
