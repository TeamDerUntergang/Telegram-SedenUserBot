# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from random import choice, randint
from time import sleep

from pyrogram import ContinuePropagation, StopPropagation
from sedenbot import HELP, PM_AUTO_BAN, TEMP_SETTINGS, app
from sedenecem.core import (
    edit,
    extract_args,
    get_translation,
    reply,
    sedenify,
    send_log,
)

# ========================= CONSTANTS ============================
AFKSTR = [get_translation(f'afkstr{i+1}') for i in range(0, 22)]
TEMP_SETTINGS['AFK_USERS'] = {}
TEMP_SETTINGS['IS_AFK'] = False
TEMP_SETTINGS['COUNT_MSG'] = 0
# =================================================================


@sedenify(
    incoming=True,
    outgoing=False,
    disable_edited=True,
    private=False,
    bot=False,
    disable_notify=True,
)
def mention_afk(msg):
    me = TEMP_SETTINGS['ME']
    mentioned = msg.mentioned
    rep_m = msg.reply_to_message
    if mentioned or rep_m and rep_m.from_user and rep_m.from_user.id == me.id:
        if TEMP_SETTINGS['IS_AFK']:
            if msg.from_user.id not in TEMP_SETTINGS['AFK_USERS']:
                if 'AFK_REASON' in TEMP_SETTINGS:
                    reply(
                        msg,
                        get_translation(
                            "afkMessage2",
                            [
                                '**',
                                me.first_name,
                                me.id,
                                '`',
                                TEMP_SETTINGS['AFK_REASON'],
                            ],
                        ),
                    )
                else:
                    reply(msg, f"```{choice(AFKSTR)}```")
                TEMP_SETTINGS['AFK_USERS'].update({msg.from_user.id: 1})
                TEMP_SETTINGS['COUNT_MSG'] = TEMP_SETTINGS['COUNT_MSG'] + 1
            else:
                if TEMP_SETTINGS['AFK_USERS'][msg.from_user.id] % randint(1, 2) == 0:
                    if 'AFK_REASON' in TEMP_SETTINGS:
                        reply(
                            msg,
                            get_translation(
                                "afkMessage2",
                                [
                                    '**',
                                    me.first_name,
                                    me.id,
                                    '`',
                                    TEMP_SETTINGS['AFK_REASON'],
                                ],
                            ),
                        )
                    else:
                        reply(msg, f"```{choice(AFKSTR)}```")
                    TEMP_SETTINGS['AFK_USERS'][msg.from_user.id] = (
                        TEMP_SETTINGS['AFK_USERS'][msg.from_user.id] + 1
                    )
                    TEMP_SETTINGS['COUNT_MSG'] = TEMP_SETTINGS['COUNT_MSG'] + 1
                else:
                    TEMP_SETTINGS['AFK_USERS'][msg.from_user.id] = (
                        TEMP_SETTINGS['AFK_USERS'][msg.from_user.id] + 1
                    )
                    TEMP_SETTINGS['COUNT_MSG'] = TEMP_SETTINGS['COUNT_MSG'] + 1
    raise ContinuePropagation


@sedenify(
    incoming=True,
    outgoing=False,
    disable_errors=True,
    group=False,
    bot=False,
    disable_notify=True,
)
def afk_on_pm(message):
    if PM_AUTO_BAN:
        try:
            from sedenecem.sql.pm_permit_sql import is_approved

            apprv = is_approved(message.from_user.id)
        except BaseException:
            apprv = True
    else:
        apprv = True
    if apprv and TEMP_SETTINGS['IS_AFK']:
        me = TEMP_SETTINGS['ME']
        if message.from_user.id not in TEMP_SETTINGS['AFK_USERS']:
            if 'AFK_REASON' in TEMP_SETTINGS:
                reply(
                    message,
                    get_translation(
                        "afkMessage2",
                        ['**', me.first_name, me.id, '`', TEMP_SETTINGS['AFK_REASON']],
                    ),
                )
            else:
                reply(message, f"```{choice(AFKSTR)}```")
            TEMP_SETTINGS['AFK_USERS'].update({message.from_user.id: 1})
            TEMP_SETTINGS['COUNT_MSG'] = TEMP_SETTINGS['COUNT_MSG'] + 1
        else:
            if TEMP_SETTINGS['AFK_USERS'][message.from_user.id] % randint(1, 2) == 0:
                if 'AFK_REASON' in TEMP_SETTINGS:
                    reply(
                        message,
                        get_translation(
                            "afkMessage2",
                            [
                                '**',
                                me.first_name,
                                me.id,
                                '`',
                                TEMP_SETTINGS['AFK_REASON'],
                            ],
                        ),
                    )
                else:
                    reply(message, f"```{choice(AFKSTR)}```")
                TEMP_SETTINGS['AFK_USERS'][message.from_user.id] = (
                    TEMP_SETTINGS['AFK_USERS'][message.from_user.id] + 1
                )
                TEMP_SETTINGS['COUNT_MSG'] = TEMP_SETTINGS['COUNT_MSG'] + 1
            else:
                TEMP_SETTINGS['AFK_USERS'][message.from_user.id] = (
                    TEMP_SETTINGS['AFK_USERS'][message.from_user.id] + 1
                )
                TEMP_SETTINGS['COUNT_MSG'] = TEMP_SETTINGS['COUNT_MSG'] + 1
    raise ContinuePropagation


@sedenify(pattern=r'^.afk')
def set_afk(message):
    args = extract_args(message)
    if len(args) > 0:
        TEMP_SETTINGS['AFK_REASON'] = args
        edit(
            message,
            get_translation('afkStartReason', ['**', '`', TEMP_SETTINGS['AFK_REASON']]),
        )
    else:
        edit(message, f'**{get_translation("afkStart")}**')
    send_log(get_translation('afkLog'))
    TEMP_SETTINGS['IS_AFK'] = True
    raise StopPropagation


@sedenify()
def type_afk_is_not_true(message):
    if TEMP_SETTINGS['IS_AFK']:
        TEMP_SETTINGS['IS_AFK'] = False
        reply(message, f'**{get_translation("afkEnd")}**')
        sleep(2)
        send_log(
            get_translation(
                'afkMessages',
                [
                    '`',
                    '**',
                    str(len(TEMP_SETTINGS['AFK_USERS'])),
                    str(TEMP_SETTINGS['COUNT_MSG']),
                ],
            )
        )
        for i in TEMP_SETTINGS['AFK_USERS']:
            name = app.get_chat(i)
            name0 = str(name.first_name)
            send_log(
                get_translation(
                    'afkMentionUsers',
                    ['**', name0, str(i), '`', str(TEMP_SETTINGS['AFK_USERS'][i])],
                )
            )
        TEMP_SETTINGS['COUNT_MSG'] = 0
        TEMP_SETTINGS['AFK_USERS'] = {}
        if 'AFK_REASON' in TEMP_SETTINGS:
            del TEMP_SETTINGS['AFK_REASON']
    raise ContinuePropagation


HELP.update({'afk': get_translation('afkInfo')})
