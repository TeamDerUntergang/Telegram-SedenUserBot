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

from sedenbot import KOMUT, LOG_ID
from sedenecem.core import extract_args, sedenify, edit, get_messages, reply_msg, reply, forward, send_log

@sedenify(pattern='^.addsnip')
def save_snip(message):
    try:
        from sedenecem.sql.snips_sql import add_snip
    except AttributeError:
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
                    edit(message, '`Mesaj yönlendirilemedi ve küresel not eklenemedi.`')
                    return
                msg_id = msg_o.message_id
                send_log('#SNIP'
                    f'\nFiltre: ${keyword}'
                     '\n\nYukarıdaki mesaj küresel notun cevaplanması için kaydedildi, lütfen silmeyin!')
        else:
            edit(message, '`Komut kullanımı hatalı.`')

    success = '`Snip {}. Kullanım:` **${}** `'
    if add_snip(keyword, string, msg_id) is False:
        edit(message, success.format('güncellendi', keyword))
    else:
        edit(message, success.format('kaydedildi', keyword))

@sedenify(pattern='^.snips$')
def snip_list(message):
    try:
        from sedenecem.sql.snips_sql import get_snips
    except:
        edit(message, '`SQL dışı modda çalışıyor!`')
        return

    list = '`Şu anda hiçbir snip mevcut değil.`'
    all_snips = get_snips()
    for a_snip in all_snips:
        if list == '`Şu anda hiçbir snip mevcut değil.`':
            list = 'Mevcut snipler:\n'
            list += f'`${a_snip.snip}`\n'
        else:
            list += f'`${a_snip.snip}`\n'

    edit(message, list)

@sedenify(pattern='^.remsnip')
def delete_snip(message):
    try:
        from sedenecem.sql.snips_sql import remove_snip
    except AttributeError:
        edit(message, '`SQL dışı modda çalışıyor!`')
        return
    name = extract_args(message)
    if len(name) < 1:
        edit(message, '`Komut kullanımı hatalı.`')
        return
    if remove_snip(name) is True:
        edit(message, f'`snip:` **{name}** `Başarıyla silindi`')
    else:
        edit(message, f'`snip:` **{name}** `Bulunamadı` ')

@sedenify(pattern=r'^\$.*')
def call_snip(message):
    name = message.text
    if not name:
        return

    try:
        try:
            from sedenecem.sql.snips_sql import get_snip
        except:
            edit(message, '`Bot Non-SQL modunda çalışıyor!`')
            return

        snipname = name.split()[0][1:]
        snip = get_snip(snipname)

        if snip:
            if snip.f_mesg_id:
                msg_o = get_messages(LOG_ID, msg_ids=int(snip.f_mesg_id))
                if msg_o and len(msg_o) > 0 and not msg_o[-1].empty:
                    msg = msg_o[-1]
                    reply_msg(message, msg)
                else:
                    edit(message, '`Küresel not sonucu bulunamadı!`')
            elif snip.reply and len(snip.reply) > 0:
                edit(message, snip.reply)
            else:
                edit(message, '`Küresel not getirilirken bir sorun oluştu!`')
        else:
            edit(message, '`Küresel not bulunamadı!`')
    except:
        pass

KOMUT.update({
    "snips":
    "\
$<snip_adı>\
\nKullanım: Belirtilen snipi kullanır.\
\n\n.addsnip <isim> <veri> veya .addsnip <isim> ile bir iletiyi yanıtlayın.\
\nKullanım: Bir snip (küresel not) olarak kaydeder. \
\n\n.snips\
\nKullanım: Kaydedilen tüm snip'leri listeler.\
\n\n.remsnip <snip_adı>\
\nKullanım: Belirtilen snip'i siler."
})
