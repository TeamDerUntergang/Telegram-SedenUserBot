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

from re import fullmatch, IGNORECASE

from sedenbot import KOMUT, LOG_ID
from sedenecem.core import extract_args, sedenify, edit, get_me, get_messages, reply_msg, reply, forward, send_log
from pyrogram import Message

@sedenify(incoming=True, outgoing=True)
def filter_incoming(message):
    if message.from_user.is_self:
        message.continue_propagation()

    name = message.text
    if not name:
        return

    try:
        from sedenecem.sql.filters_sql import get_filters
    except Exception as e:
        raise e

    filters = get_filters(message.chat.id)

    if not filters:
        return

    for trigger in filters:
        pro = fullmatch(trigger.keyword, name, flags=IGNORECASE)
        if pro:
            if trigger.f_mesg_id:
                msg_o = get_messages(LOG_ID, msg_ids=int(trigger.f_mesg_id))
                if msg_o and len(msg_o) > 0 and not msg_o[-1].empty:
                    msg = msg_o[-1]
                    reply_msg(message, msg)
                else:
                    edit(message, '`Filtre sonucu bulunamadı!`')
            elif trigger.reply:
                reply(message, trigger.reply)
            else:
                edit(message, '`Filtre hatalı!`')

@sedenify(pattern='^.addfilter')
def add_filter(message):
    try:
        from sedenecem.sql.filters_sql import add_filter
    except:
        edit(message, '`Bot Non-SQL modunda çalışıyor!`')
        return
    args = extract_args(message, markdown=True).split(' ', 1)
    if len(args) < 1 or len(args[0]) < 1:
        edit(message, '`Komut kullanımı hatalı.`')
        return
    keyword = args[0]
    string = args[1] if len(args) > 1 else ''
    msg = message.reply_to_message
    msg_id = None

    if len(string) < 1:
        if msg:
            if msg.text:
                string = msg.text.markdown
            else:
                string = None
                msg_o = forward(msg, LOG_ID)
                if not msg_o:
                    edit(message, '`Mesaj yönlendirilemedi ve filtre eklenemedi.`')
                    return
                msg_id = msg_o.message_id
                send_log('#FILTRE'
                    f'\nGrup ID: {message.chat.id}'
                    f'\nFiltre: {keyword}'
                     '\n\nYukarıdaki mesaj filtrenin cevaplanması için kaydedildi, lütfen silmeyin!')
        else:
            edit(message, '`Komut kullanımı hatalı.`')

    success = "**{}** `filtresi {}`"
    if add_filter(str(message.chat.id), keyword, string, msg_id):
        edit(message, success.format(keyword, 'eklendi'))
    else:
        edit(message, success.format(keyword, 'güncellendi'))

@sedenify(pattern='^.stop')
def stop_filter(message):
    try:
        from sedenecem.sql.filters_sql import remove_filter
    except:
        edit(message, '`Bot Non-SQL modunda çalışıyor!`')
        return
    filt = extract_args(message)
    if not remove_filter(message.chat.id, filt):
        edit(message, ' **{}** `filtresi mevcut değil.`'.format(filt))
    else:
        edit(message, '**{}** `filtresi başarıyla silindi`'.format(filt))

@sedenify(pattern='^.filters$')
def filters(message):
    try:
        from sedenecem.sql.filters_sql import get_filters
    except:
        edit(message, '`Bot Non-SQL modunda çalışıyor!`')
        return
    transact = '`Bu sohbette hiç filtre yok.`'
    filters = get_filters(message.chat.id)
    for filt in filters:
        if transact == '`Bu sohbette hiç filtre yok.`':
            transact = 'Sohbetteki filtreler:\n'
            transact += '`{}`\n'.format(filt.keyword)
        else:
            transact += '`{}`\n'.format(filt.keyword)

    edit(message, transact)

KOMUT.update({
    "filter":
    ".filters\
    \nKullanım: Bir sohbetteki tüm userbot filtrelerini listeler.\
    \n\n.addfilter <filtrelenecek kelime> <cevaplanacak metin> ya da bir mesajı .filter <filtrelenecek kelime>\
    \nKullanım: 'filtrelenecek kelime' olarak istenilen şeyi kaydeder.\
    \nBot her 'filtrelenecek kelime' yi algıladığında o mesaja cevap verecektir.\
    \nDosyalardan çıkartmalara her türlü şeyle çalışır.\
    \n\n.stop <filtre>\
    \nKullanım: Seçilen filtreyi durdurur."
})
