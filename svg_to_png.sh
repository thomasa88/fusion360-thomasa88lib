#!/bin/bash

# Script for converting an SVG in the current directory to PNGs to
# use for Fusion 360 icons.
#
# This file is part of thomasa88lib, a library of useful Fusion 360
# add-in/script functions.
#
# Copyright (c) 2020 Thomas Axelsson
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

INKSCAPE=inkscape
if ! which $INKSCAPE &> /dev/null; then
    # Try to use Inkspace on Windows in Git Bash
    INKSCAPE='/c/Program Files/Inkscape/bin/inkscape.exe'
fi

if which inkscape | grep -q /snap; then
    # Handle that Inkscape in snap has very limited file access
    SNAP_WORKAROUND=1
fi

if [[ $1 = "" ]]; then
    echo Usage: $0 input.svg SIZE1 SIZE2...
    exit 1
fi

INPUT_FILE=$1
shift
SIZES=$@

INK_INPUT_FILE=$INPUT_FILE
INK_OUTPUT_DIR=.
if [[ $SNAP_WORKAROUND -eq 1 ]]; then
    INK_INPUT_FILE=$HOME/snap/inkscape/current/svg_to_png_input.svg
    INK_OUTPUT_DIR=$HOME/snap/inkscape/current
    cp $INPUT_FILE $INK_INPUT_FILE
fi

for SIZE in $SIZES; do
    OUTPUT_FILE=$INK_OUTPUT_DIR/${SIZE}x${SIZE}.png 
    "$INKSCAPE" --export-width=$SIZE --export-height=$SIZE -o $OUTPUT_FILE $INK_INPUT_FILE
    if [[ $SNAP_WORKAROUND -eq 1 ]]; then
        mv $OUTPUT_FILE .
    fi
done

