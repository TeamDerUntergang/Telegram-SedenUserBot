# Copyright (C) 2020 TeamDerUntergang.
#
# SedenUserBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SedenUserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from sedenecem.translator import get_language_files, pwd
from json import dumps, loads

def sort_json(filename):
  json = f'{pwd}/{filename}'
  load = {}
  
  with open(json, 'r+') as jfile:
    load = loads(jfile.read())

  dump = dumps(load, indent=4, sort_keys=True)
  with open(json, 'w+') as jfile:
    jfile.write(dump)

for i in get_language_files():
  print(f'Sorting {i} ...')
  sort_json(i)
  print(f'Sorted {i}!')

print('All jobs completed successfully!')
