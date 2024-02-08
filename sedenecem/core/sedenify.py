# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import getpid, kill
from signal import SIGTERM
from subprocess import PIPE, Popen
from sys import exc_info
from time import gmtime, strftime
from traceback import format_exc

from pyrogram import ContinuePropagation, StopPropagation, enums
from pyrogram.handlers import EditedMessageHandler, MessageHandler

from sedenbot import BOT_VERSION, BRAIN, app, get_translation

from .filters import (
    AndFilter,
    BotFilter,
    IncomingFilter,
    MeFilter,
    OrFilter,
    RegexFilter,
    RetardsException,
    SedenUpdateHandler,
    UserFilter,
)
from .misc import _parsed_prefix, edit, get_cmd, is_admin
from .sedenlog import send_log_doc


def sedenify(**args):
    pattern = args.get('pattern', None)
    outgoing = args.get('outgoing', True)
    incoming = args.get('incoming', False)
    disable_edited = args.get('disable_edited', False)
    disable_notify = args.get('disable_notify', False)
    brain = args.get('brain', False)
    private = args.get('private', True)
    group = args.get('group', True)
    bot = args.get('bot', True)
    service = args.get('service', False)
    admin = args.get('admin', False)

    if pattern and '.' in pattern[:2]:
        args['pattern'] = pattern = pattern.replace('.', _parsed_prefix, 1)

    if pattern and pattern[-1:] != '$':
        args['pattern'] = pattern = f'{pattern}(?: |$)'

    def msg_decorator(func):
        def wrap(message):
            if message.empty or not message.from_user:
                return

            try:
                if message.service and not service:
                    return

                if message.chat.type == enums.ChatType.CHANNEL:
                    return

                if not bot and message.chat.type == enums.ChatType.BOT:
                    message.continue_propagation()

                if not private and message.chat.type in [
                    enums.ChatType.PRIVATE,
                    enums.ChatType.BOT,
                ]:
                    if not disable_notify:
                        edit(message, f'`{get_translation("groupUsage")}`')
                    message.continue_propagation()

                if not group and message.chat.type in [
                    enums.ChatType.SUPERGROUP,
                    enums.ChatType.GROUP,
                ]:
                    if not disable_notify:
                        edit(message, f'`{get_translation("privateUsage")}`')
                    message.continue_propagation()

                if admin and not is_admin(message):
                    if not disable_notify:
                        edit(message, f'`{get_translation("adminUsage")}`')
                    message.continue_propagation()
                func(message)
            except RetardsException:
                try:
                    kill(getpid(), SIGTERM)
                except BaseException:
                    pass
            except (ContinuePropagation, StopPropagation) as c:
                raise c
            except Exception as e:
                try:
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                    if get_cmd(message) == 'crash':
                        text = get_translation('logidTest')
                    else:
                        if not disable_notify:
                            edit(message, f'`{get_translation("errorLogSend")}`')
                        text = get_translation(
                            'sedenErrorText', ['**', '`', exc_info()[1]]
                        )

                    ftext = get_translation(
                        'sedenErrorText2',
                        [
                            date,
                            message.chat.id,
                            message.from_user.id if message.from_user else 'Unknown',
                            BOT_VERSION,
                            message.text,
                            format_exc(),
                            exc_info()[1],
                        ],
                    )

                    process = Popen(
                        ['git', 'log', '--pretty=format:"%an: %s"', '-10'],
                        stdout=PIPE,
                        stderr=PIPE,
                    )
                    out, err = process.communicate()
                    out = f'{out.decode()}\n{err.decode()}'.strip()

                    ftext += out

                    file = open(get_translation('rbgLog'), 'w+')
                    file.write(ftext)
                    file.close()

                    send_log_doc(
                        get_translation('rbgLog'), caption=text, remove_file=True
                    )
                    raise e
                except Exception as x:
                    raise x

        filter = AndFilter()
        if pattern:
            filter.add_filter(RegexFilter(pattern))
            if brain:
                filter.add_filter(UserFilter(BRAIN))
            if outgoing and not incoming:
                filter.add_filter(MeFilter())
            elif incoming and not outgoing:
                filter.add_filter(IncomingFilter(), BotFilter(True), MeFilter(True))
        else:
            if outgoing and not incoming:
                filter.add_filter(MeFilter())
            elif incoming and not outgoing:
                filter.add_filter(IncomingFilter(), BotFilter(True), MeFilter(True))
            else:
                filter.add_filter(
                    OrFilter(MeFilter(), IncomingFilter()), BotFilter(True)
                )

        handlers = [MessageHandler]
        if not disable_edited:
            handlers.append(EditedMessageHandler)

        app.add_handler(SedenUpdateHandler(wrap, filter, handlers))

    return msg_decorator
