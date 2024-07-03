__Archived: Not actively maintained anymore!__

# SelfService
Container providing Self-Service UI for password-changes, course lists etc.

## Development Requirements
- Node.js
- npm

### build

This can be build i.e. on Ubuntu 20.04. A fresh one can be run in a docker-container with

`docker run --rm -ti -v "$(pwd)":/buildhost ubuntu:20.04 /bin/bash`

and the dependencies can then be installed with

`apt update && apt install npm nodejs`

## Frontend
All frontend code is located at `/ui`. The code in `/selfservice/ui` is the current compiled version.

To setup your development environment, go tu `/ui` and run `npm install`. Then use one of the following commands.

### NPM Scripts

* 🔥 `start` - run development server
* 🔧 `dev` - run development server
* 🔧 `build` - build web app for production

## Backend
The backend code is located at `/selfservice/selfservice`.

## Releasing
You'll have to use the `createRelease.sh` script to create a release. It will compile the frontend, and package the archive.
