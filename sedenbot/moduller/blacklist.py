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
# @NaytSeyd tarafından portlanmıştır.
#

import io
import re

from sedenbot import KOMUT, LOGS
from sedenecem.events import edit, reply, send_log, reply_doc, extract_args, sedenify

from importlib import import_module

def blacklist_init():
    try:
        global sql
        sql = import_module('sedenecem.sql.blacklist_sql')
    except Exception as e:
        sql = None
        LOGS.warn('Karaliste özelliği çalıştırılamıyor, SQL bağlantısı bulunamadı')


blacklist_init()


@sedenify(incoming=True, outgoing=False)
def blacklist(message):
    if not sql:
        return
    name = message.text
    if not name:
        return
    snips = sql.get_chat_blacklist(message.chat.id)
    for snip in snips:
        pattern = r'( |^|[^\w])' + re.escape(snip) + r'( |$|[^\w])'
        if re.search(pattern, name, flags=re.IGNORECASE):
            try:
                message.delete()
            except Exception as e:
                reply(message, 'Bu grupta mesaj silme iznim yok !')
                sql.rm_from_blacklist(event.chat_id, snip.lower())
            break
        pass


@sedenify(pattern='^.addblacklist', compat=False)
def addblacklist(client, message):
    if not sql:
        edit(message, '`SQL dışı modda çalışıyorum, bunu gerçekleştiremem`')
        return
    text = extract_args(message)
    if len(text) < 1:
        edit(message, '`Bana bir metin ver`')
        return
    to_blacklist = list(set(trigger.strip() for trigger in text.split("\n") if trigger.strip()))
    for trigger in to_blacklist:
        sql.add_to_blacklist(message.chat.id, trigger.lower())
    edit(message, f'`{text}` **kelimesi bu sohbet için karalisteye alındı.**'.format(len(to_blacklist)))

    send_log(f"#BLACKLIST\
             \nGrup ID: `{message.chat.id}`\
             \nKelime: `{text}`")


@sedenify(pattern='^.showblacklist$')
def showblacklist(message):
    if not sql:
        edit(message, '`SQL dışı modda çalışıyorum, bunu gerçekleştiremem`')
        return
    all_blacklisted = sql.get_chat_blacklist(message.chat.id)
    OUT_STR = '**Bu grup için ayarlanan karaliste kelimeleri:**\n'
    if len(all_blacklisted) > 0:
        for trigger in all_blacklisted:
            OUT_STR += f'`{trigger}`\n'
    else:
        OUT_STR = '**Karalisteye eklenmiş kelime bulunamadı.**\
                  \n`.addblacklist` **komutu ile ekleyebilirsin.**'
    if len(OUT_STR) > 4096:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = 'blacklist.text'
            reply_doc(message, out_file, caption='**Bu grup için ayarlanan karaliste:**')
            message.delete()
    else:
        edit(message, OUT_STR)


@sedenify(pattern='^.rmblacklist')
def rmblacklist(message):
    if not sql:
        edit(message, '`SQL dışı modda çalışıyorum, bunu gerçekleştiremem`')
        return
    text = extract_args(message)
    if len(text) < 1:
        edit(message, '`Bana bir metin ver`')
        return
    to_unblacklist = list(set(trigger.strip() for trigger in text.split("\n") if trigger.strip()))
    successful = 0
    for trigger in to_unblacklist:
        if sql.rm_from_blacklist(message.chat.id, trigger.lower()):
            successful += 1
    edit(message, f'`{text}` **kelimesi bu sohbet için karalisteden kaldırıldı.**'.format(len(to_unblacklist)))


KOMUT.update({
    "blacklist":
    ".showblacklist\
    \nKullanım: Bir sohbetteki etkin kara listeyi listeler.\
    \n\n.addblacklist <kelime>\
    \nKullanım: İletiyi 'kara liste anahtar kelimesine' kaydeder.\
    \n'Kara liste anahtar kelimesinden' bahsedildiğinde bot iletiyi siler.\
    \n\n.rmblacklist <kelime>\
    \nKullanım: Belirtilen kara listeyi durdurur.\
    \nBu arada bu işlemleri gerçekleştirmek için yönetici olmalı ve **Mesaj Silme** yetkiniz olmalı."
})
