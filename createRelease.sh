#!/bin/bash

# Halt on errors
set -e

# Compile frontend
pushd ui
npm install
npm run build-prod
popd

# Clear ui folder and copy compiled code over
rm -rf selfservice/ui/*
cp -r ui/www/* selfservice/ui/

# Create archive
tar cfvz selfservice.tar.gz selfservice/
