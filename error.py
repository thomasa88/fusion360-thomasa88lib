# Error wrapper. Shows a message box and prints a message in the
# debug console.
#
# Typically used instead of try/except in the base of event handlers
# and run()/stop().
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

import adsk

import getpass
import os
import re
import sys
import traceback

# Avoid Fusion namespace pollution
from . import utils
from . import manifest

class ErrorCatcher():
    def __init__(self, msgbox_in_debug=False, msg_prefix=''):
        '''Initialize the error catcher.

        Showing a messagebox is disabled in debugging, by default,
        to avoid the case where Fusion is stopped and the debugger
        fails to reattach on Restart.

        msgbox_in_debug: Show an error message box also when debugging.
        msg_prefix: Prefix error message with this text. E.g. with
                    add-in name and version.

        Usage:

        Globally, to always have the same options set:
        
            error_catcher_ = ErrorCatcher()

        In function:

            with error_catcher_:
                code that can throw
        '''
        self.msgbox_in_debug = msgbox_in_debug
        self.msg_prefix = msg_prefix

    def __enter__(self):
        self.caller_file = utils.get_caller_path()

    def __exit__(self, etype, value, tb):
        if tb:
            app = adsk.core.Application.get()
            ui = app.userInterface

            # Only keep the AddIns/Scripts part of the path
            caller = re.sub(r'.*API[/\\]', '', self.caller_file)

            tb_str = ''.join(traceback.format_exception(etype, value, tb))

            # Shorten file paths, to compact the message
            tb_str = re.sub(r'"[^"]+/(?:API/AddIns|Api/Python)', '"', tb_str)

            # Attempt to scrub the user's username from the traceback, if any remains
            tb_str = tb_str.replace(getpass.getuser(), '<user>')

            message = (f'{self.msg_prefix} error: {value}\n\n' +
                       'Copy this message using Ctrl+C (Windows) or take a screenshot (Mac). ' +
                       'Describe what you did to get this error or record a video.\n\n' +
                       '-' * 50 + '\n\n' +
                       f'{caller} failed: \n\n' +
                       tb_str)
            
            print(message)

            in_debugger = hasattr(sys, 'gettrace') and sys.gettrace()
            if ui and (not in_debugger or self.msgbox_in_debug):
                print("Also showed in message box.")
                ui.messageBox(message)
        
            # Exception handled
            return True
