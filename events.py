# Event managing.
# 
# Allows catching events with functions instead of classes.
# Tracks registered events and allows clean-up with one function call.
# All event callbacks are also wrapped in an error.ErrorCatcher().
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

# Avoid Fusion namespace pollution
from . import error

class EventsManager:
    def __init__(self, error_catcher=None):
        self.handlers = []
        self.custom_event_names = []

        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface

        if not error_catcher:
            error_catcher = error.ErrorCatcher()
        self.error_catcher = error_catcher
    
    def clean_up(self):
        self.remove_all_handlers()
        self.unregister_all_events()
    
    def add_handler(self, event, base_class, notify_callback):
        handler_name = base_class.__name__ + '_' + notify_callback.__name__
        handler_class = type(handler_name, (base_class,),
                            { "notify": self._error_catcher_wrapper(notify_callback) })
        handler_class.__init__ = lambda self: super(handler_class, self).__init__()
        handler = handler_class()
        handler_info = (handler, event)

        result = event.add(handler)
        if not result:
            raise Exception('Failed to add handler ' + notify_callback.__name__)
        
        # Avoid garbage collection
        self.handlers.append(handler_info)
        return handler_info

    def remove_handler(self, handler_info):
        handler, event = handler_info
        self.handlers.remove(handler_info)
        event.remove(handler)

    def remove_all_handlers(self):
        for handler, event in self.handlers:
            event.remove(handler)
        self.handlers.clear()
    
    def register_event(self, name):
        # Make sure there is not an old event registered due to a bad stop
        self.app.unregisterCustomEvent(name)

        event = self.app.registerCustomEvent(name)
        if event:
            self.custom_event_names.append(name)
        return event

    def unregister_all_events(self):
        for event_name in self.custom_event_names:
            self.app.unregisterCustomEvent(event_name)
        self.custom_event_names.clear()

    def _error_catcher_wrapper(class_self, func):
        def catcher(func_self, args):
            with class_self.error_catcher:
                func(args)
        return catcher
    
