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

from subprocess import Popen, PIPE
from sys import executable, exc_info
from time import gmtime, strftime
from traceback import format_exc

from pyrogram import Filters, MessageHandler, ContinuePropagation
from sedenbot import (SUPPORT_GROUP, BLACKLIST,
                      BRAIN_CHECKER, me, app, get_translation)
from .sedenlog import send_log_doc
from .misc import edit, _parsed_prefix


def sedenify(**args):
    pattern = args.get('pattern', None)
    outgoing = args.get('outgoing', True)
    incoming = args.get('incoming', False)
    disable_edited = args.get('disable_edited', False)
    disable_notify = args.get('disable_notify', False)
    compat = args.get('compat', True)
    brain = args.get('brain', False)
    private = args.get('private', True)
    group = args.get('group', True)
    bot = args.get('bot', True)
    service = args.get('service', False)

    if pattern and '.' in pattern[:2]:
        args['pattern'] = pattern = pattern.replace('.', _parsed_prefix, 1)

    def msg_decorator(func):
        def wrap(client, message):
            if message.empty:
                return

            try:
                if len(me) < 1:
                    me.append(app.get_me())

                    if me[0].id in BLACKLIST:
                        raise RetardsException('RETARDS CANNOT USE THIS BOT')

                if message.service and not service:
                    return

                if message.chat.type == 'channel':
                    return

                if not bot and message.chat.type == 'bot':
                    message.continue_propagation()

                if not private and message.chat.type in ['private', 'bot']:
                    if not disable_notify:
                        edit(message, f'`{get_translation("groupUsage")}`')
                    return

                if not group and message.chat.type in ['group', 'supergroup']:
                    if not disable_notify:
                        edit(message, f'`{get_translation("privateUsage")}`')
                    return

                if not compat:
                    func(client, message)
                else:
                    func(message)
            except RetardsException:
                try:
                    app.stop()
                except BaseException:
                    pass
            except ContinuePropagation as c:
                raise c
            except Exception as e:
                if disable_notify:
                    return

                try:
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                    if f'{_parsed_prefix}crash' == f'{message.text}'.split()[
                            0]:
                        text = f'{get_translation("logidTest")}'
                    else:
                        edit(message, f'`{get_translation("errorLogSend")}`')
                        link = get_translation("supportGroup", [SUPPORT_GROUP])
                        text = get_translation("sedenErrorText", ['**', link])

                    ftext = get_translation(
                        "sedenErrorText2",
                        [date, message.chat.id, message.from_user.id
                         if message.from_user else "Unknown", message.text,
                         format_exc(),
                         exc_info()[1]])

                    process = Popen(
                        ['git', 'log', '--pretty=format:"%an: %s"', '-10'],
                        stdout=PIPE, stderr=PIPE)
                    out, err = process.communicate()
                    out = f'{out.decode()}\n{err.decode()}'.strip()

                    ftext += out

                    file = open(f'{get_translation("rbgLog")}', 'w+')
                    file.write(ftext)
                    file.close()

                    send_log_doc(f'{get_translation("rbgLog")}',
                                 caption=text, remove_file=True)
                    raise e
                except Exception as x:
                    raise x

        filter = None
        if pattern:
            filter = Filters.regex(pattern)
            if brain:
                filter &= Filters.user(BRAIN_CHECKER)
            if outgoing and not incoming:
                filter &= Filters.me
            elif incoming and not outgoing:
                filter &= (Filters.incoming & ~Filters.bot)
        else:
            if outgoing and not incoming:
                filter = Filters.me
            elif incoming and not outgoing:
                filter = (Filters.incoming & ~Filters.bot)
            else:
                filter = (Filters.me | Filters.incoming) & ~Filters.bot

        if disable_edited:
            filter &= ~Filters.edited

        app.add_handler(MessageHandler(wrap, filter))

    return msg_decorator


class RetardsException(Exception):
    pass
