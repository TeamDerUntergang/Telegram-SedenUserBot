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

@sedenify(pattern='^.notes$')
def notes(message):
    try:
        from sedenecem.sql.notes_sql import get_notes
    except AttributeError:
        edit(message, '`Bot Non-SQL modunda çalışıyor !`')
        return
    reply = '`Bu sohbette kaydedilmiş not bulunamadı`'
    notesx = get_notes(message.chat.id)
    for note in notesx:
        if reply == '`Bu sohbette kaydedilmiş not bulunamadı`':
            reply = 'Bu sohbette kayıtlı notlar:\n'
            reply += '`#{}`\n'.format(note.keyword)
        else:
            reply += '`#{}`\n'.format(note.keyword)
    edit(message, reply)

@sedenify(pattern=r'^.save(.*)')
def save_note(message):
    try:
        from sedenecem.sql.notes_sql import add_note
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
                    edit(message, '`Mesaj yönlendirilemedi ve not eklenemedi.`')
                    return
                msg_id = msg_o.message_id
                send_log('#NOTE'
                    f'\nGrup ID: {message.chat.id}'
                    f'\nFiltre: {keyword}'
                     '\n\nYukarıdaki mesaj notun cevaplanması için kaydedildi, lütfen silmeyin!')
        else:
            edit(message, '`Komut kullanımı hatalı.`')

    success = '`Not başarıyla {}. ` #{} `komutuyla notu çağırabilirsiniz`'
    if add_note(str(message.chat.id), keyword, string, msg_id) is False:
        return edit(message, success.format('güncellendi', keyword))
    else:
        return edit(message, success.format('eklendi', keyword))

@sedenify(pattern=r'^.clear')
def clear_note(message):
    try:
        from sedenecem.sql.notes_sql import rm_note
    except AttributeError:
        edit(message, '`Bot Non-SQL modunda çalışıyor!`')
        return
    notename = extract_args(message)
    if rm_note(message.chat.id, notename) is False:
        edit(message, ' **{}** `notu bulunamadı`'.format(notename))
    else:
        edit(message,
             '**{}** `notu başarıyla silindi`'.format(notename))
        return

@sedenify(pattern=r'^#.*')
def get_note(message):
    try:
        try:
            from sedenecem.sql.notes_sql import get_note
        except:
            edit(message, '`Bot Non-SQL modunda çalışıyor!`')
            return

        notename = message.text.split()[0][1:]
        note = get_note(message.chat.id, notename)

        if note:
            if note.f_mesg_id:
                msg_o = get_messages(LOG_ID, msg_ids=int(note.f_mesg_id))
                if msg_o and len(msg_o) > 0 and not msg_o[-1].empty:
                    msg = msg_o[-1]
                    reply_msg(message, msg)
                else:
                    edit(message, '`Not sonucu bulunamadı!`')
            elif note.reply and len(note.reply) > 0:
                edit(message, note.reply)
            else:
                edit(message, '`Not getirilirken bir sorun oluştu!`')
        else:
            edit(message, '`Not bulunamadı!`')
    except:
        pass

KOMUT.update({
    "notes":
    "\
#<notismi>\
\nKullanım: Belirtilen notu çağırır.\
\n\n.save <not adı> <not olarak kaydedilecek şey> ya da bir mesajı .save <not adı> şeklinde yanıtlayarak kullanılır. \
\nKullanım: Yanıtlanan mesajı ismiyle birlikte bir not olarak kaydeder. \
\n\n.notes\
\nKullanım: Bir sohbetteki tüm notları çağırır.\
\n\n.clear <not adı>\
\nKullanım: Belirtilen notu siler."
})
