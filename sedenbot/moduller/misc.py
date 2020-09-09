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

from random import choice

from sedenbot import KOMUT, SUPPORT_GROUP
from sedenecem.core import edit, extract_args, sedenify, get_translation
from sedenbot.moduller.notes import get_note
from sedenbot.moduller.snips import get_snip


@sedenify(pattern='^.random')
def random(message):
    items = extract_args(message, False)
    args = items.split()
    if len(args) < 2:
        edit(message, f'`{get_translation("randomUsage")}`')
        return

    edit(message, get_translation(
        "randomResult", ['**', '`', items, choice(args)]))


@sedenify(pattern='^.support$')
def support(message):
    edit(message, get_translation("supportResult", [SUPPORT_GROUP]),
         preview=False)


@sedenify(pattern='^.founder')
def founder(message):
    edit(message, get_translation("founderResult", ['`']), preview=False)


@sedenify(pattern='^.readme$')
def readme(message):
    edit(message,
         "[Seden README.md](https://github.com/TeamDerUntergang/Telegram-SedenUserBot/blob/seden/README.md)",
         preview=False)


@sedenify(pattern='^.repo$')
def repo(message):
    edit(message,
         "[Seden Repo](https://github.com/TeamDerUntergang/Telegram-SedenUserBot)",
         preview=False)


@sedenify(pattern='^.repeat')
# Copyright (c) Gegham Zakaryan | 2019
def repeat(message):
    args = extract_args(message).split(' ', 1)
    if len(args) < 2:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    cnt, txt = args
    if not cnt.isdigit():
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + "\n"

    for i in range(0, replyCount - 1):
        replyText += toBeRepeated + "\n"

    edit(message, replyText)


@sedenify(pattern='^.call')
def call_notes(message):
    args = extract_args(message)
    if args.startswith('#'):
        get_note(message)
    elif args.startswith('$'):
        get_snip(message)
    else:
        edit(message, f"`{get_translation('wrongCommand')}`")


@sedenify(pattern='^.crash$')
def crash(message):
    edit(message, f'`{get_translation("testLogId")}`')
    raise Exception(f'`{get_translation("testException")}`')


KOMUT.update({'random': get_translation("randomInfo")})
KOMUT.update({'support': get_translation("supportInfo")})
KOMUT.update({'repo': get_translation("repoInfo")})
KOMUT.update({"readme": get_translation("readmeInfo")})
KOMUT.update({"founder": get_translation("founderInfo")})
KOMUT.update({"repeat": get_translation("repeatInfo")})
KOMUT.update({"call": get_translation("callInfo")})
