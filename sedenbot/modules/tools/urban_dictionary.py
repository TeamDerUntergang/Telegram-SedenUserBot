# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from json import loads
from os import path, remove
from random import randrange

from requests import get

from sedenbot import HELP
from sedenecem.core import edit, extract_args, get_translation, reply_doc, sedenify


@sedenify(pattern='^.ud')
def urbandictionary(message):
    query = extract_args(message)
    if len(query) < 1:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    edit(message, f'`{get_translation("processing")}`')
    response = get(f'https://api.urbandictionary.com/v0/define?term={query}')
    data = loads(response.text)
    if len(data["list"]):
        list_size = len(data['list'])
        item = data['list'][randrange(list_size)]
        meanlen = item['definition'] + item['example']
        if len(meanlen) >= 4096:
            edit(message, f'`{get_translation("outputTooLarge")}`')
            file = open('urban_dictionary.txt', 'w+')
            file.write(
                f"Query: {query}\n\n"
                f"Meaning: {item['definition']}\n\n"
                f"Example: \n{item['example']}\n"
            )
            file.close()
            reply_doc(
                message,
                'urbandictionary.txt',
                caption=f'`{get_translation("outputTooLarge")}`',
            )
            if path.exists('urbandictionary.txt'):
                remove('urbandictionary.txt')
            message.delete()
            return
        edit(
            message,
            get_translation(
                'sedenQueryUd',
                ['**', '`', query, item['definition'], item['example']],
            ),
        )
    else:
        edit(message, get_translation('udNoResult', ['**', query]))


HELP.update({'ud': get_translation('udInfo')})
