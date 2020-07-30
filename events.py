# Event managing.
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

class EventsManager:
    def __init__(self, addin_name='Add-in'):
        self.handlers = []
        self.custom_event_names = []
        self.addin_name = addin_name

        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface
    
    def add_handler(self, event, base_class, notify_callback):
        handler_name = base_class.__name__ + '_' + notify_callback.__name__
        handler_class = type(handler_name, (base_class,),
                            { "notify": self.error_catcher_wrapper(notify_callback) })
        handler_class.__init__ = lambda self: super(handler_class, self).__init__()
        handler = handler_class()
        # Avoid garbage collection
        self.handlers.append((handler, event))
        result = event.add(handler)
        if not result:
            raise Exception('Failed to add handler ' + notify_callback.__name__)

    def error_catcher_wrapper(self, func):
        addin_name = self.addin_name
        ui = self.ui
        def catcher(self, args):
            try:
                func(args)
            except:
                print(f'{addin_name} event handler failure:\n{traceback.format_exc()}')
                if ui:
                    ui.messageBox(f'Copy this message using Ctrl+C.\n\n{addin_name} ' +
                                  f'event handler failure:\n{traceback.format_exc()}')
        return catcher
    
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
    
    def clean_up(self):
        self.remove_all_handlers()
        self.unregister_all_events()
