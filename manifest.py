# Manifest reader.
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

import json
import os

# Avoid Fusion namespace pollution
from . import utils

def read():
    caller_file = utils.get_caller_path()
    manifest_path = caller_file.replace('.py', '.manifest')
    with open(manifest_path, encoding='utf-8') as manifest_file:
        return json.load(manifest_file)