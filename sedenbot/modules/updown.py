# Copyright (C) 2020-2021 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os.path import isfile
from sedenbot import HELP
from sedenecem.core import (download_media_wc, sedenify, edit,
                            extract_args, reply_doc, get_translation)


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


HELP.update({'download': get_translation('uploadInfo')})
