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


from random import choice, randint
from time import sleep

from pyrogram import ContinuePropagation, StopPropagation

from sedenbot import (KOMUT, TEMP_SETTINGS, PM_AUTO_BAN, app, me as mel)
from sedenecem.core import (extract_args, sedenify, send_log,
                            edit, reply, get_translation)

# ========================= CONSTANTS ============================

AFKSTR = [get_translation(f'afkstr{i+1}') for i in range(0, 22)]
# =================================================================

TEMP_SETTINGS['AFK_USERS'] = {}
TEMP_SETTINGS['IS_AFK'] = False
TEMP_SETTINGS['COUNT_MSG'] = 0


@sedenify(incoming=True, outgoing=False, disable_edited=True,
          private=False, bot=False, disable_notify=True)
def mention_afk(mention):
    me = mel[0]
    if mention.mentioned or mention.reply_to_message and mention.reply_to_message.from_user and mention.reply_to_message.from_user.id == me.id:
        if TEMP_SETTINGS['IS_AFK']:
            if mention.from_user.id not in TEMP_SETTINGS['AFK_USERS']:
                if 'AFK_REASON' in TEMP_SETTINGS:
                    reply(
                        mention, get_translation(
                            "afkMessage2", [
                                '**', me.first_name, me.id, '`', TEMP_SETTINGS['AFK_REASON']]))
                else:
                    reply(mention, f"```{choice(AFKSTR)}```")
                TEMP_SETTINGS['AFK_USERS'].update({mention.from_user.id: 1})
                TEMP_SETTINGS['COUNT_MSG'] = TEMP_SETTINGS['COUNT_MSG'] + 1
            else:
                if TEMP_SETTINGS['AFK_USERS'][
                        mention.from_user.id] % randint(
                        2, 4) == 0:
                    if 'AFK_REASON' in TEMP_SETTINGS:
                        reply(
                            mention, get_translation(
                                "afkMessage2", [
                                    '**', me.first_name, me.id, '`', TEMP_SETTINGS['AFK_REASON']]))
                    else:
                        reply(mention, f"```{choice(AFKSTR)}```")
                    TEMP_SETTINGS['AFK_USERS'][
                        mention.from_user.id] = TEMP_SETTINGS['AFK_USERS'][
                        mention.from_user.id] + 1
                    TEMP_SETTINGS['COUNT_MSG'] = TEMP_SETTINGS['COUNT_MSG'] + 1
                else:
                    TEMP_SETTINGS['AFK_USERS'][
                        mention.from_user.id] = TEMP_SETTINGS['AFK_USERS'][
                        mention.from_user.id] + 1
                    TEMP_SETTINGS['COUNT_MSG'] = TEMP_SETTINGS['COUNT_MSG'] + 1
    raise ContinuePropagation


@sedenify(incoming=True, outgoing=False, disable_errors=True,
          group=False, bot=False, disable_notify=True)
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
        me = mel[0]
        if message.from_user.id not in TEMP_SETTINGS['AFK_USERS']:
            if 'AFK_REASON' in TEMP_SETTINGS:
                reply(
                    mention, get_translation(
                        "afkMessage2", [
                            '**', me.first_name, me.id, '`', TEMP_SETTINGS['AFK_REASON']]))
            else:
                reply(message, f"```{choice(AFKSTR)}```")
            TEMP_SETTINGS['AFK_USERS'].update({message.from_user.id: 1})
            TEMP_SETTINGS['COUNT_MSG'] = TEMP_SETTINGS['COUNT_MSG'] + 1
        else:
            if TEMP_SETTINGS['AFK_USERS'][
                    message.from_user.id] % randint(
                    2, 4) == 0:
                if 'AFK_REASON' in TEMP_SETTINGS:
                    reply(
                        mention, get_translation(
                            "afkMessage2", [
                                '**', me.first_name, me.id, '`', TEMP_SETTINGS['AFK_REASON']]))
                else:
                    reply(message, f"```{choice(AFKSTR)}```")
                TEMP_SETTINGS['AFK_USERS'][
                    message.from_user.id] = TEMP_SETTINGS['AFK_USERS'][
                    message.from_user.id] + 1
                TEMP_SETTINGS['COUNT_MSG'] = TEMP_SETTINGS['COUNT_MSG'] + 1
            else:
                TEMP_SETTINGS['AFK_USERS'][
                    message.from_user.id] = TEMP_SETTINGS['AFK_USERS'][
                    message.from_user.id] + 1
                TEMP_SETTINGS['COUNT_MSG'] = TEMP_SETTINGS['COUNT_MSG'] + 1
    raise ContinuePropagation


@sedenify(pattern=r"^.afk")
def set_afk(message):
    args = extract_args(message)
    if len(args) > 0:
        TEMP_SETTINGS['AFK_REASON'] = args
        edit(
            message, get_translation(
                "afkStartReason", [
                    '**', '`', TEMP_SETTINGS['AFK_REASON']]))
    else:
        edit(message, f'**{get_translation("afkStart")}**')
    send_log(get_translation("afkLog"))
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
                "afkMessages",
                ['`', '**', str(len(TEMP_SETTINGS['AFK_USERS'])),
                 str(TEMP_SETTINGS['COUNT_MSG'])]))
        for i in TEMP_SETTINGS['AFK_USERS']:
            name = app.get_chat(i)
            name0 = str(name.first_name)
            send_log(
                get_translation(
                    "afkMentionUsers",
                    ['**', name0, str(i),
                     '`', str(TEMP_SETTINGS['AFK_USERS'][i])]))
        TEMP_SETTINGS['COUNT_MSG'] = 0
        TEMP_SETTINGS['AFK_USERS'] = {}
        if 'AFK_REASON' in TEMP_SETTINGS:
            del TEMP_SETTINGS['AFK_REASON']
    raise ContinuePropagation


KOMUT.update({"afk": get_translation("afkInfo")})
