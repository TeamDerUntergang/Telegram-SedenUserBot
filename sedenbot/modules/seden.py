# Copyright (C) 2020 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from sedenbot import KOMUT
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
        edit(message, get_translation('sedenUsage2', ['**', '`']))
        metin = '{}\n'.format(get_translation('sedenShowLoadedModules', [
            '**', '`', len(cmds)]))
        for item in cmds:
            metin += f'• `{item}`\n'
        reply(message, metin, preview=False)
