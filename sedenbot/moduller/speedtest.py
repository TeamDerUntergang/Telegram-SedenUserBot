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

from datetime import datetime as DateTime
from speedtest import Speedtest

from sedenbot import KOMUT, SEDEN_LANG
from sedenecem.core import extract_args, sedenify, edit, reply_doc, get_translation


@sedenify(pattern='^.speedtest')
def speed_test(message):
    input_str = extract_args(message)
    as_text = False
    as_document = True
    if input_str == 'image':
        as_document = False
    elif input_str == 'file':
        as_document = True
    elif input_str == 'text':
        as_text = True
    edit(message, f'`{get_translation("speedtest")}`')
    start = DateTime.now()
    spdtst = Speedtest()
    spdtst.get_best_server()
    spdtst.download()
    spdtst.upload()
    end = DateTime.now()
    ms = (end - start).microseconds / 1000
    response = spdtst.results.dict()
    download_speed = response.get('download')
    upload_speed = response.get('upload')
    ping_time = response.get('ping')
    client_infos = response.get('client')
    i_s_p = client_infos.get('isp')
    i_s_p_rating = client_infos.get('isprating')
    reply_msg_id = message.chat.id
    if message.reply_to_message:
        reply_msg_id = message.reply_to_message
    try:
        response = spdtst.results.share()
        speedtest_image = response
        if as_text:
            edit(message,
                 get_translation('speedtestResultText',
                                 ['**',
                                  ms,
                                  convert_from_bytes(download_speed),
                                  convert_from_bytes(upload_speed),
                                  ping_time,
                                  i_s_p,
                                  i_s_p_rating,
                                  '']))
        else:
            reply_doc(
                message, speedtest_image, caption=get_translation(
                    'speedtestResultDoc', [
                        '**', ms]))
            message.delete()
    except Exception as exc:
        edit(message,
             get_translation('speedtestResultText',
                             ['**',
                              ms,
                              convert_from_bytes(download_speed),
                              convert_from_bytes(upload_speed),
                              ping_time,
                              i_s_p,
                              i_s_p_rating,
                              f'ERROR: {str(exc)}']))


def convert_from_bytes(size):
    power = 2**10
    _ = 0
    units = {
        0: '',
        1: 'kilobytes',
        2: 'megabytes',
        3: 'gigabytes',
        4: 'terabytes'
    }
    while size > power:
        size /= power
        _ += 1
    return f"{round(size, 2)} {units[_]}"


KOMUT.update({"speedtest": get_translation("speedtestInfo")})
