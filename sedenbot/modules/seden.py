# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from collections import OrderedDict

from sedenbot import HELP
from sedenecem.core import edit, extract_args, get_translation, reply, sedenify


@sedenify(pattern='^.(seden|help)')
def seden(message):
    seden = extract_args(message).lower()
    cmds = OrderedDict(sorted(HELP.items()))
    if len(seden) > 0:
        if seden in cmds:
            edit(message, str(cmds[seden]))
        else:
            edit(message, f'**{get_translation("sedenUsage")}**')
    else:
        edit(message, get_translation('sedenUsage2', ['**', '`']))
        metin = f'{get_translation("sedenShowLoadedModules", ["**", "`", len(cmds)])}\n'
        for item in cmds:
            metin += f'• `{item}`\n'
        reply(message, metin)
