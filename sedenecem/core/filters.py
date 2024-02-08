# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from asyncio import run
from re import search
from traceback import format_exc
from typing import Callable, List, Union

from pyrogram import ContinuePropagation, StopPropagation
from pyrogram.handlers import RawUpdateHandler
from pyrogram.raw.types import (
    MessageActionContactSignUp,
    MessageService,
    UpdateNewMessage,
)
from pyrogram.types import Message, User

from sedenbot import BLACKLIST, LOGS


class BaseFilter:
    def __init__(self, invert: bool = False):
        self.invert = invert

    def __verify__(self, _: Message):
        raise NotImplementedError

    def verify(self, message: Message):
        if (
            not isinstance(message, Message)
            or not message
            or message.empty
            or not message.from_user
        ):
            return False

        try:
            ret = self.__verify__(message)
            ret = not ret if self.invert else ret
        except (ContinuePropagation, StopPropagation, RetardsException) as e:
            raise e
        except BaseException:
            ret = False
            LOGS.error(format_exc())

        if not ret:
            return message.continue_propagation()

        return True


class AndFilter(BaseFilter):
    def __init__(self, invert: bool = False, *filters: BaseFilter):
        super().__init__(invert)
        self.filters: List[BaseFilter, OrFilter] = []
        self.add_filter(*filters)

    def add_filter(self, *filters: BaseFilter):
        self.filters.extend(filters)

    def __verify__(self, message: Message):
        for item in self.filters:
            if not item.verify(message):
                return False
        return True


class OrFilter(AndFilter):
    def verify(self, message: Message):
        for item in self.filters:
            if item.verify(message):
                return True
        return False


class RegexFilter(BaseFilter):
    def __init__(self, regex: str, invert: bool = False):
        super().__init__(invert)
        self.regex = regex

    def __verify__(self, message: Message):
        return search(self.regex, message.text) if message.text else False


class IncomingFilter(BaseFilter):
    def __init__(self):
        super().__init__(invert=True)

    def __verify__(self, message: Message):
        return message.outgoing


class UserFilter(BaseFilter):
    def __init__(
        self, users: Union[int, List[int], User, List[User]], invert: bool = False
    ):
        super().__init__(invert)
        self.users = users

    def extract_uid(self, user):
        return user.id if type(user) is User else user

    def __verify__(self, message: Message):
        uid = message.from_user.id if message.from_user else 0

        if type(self.users) is List:
            self.users = [self.extract_uid(x) for x in self.users]
        else:
            self.users = [self.extract_uid(self.users)]

        for user in self.users:
            if uid != user:
                return False
        return True


class BotFilter(BaseFilter):
    def __init__(self, invert: bool = False):
        super().__init__(invert)

    def __verify__(self, message: Message):
        return message.from_user.is_bot if message.from_user else False


class MeFilter(BaseFilter):
    def __init__(self, invert: bool = False):
        super().__init__(invert)

    def __verify__(self, message: Message):
        return (
            message.from_user.is_self or message.chat.id == message._client.me.id
            if message.from_user and message.chat
            else False
        )


class SedenUpdateHandler(RawUpdateHandler):
    def __init__(self, callback: Callable, filter: AndFilter, handlers: List):
        super().__init__(self.__callback__)
        self.filter = filter
        self.handlers = handlers
        self.seden_callback = callback

    def __callback__(self, client, update, users, chats):
        if client.me.id in BLACKLIST:
            raise RetardsException('RETARDS CANNOT USE THIS BOT')

        if (
            isinstance(update, UpdateNewMessage)
            and isinstance(update.message, MessageService)
            and isinstance(update.message.action, MessageActionContactSignUp)
        ):
            LOGS.warning('User created an account')
            raise StopPropagation
        else:
            parser = client.dispatcher.update_parsers.get(type(update), None)
            parsed_update, handler_type = (
                run(parser(update, users, chats))
                if parser is not None
                else (None, type(None))
            )

            verified = [i.verify(parsed_update) for i in self.filter.filters]
            if handler_type in self.handlers and all(verified):
                self.seden_callback(parsed_update)
                raise ContinuePropagation


class RetardsException(Exception):
    pass
