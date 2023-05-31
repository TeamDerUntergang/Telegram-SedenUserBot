# Copyright (C) 2020-2023 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from collections import OrderedDict
from re import match

from sedenbot import HELP
from sedenecem.core import edit, extract_args, get_translation, reply, sedenify


@sedenify(pattern='^.(seden|help)')
def seden_cmds(message):
    args = extract_args(message).lower()
    cmds = OrderedDict(sorted(HELP.items()))

    if not args:
        edit(message, get_translation('sedenUsage2', ['**', '`']))
        metin = f'{get_translation("sedenShowLoadedModules", ["**", "`", len(cmds)])}\n'
        metin += '\n'.join([f'• `{item}`' for item in cmds])
        return reply(message, metin)

    matching_cmds = [cmd for cmd in cmds if match(args, cmd)]
    if matching_cmds:
        edit(message, str(cmds[matching_cmds[0]]))
    else:
        edit(message, f'**{get_translation("sedenUsage")}**')