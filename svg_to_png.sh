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
    INKSCAPE='/c/Program Files/Inkscape/inkscape.exe'
fi

SVG32=$(ls *.svg | grep -v _)
SVG16=$SVG32
if ls *_16.svg &>/dev/null; then
    SVG16=$(echo *_16.svg)
fi
#"$INKSCAPE" -z -w 16 -h 16 -e 16x16.png $SVG16
#"$INKSCAPE" -z -w 32 -h 32 -e 32x32.png $SVG32
#"$INKSCAPE" --export-type=png  $SVG32
"$INKSCAPE" --export-width=16 --export-height=16 -o 16x16.png  $SVG16
"$INKSCAPE" --export-width=32 --export-height=32 -o 32x32.png  $SVG32

