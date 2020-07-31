# Utility functions.
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

import adsk.core, adsk.fusion, adsk.cam, traceback

import inspect
import os

def short_class(obj):
    '''Returns shortened name of Object class'''
    return obj.classType().split('::')[-1]

def get_fusion_deploy_folder():
    '''
    Get the Fusion 360 deploy folder.

    Typically: C:/Users/<user>/AppData/Local/Autodesk/webdeploy/production/<hash>
    '''

    return get_fusion_ui_resource_folder().replace('/Fusion/UI/FusionUI/Resources', '')

_resFolder = None
def get_fusion_ui_resource_folder():
    '''
    Get the Fusion UI resource folder. Note: Not all resources reside here.

    Typically: C:/Users/<user>/AppData/Local/Autodesk/webdeploy/production/<hash>/Fusion/UI/FusionUI/Resources
    '''
    global _resFolder
    if not _resFolder:
        app = adsk.core.Application.get()
        _resFolder = app.userInterface.workspaces.itemById('FusionSolidEnvironment').resourceFolder.replace('/Environment/Model', '')
    return _resFolder

def get_caller_path():
    '''Gets the filename of the file calling the function
    that called this function. Used by the library.'''
    caller_file = os.path.abspath(inspect.stack()[2][1])
    return caller_file