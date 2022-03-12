# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import name

if name == 'nt':
    print('Uninstall Windows to use this bot')
    quit(1)

from distutils.util import strtobool as sb
from importlib import import_module
from logging import CRITICAL, DEBUG, INFO, basicConfig, getLogger
from os import environ, listdir, path, remove
from os.path import isfile
from pathlib import PurePath
from re import search as resr
from sqlite3 import connect
from sys import version_info
from traceback import format_exc
from typing import Any, Dict

import sedenecem.translator as _tr
from dotenv import load_dotenv, set_key, unset_key
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from requests import get


def reload_env():
    return load_dotenv('config.env', override=True)


reload_env()

LOGS = getLogger(__name__)

#
# Bot lang
#
# If missted, the default lang is English.
SEDEN_LANG = environ.get('SEDEN_LANG', 'en')


def get_translation(transKey, params: list = None):
    ret = _tr.get_translation(SEDEN_LANG, transKey)

    if params and len(params) > 0:
        for i in reversed(range(len(params))):
            ret = ret.replace(f'%{i+1}', str(params[i]))

    ret = ret.replace('½', '%')

    return ret


if version_info[0] < 3 or version_info[1] < 8:
    LOGS.warn(get_translation('pythonVersionError'))
    quit(1)

HELP: Dict[str, str] = {}
BRAIN = []
BLACKLIST = []
CONVERSATION: Dict[Any, Any] = {}
TEMP_SETTINGS: Dict[Any, Any] = {}
TEMP_SETTINGS['PM_COUNT'] = {}
TEMP_SETTINGS['PM_LAST_MSG'] = {}

# Console verbose logging
LOG_VERBOSE = sb(environ.get('LOG_VERBOSE', 'False'))

basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=DEBUG if LOG_VERBOSE else INFO,
)


def set_local_env(key: str, value: str):
    return set_key(PurePath('config.env'), key, value)


def unset_local_env(key: str):
    if key in environ:
        del environ[key]
    return unset_key(PurePath('config.env'), key)


def set_logger():
    # Turns off out printing Session value
    pyrogram_syncer = getLogger('pyrogram.syncer')
    pyrogram_syncer.setLevel(CRITICAL)

    # Closes some junk outputs
    pyrogram_session = getLogger('pyrogram.session.session')
    pyrogram_session.setLevel(CRITICAL)

    pyrogram_auth = getLogger('pyrogram.session.auth')
    pyrogram_auth.setLevel(CRITICAL)


set_logger()

# Telegram APP ID and HASH
API_ID = environ.get('API_ID', None)
if not API_ID:
    LOGS.warn(get_translation('apiIdError'))
    quit(1)

API_HASH = environ.get('API_HASH', None)
if not API_HASH:
    LOGS.warn(get_translation('apiHashError'))
    quit(1)

BOT_VERSION = '1.5.5'
SUPPORT_GROUP = 'SedenUserBotSupport'
CHANNEL = 'SedenUserBot'

# Weather default city
WEATHER = environ.get('WEATHER', None)

# Genius module
GENIUS_TOKEN = environ.get('GENIUS_TOKEN', None) or environ.get('GENIUS', None)

# Spoify Client ID
SPOTIPY_CLIENT_ID = environ.get('SPOTIPY_CLIENT_ID')

# SPotify Client SECRET
SPOTIPY_CLIENT_SECRET = environ.get('SPOTIPY_CLIENT_SECRET')

# Gdrive Folder ID
GDRIVE_FOLDER_ID = environ.get('GDRIVE_FOLDER_ID', None)

# Change Alive Message
ALIVE_MSG = environ.get('ALIVE_MSG', None)

# For neofetch
HOSTNAME = environ.get('HOSTNAME', 'DerUntergang')
USER = environ.get('USER', 'sedenecem')

# Chrome Driver and Headless Google Chrome Binaries
CHROME_DRIVER = environ.get('CHROME_DRIVER', 'chromedriver')

# OCR API key
OCR_APIKEY = environ.get('OCR_APIKEY', None)

# Auto pp link
AUTO_PP = environ.get('AUTO_PP', None)

# RBG API key
RBG_APIKEY = environ.get('RBG_APIKEY', None)

# Custom sticker pack
PACKNAME = environ.get('PACKNAME', None)
PACKNICK = environ.get('PACKNICK', None)

# SQL Database URL
DATABASE_URL = environ.get('DATABASE_URL', None)

# SedenBot Session
SESSION = environ.get('SESSION', 'sedenify')

# SedenBot repo url for updater
REPO_URL = environ.get(
    'REPO_URL', 'https://github.com/TeamDerUntergang/Telegram-SedenUserBot'
)

# Heroku Credentials for updater
HEROKU_KEY = environ.get('HEROKU_KEY', None)
HEROKU_APPNAME = environ.get('HEROKU_APPNAME', None)

# SpamWatch API key
SPAMWATCH_KEY = environ.get('SPAMWATCH_KEY', None)

# Chat ID for Bot Logs
_LOG_ID = environ.get('LOG_ID', None)
LOG_ID = int(_LOG_ID) if _LOG_ID and resr(r'^-?\d+$', _LOG_ID) else None
del _LOG_ID

# PmPermit PM Auto Ban Stuffs
PM_AUTO_BAN = sb(environ.get('PM_AUTO_BAN', 'False'))
_PM_MSG_COUNT = environ.get('PM_MSG_COUNT', 'default')
PM_MSG_COUNT = int(_PM_MSG_COUNT) if _PM_MSG_COUNT.isdigit() else 5
del _PM_MSG_COUNT
PM_UNAPPROVED = environ.get('PM_UNAPPROVED', None)

# Bot Prefix (Defaults to dot)
BOT_PREFIX = environ.get('BOT_PREFIX', None)

ENV_RESTRICTED_KEYS = ['HEROKU_KEY', 'HEROKU_APPNAME', 'SESSION', 'API_ID', 'API_HASH']


def load_brain():
    try:
        if path.exists('learning-data-root.check'):
            remove('learning-data-root.check')
        URL = (
            'https://raw.githubusercontent.com/NaytSeyd/'
            'databasescape/master/learning-data-root.check'
        )
        with open('learning-data-root.check', 'wb') as load:
            load.write(get(URL).content)
        DB = connect('learning-data-root.check')
        CURSOR = DB.cursor()
        CURSOR.execute('SELECT * FROM BRAIN1')
        ALL_ROWS = CURSOR.fetchall()
        for i in ALL_ROWS:
            BRAIN.append(i[0])
        DB.close()
    except BaseException:
        pass


def load_bl():
    try:
        if path.exists('blacklist.check'):
            remove('blacklist.check')
        URL = (
            'https://raw.githubusercontent.com/NaytSeyd/'
            'databaseblacklist/master/blacklist.check'
        )
        with open('blacklist.check', 'wb') as load:
            load.write(get(URL).content)
        DB = connect('blacklist.check')
        CURSOR = DB.cursor()
        CURSOR.execute('SELECT * FROM RETARDS')
        ALL_ROWS = CURSOR.fetchall()
        for i in ALL_ROWS:
            BLACKLIST.append(i[0])
        DB.close()
    except BaseException:
        pass


load_brain()
load_bl()


class PyroClient(Client):
    @staticmethod
    def store_msg(_, message):
        try:
            chat = message.chat
            if chat.id in CONVERSATION:
                CONVERSATION[chat.id].append(message)
            elif chat.username and chat.username in CONVERSATION:
                CONVERSATION[chat.username].append(message)
        except BaseException:
            pass
        message.continue_propagation()

    def __init__(self, session, **args):
        super().__init__(session, **args)
        self.add_handler(MessageHandler(PyroClient.store_msg, filters.incoming))

    def start(self):
        super().start()
        LOGS.info(get_translation('runningBot', [SUPPORT_GROUP]))
        LOGS.info(get_translation('sedenVersion', [BOT_VERSION]))

    def stop(self):
        super().stop()
        LOGS.info(get_translation('goodbyeMsg'))

    def export_session_string(self):
        raise NotImplementedError


app = PyroClient(
    SESSION,
    api_id=API_ID,
    api_hash=API_HASH)


# delete these variables to add some security
del SESSION
del API_ID
del API_HASH


def __get_modules():
    folder = 'sedenbot/modules'
    modules = [
        f[:-3]
        for f in listdir(folder)
        if isfile(f'{folder}/{f}') and f[-3:] == '.py' and f != '__init__.py'
    ]
    return modules


def __import_modules():
    modules = sorted(__get_modules())
    LOGS.info(get_translation('loadedModules', [modules]))
    for module in modules:
        try:
            import_module(f'sedenbot.modules.{module}')
        except Exception:
            if LOG_VERBOSE:
                LOGS.warn(format_exc())
            LOGS.warn(get_translation('loadedModulesError', [module]))


__import_modules()
