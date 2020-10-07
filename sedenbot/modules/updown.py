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
from sedenbot import KOMUT
from sedenecem.core import (download_media_wc, sedenify, edit,
                            extract_args, reply_doc, get_translation)

# Copyright (c) @frknkrc44 | 2020


@sedenify(pattern='^.download$')
def download(message):
    reply = message.reply_to_message
    if not reply or not reply.media:
        edit(message, f'`{get_translation("downloadReply")}`')
        return

    def progress(current, total):
        edit(message, get_translation('updownDownload', [
             '`', '(½{:.2f})'.format(current * 100 / total)]))

    edit(message, f'`{get_translation("downloadMedia")}`')
    media = download_media_wc(reply, progress=progress)

    if not media:
        edit(message, f'`{get_translation("downloadMediaError")}`')
        return

    edit(message, get_translation('updownDownloadSuccess', ['`', media]))


@sedenify(pattern='^.upload')
def upload(message):
    args = extract_args(message)

    if len(args) < 1:
        edit(message, f'`{get_translation("uploadReply")}`')
        return

    def progress(current, total):
        edit(message, get_translation('updownUpload', [
             '`', '(½{:.2f})'.format(current * 100 / total), args]))

    if isfile(args):
        try:
            edit(message, get_translation('updownUpload', ['`', '', args]))
            reply_doc(message, args, progress=progress)
            edit(message, f'`{get_translation("uploadFinish")}`')
        except Exception as e:
            edit(message, f'`{get_translation("uploadError")}`')
            raise e

        return

    edit(message, f'`{get_translation("uploadFileError")}`')


KOMUT.update({"download": get_translation("uploadInfo")})
