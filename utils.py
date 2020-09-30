# Utility functions.
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

import adsk.core, adsk.fusion, adsk.cam, traceback

import inspect
import os
import re

def short_class(obj):
    '''Returns shortened name of Object class'''
    return obj.classType().split('::')[-1]

_DEPLOY_FOLDER_PATTERN = re.compile(r'.*/webdeploy/production/[^/]+')
def get_fusion_deploy_folder():
    '''
    Get the Fusion 360 deploy folder.

    Typically:
     * Windows: C:/Users/<user>/AppData/Local/Autodesk/webdeploy/production/<hash>
     * Mac: /Users/<user>/Library/Application Support/Autodesk/webdeploy/production/<hash>

    NOTE! The structure within the deploy folder is not the same on Windows and Mac!
    E.g. see the examples for get_fusion_ui_resource_folder().
    '''

    # Strip the suffix from the UI resource folder, i.e.:
    # Windows: /Fusion/UI/FusionUI/Resources
    # Mac: /Autodesk Fusion 360.app/Contents/Libraries/Applications/Fusion/Fusion/UI/FusionUI/Resources

    return _DEPLOY_FOLDER_PATTERN.match(get_fusion_ui_resource_folder()).group(0)

_resFolder = None
def get_fusion_ui_resource_folder():
    '''
    Get the Fusion UI resource folder. Note: Not all resources reside here.

    Typically:
     * Windows: C:/Users/<user>/AppData/Local/Autodesk/webdeploy/production/<hash>/Fusion/UI/FusionUI/Resources
     * Mac: /Users/<user>/Library/Application Support/Autodesk/webdeploy/production/<hash>/Autodesk Fusion 360.app/Contents/Libraries/Applications/Fusion/Fusion/UI/FusionUI/Resources
    '''
    global _resFolder
    if not _resFolder:
        app = adsk.core.Application.get()
        _resFolder = app.userInterface.workspaces.itemById('FusionSolidEnvironment').resourceFolder.replace('/Environment/Model', '')
    return _resFolder

def get_caller_path():
    '''Gets the filename of the file calling the function
    that called this function. Used by the library.
    
    That is, is nested in "two steps".
    '''
    caller_file = os.path.abspath(inspect.stack()[2][1])
    return caller_file

def get_file_path():
    '''Gets the filename of the function that called this
    function.'''
    caller_file = os.path.abspath(inspect.stack()[1][1])
    return caller_file

def get_file_dir():
    '''Gets the directory containing the file which function
    called this function.'''
    caller_file = os.path.dirname(os.path.abspath(inspect.stack()[1][1]))
    return caller_file

