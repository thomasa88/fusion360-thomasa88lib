# Helper functions for Fusion Commands.
#
# This file is part of thomasa88lib, a library of useful Fusion 360
# add-in/script functions.
#
# Copyright (c) 2023 Thomas Axelsson
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

import adsk

import getpass
import os
import re
import sys
import traceback

# Avoid Fusion namespace pollution
from . import utils
from . import manifest

def try_delete_cmd_def(cmd_id):
    app = adsk.core.Application.get()
    ui = app.userInterface
    cmd_def = ui.commandDefinitions.itemById(cmd_id)
    if cmd_def:
        cmd_def.deleteMe()

def recreate_checkbox_def(cmd_id, name, tooltip, is_checked):
    try_delete_cmd_def(cmd_id)
    app = adsk.core.Application.get()
    ui = app.userInterface
    return ui.commandDefinitions.addCheckBoxDefinition(cmd_id, name, tooltip, is_checked)
