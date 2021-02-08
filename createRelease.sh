#!/bin/bash

# Halt on errors
set -e

# Paths
COMPILED_GUI="selfservice/ui"
ARCHIVE="selfservice.tar.gz"
CONTAINER_DEST="selfservice/"

# Cleanup
if [ -d "$COMPILED_GUI" ]; then
  rm -rf $COMPILED_GUI
fi
if [ -f "$ARCHIVE" ]; then
  rm -rf $ARCHIVE
fi

# Compile frontend
pushd ui
npm install
npm run build
popd

# Create ui folder and copy compiled code over
mkdir $COMPILED_GUI
cp -r ui/www/* "$COMPILED_GUI/"

# Create archive
tar cfvz $ARCHIVE $CONTAINER_DEST
