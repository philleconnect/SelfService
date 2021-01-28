# SelfService
Container providing Self-Service UI for password-changes, course lists etc.

## Development Requirements
- Node.js
- npm

## Frontend
All frontend code is located at `/ui`. The code in `/selfservice/ui` is the current compiled version.

To setup your development environment, go tu `/ui` and run `npm install`. Then use one of the following commands.

### NPM Scripts

* 🔥 `start` - run development server
* 🔧 `dev` - run development server
* 🔧 `build-dev` - build web app using development mode (faster build without minification and optimization)
* 🔧 `build-prod` - build web app for production

## Backend
The backend code is located at `/selfservice/selfservice`.

## Releasing
You'll have to use the `createRelease.sh` script to create a release. It will compile the frontend, and package the archive.
