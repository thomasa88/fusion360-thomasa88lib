# Persistent settings.
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

import inspect
import json
import os

class SettingsManager:
    def __init__(self, default_values, write_through=True, filename='settings.json'):
        self.default_values = default_values
        self.write_through = write_through
        self.settings = None

        caller_file = os.path.abspath((inspect.stack()[1])[1])
        caller_dir = os.path.dirname(caller_file)
        self.file_path = os.path.join(caller_dir, filename)

        self._read()

    def __getitem__(self, key):
        return self.settings[key]

    def __setitem__(self, key, value):
        self.settings[key] = value
        if self.write_through:
            self.write()

    def write(self):
        with open(self.file_path, 'w+') as f:
            json.dump(self.settings, f)

    def _read(self):
        try:
            with open(self.file_path, 'r') as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            self.settings = self.default_values
            self.write()
