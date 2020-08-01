#!/bin/bash

# Run in bash or Git Bash

set -e

# Safety check. The lib should exist as a subdirectory
# if the user is in the correct directory.
if [[ ! -e .git ]] || [[ ! -e thomasa88lib/.git ]]; then
    echo "Run this script from the add-in's top directory."
    exit 1
fi

APP_NAME=$(basename "$PWD")
VERSION=$(git describe --tags --dirty)

echo "App:     $APP_NAME"
echo "Version: $VERSION"

if [[ $VERSION =~ dirty ]]; then
    echo
    read -p "The repository is dirty. Continue anyway? [yN] " -n 1 -r
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo Aborted
        exit 1
    fi
fi

ARCHIVE_NAME="$APP_NAME-$VERSION.zip"

mkdir -p release

git archive --format=zip -o release/app.zip HEAD
git -C thomasa88lib archive --format=zip --prefix=thomasa88lib/ -o ../release/lib.zip HEAD

pushd release > /dev/null
rm -rf -- unpacked_release

mkdir unpacked_release
pushd unpacked_release > /dev/null
unzip -q ../app.zip
unzip -q ../lib.zip

git init --quiet
git add .
git commit --quiet -m 'ZIP'
git archive --format=zip --prefix="$APP_NAME/" -o "../$ARCHIVE_NAME" HEAD

popd > /dev/null
rm app.zip lib.zip
rm -rf -- unpacked_release

echo
echo Release file: release/$ARCHIVE_NAME