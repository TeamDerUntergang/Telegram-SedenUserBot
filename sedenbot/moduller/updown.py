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

from os.path import isfile
from sedenecem.events import (download_media_wc, sedenify, edit, 
                              extract_args, reply_doc)

# Copyright (c) @frknkrc44 | 2020
@sedenify(pattern='^.download$')
def download(message):
    reply = message.reply_to_message
    if not reply or not reply.media:
        edit(message, '`Lütfen bir dökümanı alıntılayın.`')
        return

    def progress(current, total):
        edit(message, '`İndiriliyor ... ' +
                      '(%{:.2f})`'.format(current * 100 / total))

    edit(message, '`İndiriliyor ...`')
    media = download_media_wc(reply, progress=progress)
    
    if not media:
        edit(message, '`Henüz yapımcılarım bu türde bir medyayı'
                      ' indirmem için beni ayarlamamış.`')
        return
    
    edit(message, f'`{media}` konumuna başarıyla indirildi.')


@sedenify(pattern='^.upload')
def upload(message):
    args = extract_args(message)

    if len(args) < 1:
        edit(message, '`Buraya hiçliği yükleyemem.`')
        return

    def progress(current, total):
        edit(message, '`Yükleniyor ... ' +
                      '(%{:.2f})`'.format(current * 100 / total) +
                      f'\n{args}')

    if isfile(args):
        try:
            edit(message, f'`Yükleniyor ...`\n{args}')
            reply_doc(message, args, progress=progress)
            edit(message, '`Yükleme tamamlandı!`')
        except Exception as e:
            edit(message, '`Dosya yüklenemedi.`')
            raise e

        return

    edit(message, '`Dosya bulunamadı.`')
