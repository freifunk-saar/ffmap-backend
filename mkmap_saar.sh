#!/bin/bash

set -e

DEST=$1


[ "$DEST" ] || exit 1

cd "$(dirname "$0")"

# ./bat2nodes.py -A -a aliases.json -a aliases_hl.json -a aliases_moelln.json -d $DEST
sudo ./bat2nodes.py -A -a aliases_saar.json -d $DEST

sudo alfred-json -z -r 165 > $DEST"traffic.json"
