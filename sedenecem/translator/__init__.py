# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from json import loads
from os import getcwd, listdir, path

pwd = f'{getcwd()}/sedenecem/translator'

translate_cache = {}


def get_language_files():
    items = []
    for i in listdir(pwd):
        if i[-5:] == '.json':
            items.append(i)
    return items


def get_language_keys():
    return [i.replace('.json', '') for i in get_language_files()]


def get_language_names():
    def get_lang_name(item):
        item = f'{pwd}/{item}'
        with open(item, 'r+') as json:
            item = loads(json.read())['langName']
        return item

    return [get_lang_name(i) for i in get_language_files()]


def _get_translation_file(langKey):
    return f'{pwd}/{langKey}.json'


def _get_translation_items_from_cache(langKey):
    json = None
    if langKey not in translate_cache:
        transfile = _get_translation_file(langKey)
        if not path.exists(transfile):
            return {}
        with open(transfile, 'r+') as jsonfile:
            json = loads(jsonfile.read())
            translate_cache[langKey] = json
    else:
        json = translate_cache[langKey]

    return json


def get_translation(langKey, transKey):
    json = None

    if langKey == 'en' or langKey not in get_language_keys():
        json = _get_translation_items_from_cache('en')

        if transKey not in json:
            return transKey
    else:
        json = _get_translation_items_from_cache(langKey)

        if transKey not in json:
            return get_translation('en', transKey)

    return json[transKey]
