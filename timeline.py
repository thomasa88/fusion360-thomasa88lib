# Timeline querying and manipulation.
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

TIMELINE_STATUS_OK = 0
TIMELINE_STATUS_PRODUCT_NOT_READY = 1
TIMELINE_STATUS_NOT_PARAMETRIC = 2

OCCURRENCE_NOT_OCCURRENCE = -1
OCCURRENCE_UNKNOWN_COMP = 0
OCCURRENCE_NEW_COMP = 1
OCCURRENCE_COPY_COMP = 2
OCCURRENCE_SHEET_METAL = 3
OCCURRENCE_BODIES_COMP = 4

def get_timeline():
    app = adsk.core.Application.get()

    # activeProduct throws if start-up is not completed
    if not app.isStartupComplete: # Backup solution: app.documents.count == 0:
        return (TIMELINE_STATUS_PRODUCT_NOT_READY, None)

    product = app.activeProduct
    if product is None or product.classType() != 'adsk::fusion::Design':
        return (TIMELINE_STATUS_PRODUCT_NOT_READY, None)
    
    design = adsk.fusion.Design.cast(product)

    if design.designType == adsk.fusion.DesignTypes.ParametricDesignType:
        return (TIMELINE_STATUS_OK, design.timeline)
    else:
        return (TIMELINE_STATUS_NOT_PARAMETRIC, None)

def flatten_timeline(timeline_collection):
    '''
    A flat timeline representation, with all objects except any group objects.
    (Groups disappear when expanded - The icon is no longer there in the timeline.)
    '''
    flat_collection = []
    
    for obj in timeline_collection:
        if obj.isGroup:
            # Groups only appear in the timeline if they are collapsed
            # In that case, the features inside the group are only listed within the group
            # and not as part of the top-level timeline. So timeline essentially gives us
            # what is literally shown in the timeline control in Fusion.

            # Flatten the group
            flat_collection += flatten_timeline(obj)
        else:
            flat_collection.append(obj)

    return flat_collection

def get_occurrence_type(timeline_obj):
    '''Heuristics to determine component creation feature'''
    
    if timeline_obj.entity.classType() != 'adsk::fusion::Occurrence':
        return OCCURRENCE_NOT_OCCURRENCE

    # When prefixed with a "type prefix", we can be sure of the occurence type.
    # In that case, the name of the timeline object cannot be edited.
    # This, of course, assumes that the user does not create a component starting
    # with such a string.
    split_name = timeline_obj.name.split(' ', maxsplit=1)
    # User can have input spaces, so a length of split_name > 1 does not automatically
    # mean that we have a type prefix. So let's try.
    # TODO: We can probably compare with the component name to find out if this is
    #       indeed a prefix.
    potential_type_prefix = split_name[0]
    if potential_type_prefix == '':
        return OCCURRENCE_NEW_COMP
        # I have not found any way to determine if a component is a sheet metal component.
        # Solid features are allowed in sheet metal components and sheet metal features are
        # allowed in "normal" components, so cannot use the content as a differentiator.
        #return OCCURRENCE_SHEET_METAL
    if potential_type_prefix == 'CopyPaste':
        return OCCURRENCE_COPY_COMP

    if hasattr(timeline_obj.entity, 'bRepBodies'):
        return OCCURRENCE_BODIES_COMP

    return OCCURRENCE_UNKNOWN_COMP
