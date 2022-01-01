# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import path, remove

from PIL import Image
from removebg import RemoveBg
from sedenbot import HELP, RBG_APIKEY
from sedenecem.core import (
    download_media_wc,
    edit,
    get_download_dir,
    get_translation,
    reply_doc,
    sedenify,
)


@sedenify(pattern='^.rbg$')
def rbg(message):
    if not RBG_APIKEY:
        return edit(
            message,
            get_translation('rbgApiMissing', ['**', 'Remove.BG', '`']),
            preview=False,
        )
    reply = message.reply_to_message

    if (
        reply
        and reply.media
        and (
            reply.photo
            or (reply.sticker and not reply.sticker.is_animated)
            or (reply.document and 'image' in reply.document.mime_type)
        )
    ):
        edit(message, f'`{get_translation("processing")}`')
    else:
        edit(message, f'`{get_translation("rbgUsage")}`')
        return

    IMG_PATH = f'{get_download_dir()}/image.png'

    if path.exists(IMG_PATH):
        remove(IMG_PATH)
    download_media_wc(reply, IMG_PATH)
    edit(message, f'`{get_translation("rbgProcessing")}`')

    if reply.sticker and not reply.sticker.is_animated:
        image = Image.open(IMG_PATH)
        IMG_PATH = f'{get_download_dir()}/image.png'
        image.save(IMG_PATH)

    try:
        remove_bg = RemoveBg(RBG_APIKEY, get_translation('rbgLog'))
        remove_bg.remove_background_from_img_file(IMG_PATH)
        rbg_img = f'{IMG_PATH}_no_bg.png'
        reply_doc(
            reply, rbg_img, caption=get_translation('rbgResult'), delete_after_send=True
        )
        message.delete()
    except Exception as e:
        return edit(message, get_translation('banError', ['`', '**', e]))


HELP.update({'rbg': get_translation('rbgInfo')})
