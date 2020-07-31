# Error wrapper. Shows a message box and prints a message in the
# debug console.
#
# This file is part of thomasa88lib, a library of useful Fusion 360
# add-in/script functions.
#
# Copyright (C) 2020  Thomas Axelsson
#
# thomasa88lib is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# thomasa88lib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with thomasa88lib.  If not, see <https://www.gnu.org/licenses/>.


import adsk

import os
import re
import sys
import traceback

# Avoid Fusion namespace pollution
from . import utils

class ErrorCatcher():
    def __init__(self, msgbox_in_debug=False):
        '''Initialize the error catcher.

        Showing a messagebox is disabled in debugging, by default,
        to avoid the case where Fusion is stopped and the debugger
        fails to reattach on Restart.

        msgbox_in_debug: Show an error message box also when debugging.


        Usage:

        Globally, to always have the same options set:
        
            error_catcher_ = ErrorCatcher()

        In function:

            with error_catcher_:
                code that can throw
        '''
        self.msgbox_in_debug = msgbox_in_debug

    def __enter__(self):
        self.caller_file = utils.get_caller_path()

    def __exit__(self, etype, value, tb):
        if tb:
            app = adsk.core.Application.get()
            ui = app.userInterface

            # Only keep the AddIns/Scripts part of the path
            caller = re.sub(r'.*API[/\\]', '', self.caller_file)

            tb_str = ''.join(traceback.format_exception(etype, value, tb))

            message = ('Copy this message using Ctrl+C:\n\n' +
                        f'{caller} failed:\n\n' +
                        tb_str)
            
            print(message)

            in_debugger = hasattr(sys, 'gettrace')
            if not in_debugger or self.msgbox_in_debug:
                print("Also showed in message box.")
                ui.messageBox(message)
        
            # Exception handled
            return True
