# Copyright (C) 2020-2021 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from sedenbot import app

_admin_status_list = ['creator', 'administrator']

def is_admin(message):
    if not 'group' in message.chat.type:
        return True

    user = app.get_chat_member(chat_id=message.chat.id,
                               user_id=message.from_user.id)
    return user.status in _admin_status_list
