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

from sqlite3 import connect
from sys import version_info
from os.path import isfile
from os import environ, listdir, path, remove
from re import search as resr
from distutils.util import strtobool as sb
from importlib import import_module
from logging import basicConfig, getLogger, INFO, DEBUG, CRITICAL
from requests import get
from pyrogram import Client, Filters, MessageHandler
from dotenv import load_dotenv
load_dotenv("config.env")

if version_info[0] < 3 or version_info[1] < 8:
    LOGS.warn("En az python 3.8 sürümüne sahip olmanız gerekir. "
              "Birden fazla özellik buna bağlıdır. Bot kapatılıyor.")
    quit(1)

KOMUT = {}
BRAIN_CHECKER = []
BLACKLIST = []
VALID_PROXY_URL = []
ASYNC_POOL = []
CONVERSATION = {}

# Ayrıntılı konsol günlügü
LOG_VERBOSE = sb(environ.get("LOG_VERBOSE", "False"))

basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=DEBUG if LOG_VERBOSE else INFO,
)

# Copyright (c) @NaytSeyd, @frknkrc44 | 2020
def set_logger():
    # String session değerini dışarı yazdırmayı kapatır
    pyrogram_syncer = getLogger('pyrogram.client.ext.syncer')
    pyrogram_syncer.setLevel(CRITICAL)

    # Bazı önemsiz çıktıları kapatır
    pyrogram_session = getLogger('pyrogram.session.session')
    pyrogram_session.setLevel(CRITICAL)

set_logger()

LOGS = getLogger(__name__)

# Yapılandırmanın önceden kullanılan değişkeni kullanarak düzenlenip düzenlenmediğini kontrol edin.
# Temel olarak, yapılandırma dosyası için kontrol.
CONFIG_CHECK = environ.get(
    "___________LUTFEN_______BU_____SATIRI_____SILIN__________", None)

if CONFIG_CHECK:
    LOGS.warn("Lütfen ilk belirtilen satırı config.env dosyasından kaldırın")
    quit(1)

# Telegram APP ID ve HASH
API_ID = environ.get("API_ID", None)
if not API_ID:
    LOGS.warn("API ID Ayarlanmadı. Lütfen config.env dosyasınız kontrol edin.")
    quit(1)

API_HASH = environ.get("API_HASH", None)
if not API_HASH:
    LOGS.warn("API HASH Ayarlanmadı. Lütfen config.env dosyasınız kontrol edin.")
    quit(1)

BOT_VERSION = "1.0 Beta"
SUPPORT_GROUP = "SedenUserBotSupport"
CHANNEL = "SedenUserBot"

# Hava durumu varsayılan şehir
WEATHER = environ.get("WEATHER", None)

# Genius modülü
GENIUS_TOKEN = environ.get("GENIUS_TOKEN", None) or environ.get("GENIUS", None)

# Alive Mesajını değiştirme
ALIVE_MESAJI = environ.get("ALIVE_MESAJI", "Merhaba Seden! Seni Seviyorum ❤️")

# Chrome sürücüsü ve Google Chrome dosyaları
CHROME_DRIVER = environ.get("CHROME_DRIVER", "chromedriver")

# OCR API key
OCR_APIKEY = environ.get("OCR_APIKEY", None)

# RBG API key
RBG_APIKEY = environ.get("RBG_APIKEY", None)

# SQL Veritabanı
DATABASE_URL = environ.get("DATABASE_URL", None)

# İndirme konumu
DOWNLOAD_DIRECTORY = environ.get("DOWNLOAD_DIRECTORY", "./downloads")

# SedenBot String Session
SESSION = environ.get("SESSION", 'sedenuserbot')

# SedenBot güncellemesi için depo adresi
REPO_URL = environ.get("REPO_URL", "https://github.com/TeamDerUntergang/SedenUserBot")

# Heroku bilgileri
HEROKU_KEY = environ.get("HEROKU_KEY", None)
HEROKU_APPNAME = environ.get("HEROKU_APPNAME", None)

# Bot kayıtları için sohbet numarası
LOG_ID = environ.get("LOG_ID", None)
LOG_ID = int(LOG_ID) if LOG_ID and resr(r'^-?\d+$', LOG_ID) else None

# Test sunucusuna bağlantı kur
#
# Normal kullanıcılar için değildir
# Ayrı hesabınız olur ama normal sunucudaki
# mesajlara erişemezsiniz veya oradan bu hesaba
# ulaşım sağlayamazsınız
#
# Deep Telegram adıyla da bilinir
#
# Daha fazla bilgi: https://docs.pyrogram.org/topics/test-servers
DEEPGRAM = sb(environ.get('DEEPGRAM', "False"))

def load_brain():
    if path.exists("learning-data-root.check"):
        remove("learning-data-root.check")
    URL = 'https://raw.githubusercontent.com/NaytSeyd/databasescape/master/learning-data-root.check'
    with open('learning-data-root.check', 'wb') as load:
        load.write(get(URL).content)
    DB = connect("learning-data-root.check")
    CURSOR = DB.cursor()
    CURSOR.execute("""SELECT * FROM BRAIN1""")
    ALL_ROWS = CURSOR.fetchall()
    for i in ALL_ROWS:
        BRAIN_CHECKER.append(i[0])
    DB.close()

def load_bl():
    if path.exists("blacklist.check"):
        remove("blacklist.check")
    URL = 'https://raw.githubusercontent.com/NaytSeyd/databaseblacklist/master/blacklist.check'
    with open('blacklist.check', 'wb') as load:
        load.write(get(URL).content)
    DB = connect("blacklist.check")
    CURSOR = DB.cursor()
    CURSOR.execute("SELECT * FROM RETARDS")
    ALL_ROWS = CURSOR.fetchall()
    for i in ALL_ROWS:
        BLACKLIST.append(i[0])
    DB.close()

load_brain()
load_bl()

me = []

class PyroClient(Client):

    @staticmethod
    def store_msg(_, message):
        try:
            chat = message.chat
            if chat.id in CONVERSATION:
                CONVERSATION[chat.id].append(message)
            elif chat.username and chat.username in CONVERSATION:
                CONVERSATION[chat.username].append(message)
        except:
            pass
        message.continue_propagation()

    def __init__(self, session, **args):
        super().__init__(session, **args)
        self.add_handler(MessageHandler(PyroClient.store_msg, Filters.incoming))

app = PyroClient(
    SESSION,
    api_id=API_ID,
    api_hash=API_HASH,
    app_version=f"Seden v{BOT_VERSION}",
    device_model="Der Untergang",
    system_version=f"v{BOT_VERSION}",
    lang_code="tr",
    test_mode=DEEPGRAM,
)

def __get_modules():
    folder = 'sedenbot/moduller'
    modules = [
        f[:-3] for f in listdir(folder)
        if isfile(f"{folder}/{f}") and f[-3:] == '.py' and f != '__init__.py'
    ]
    return modules

def __import_modules():
    modules = __get_modules()
    LOGS.info(f'Yüklenecek modüller: {modules}')
    for module in modules:
        try:
            LOGS.info(f'Yüklenen modül: {module}')
            import_module(f'sedenbot.moduller.{module}')
        except Exception as e:
            if LOG_VERBOSE:
                raise e
            LOGS.warn(f"{module} modülü yüklenirken bir hata oluştu.")

__import_modules()

LOGS.info("Botun çalışıyor! Herhangi bir sohbete .alive yazarak test edebilirsin, "
          ".seden yazarak modüllerin listesini alabilirsin. "
          f"Yardıma ihtiyacın varsa, destek grubumuza bakabilirsin https://t.me/{SUPPORT_GROUP}")
LOGS.info(f"Bot sürümü; Seden v{BOT_VERSION}")
