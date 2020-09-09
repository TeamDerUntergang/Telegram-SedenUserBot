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

import sedenecem.translator as tr

print('Language keys:', tr.get_language_keys())
print('Language names:', tr.get_language_names())
print('Seden alive:', tr.get_translation('tr', 'sedenAlive'))
print('Seden en fallback:', tr.get_translation('tr', 'sedenGitNotFound'))
print('Seden wrong key:', tr.get_translation('tr', 'wrongKeyExample'))
