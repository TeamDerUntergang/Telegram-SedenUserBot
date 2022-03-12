# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from datetime import datetime

from sedenbot import HELP
from sedenecem.core import edit, extract_args, get_translation, reply_img, sedenify

from speedtest import Speedtest


@sedenify(pattern='^.speedtest')
def speed_test(message):
    input_str = extract_args(message)
    as_text = False
    if input_str == 'text':
        as_text = True
    edit(message, f'`{get_translation("speedtest")}`')
    start = datetime.now()
    spdtst = Speedtest()
    spdtst.get_best_server()
    spdtst.download()
    spdtst.upload()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    response = spdtst.results.dict()
    download_speed = response.get('download')
    upload_speed = response.get('upload')
    ping_time = response.get('ping')
    client_infos = response.get('client')
    i_s_p = client_infos.get('isp')
    i_s_p_rating = client_infos.get('isprating')
    try:
        response = spdtst.results.share()
        speedtest_image = response
        if as_text:
            edit(
                message,
                get_translation(
                    'speedtestResultText',
                    [
                        '**',
                        ms,
                        convert_from_bytes(download_speed),
                        convert_from_bytes(upload_speed),
                        ping_time,
                        i_s_p,
                        i_s_p_rating,
                        '',
                    ],
                ),
            )
        else:
            reply_img(
                message,
                speedtest_image,
                caption=get_translation('speedtestResultDoc', ['**', ms]),
                delete_file=True,
                delete_orig=True,
            )
    except Exception as exc:
        edit(
            message,
            get_translation(
                'speedtestResultText',
                [
                    '**',
                    ms,
                    convert_from_bytes(download_speed),
                    convert_from_bytes(upload_speed),
                    ping_time,
                    i_s_p,
                    i_s_p_rating,
                    f'ERROR: {str(exc)}',
                ],
            ),
        )


def convert_from_bytes(size):
    power = 2 ** 10
    _ = 0
    units = {0: '', 1: 'kilobytes', 2: 'megabytes', 3: 'gigabytes', 4: 'terabytes'}
    while size > power:
        size /= power
        _ += 1
    return f'{round(size, 2)} {units[_]}'


HELP.update({'speedtest': get_translation('speedtestInfo')})
