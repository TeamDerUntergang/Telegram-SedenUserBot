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

from sedenbot import KOMUT, CHANNEL
from sedenecem.core import (edit, reply, extract_args,
                            sedenify, get_translation)
from collections import OrderedDict


@sedenify(pattern='^.seden')
def seden(message):
    seden = extract_args(message).lower()
    cmds = OrderedDict(sorted(KOMUT.items()))
    if len(seden) > 0:
        if seden in cmds:
            edit(message, str(cmds[seden]))
        else:
            edit(message, f'**{get_translation("sedenUsage")}**')
    else:
        edit(message, get_translation("sedenUsage2", ['**', '`']))
        metin = "{}\n".format(get_translation('sedenShowLoadedModules', [
            '**', 'Seden UserBot', CHANNEL]))
        for item in cmds:
            metin += f'• `{item}`\n'
        reply(message, metin, preview=False)
