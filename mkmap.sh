#!/bin/bash

set -e

DEST=$1
FIRMWARE=$2

export PATH=/home/admin/bin:$PATH

[ "$DEST" ] || exit 1

cd "$(dirname "$0")"/

./bat2nodes.py -a aliases-mz.json -m mzBAT -s /var/run/alfred-mz.sock -f $FIRMWARE -d $DEST
#./bat2nodes.py -a aliases-wi.json -m wiBAT -s /var/run/alfred-wi.sock -f $FIRMWARE -d $DEST

