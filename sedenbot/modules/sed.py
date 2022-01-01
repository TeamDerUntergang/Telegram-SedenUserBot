# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from re import IGNORECASE, I, match, sub
from sre_constants import error as sre_err

from sedenbot import HELP
from sedenecem.core import edit, get_translation, sedenify

DELIMITERS = ('/', ':', '|', '_')


def separate_sed(sed_string):
    if (
        len(sed_string) > 3
        and sed_string[3] in DELIMITERS
        and sed_string.count(sed_string[3]) >= 2
    ):
        delim = sed_string[3]
        start = counter = 4
        while counter < len(sed_string):
            if sed_string[counter] == '\\':
                counter += 1

            elif sed_string[counter] == delim:
                replace = sed_string[start:counter]
                counter += 1
                start = counter
                break

            counter += 1

        else:
            return None

        while counter < len(sed_string):
            if (
                sed_string[counter] == '\\'
                and counter + 1 < len(sed_string)
                and sed_string[counter + 1] == delim
            ):
                sed_string = sed_string[:counter] + sed_string[counter + 1 :]

            elif sed_string[counter] == delim:
                replace_with = sed_string[start:counter]
                counter += 1
                break

            counter += 1
        else:
            return replace, sed_string[start:], ''

        flags = ''
        if counter < len(sed_string):
            flags = sed_string[counter:]
        return replace, replace_with, flags.lower()
    return None


@sedenify(pattern='^sed')
def sed(message):
    sed_result = separate_sed(message.text or message.caption)
    textx = message.reply_to_message
    if sed_result:
        if textx:
            to_fix = textx.text
        else:
            edit(message, f'`{get_translation("sedError")}`')
            return

        repl, repl_with, flags = sed_result

        if not repl:
            edit(message, f'`{get_translation("sedError")}`')
            return

        try:
            check = match(repl, to_fix, flags=IGNORECASE)
            if check and check.group(0).lower() == to_fix.lower():
                edit(message, f'`{get_translation("sedError2")}`')
                return

            if 'i' in flags and 'g' in flags:
                text = sub(repl, repl_with, to_fix, flags=I).strip()
            elif 'i' in flags:
                text = sub(repl, repl_with, to_fix, count=1, flags=I).strip()
            elif 'g' in flags:
                text = sub(repl, repl_with, to_fix).strip()
            else:
                text = sub(repl, repl_with, to_fix, count=1).strip()
        except sre_err:
            edit(message, f'`{get_translation("sedLearn")}`')
            return
        if text:
            edit(message, get_translation('sedResult', [text]))


HELP.update({'sed': get_translation('sedInfo')})
