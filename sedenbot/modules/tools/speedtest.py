# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
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


def convert_bytes_to_human_readable(size_in_bytes):
    power = 1024
    size = size_in_bytes
    units = ['bytes', 'kilobytes', 'megabytes', 'gigabytes', 'terabytes']

    for unit in units:
        if size < power:
            return f'{size:.2f} {unit}'
        size /= power

    return f'{size:.2f} {units[-1]}'


@sedenify(pattern='^.speedtest')
def speed_test(message):
    as_text = extract_args(message) == 'text'
    edit(message, f'`{get_translation("speedtest")}`')
    start_time = datetime.now()
    spdtst = Speedtest()
    spdtst.get_best_server()
    spdtst.download()
    spdtst.upload()
    end_time = datetime.now()
    elapsed_seconds = int((end_time - start_time).total_seconds())

    results = spdtst.results.dict()
    download_speed = results['download']
    upload_speed = results['upload']
    ping_time = int(results['ping'])
    client_info = results['client']
    isp_name = client_info['isp']
    isp_rating = client_info['isprating']

    try:
        response = spdtst.results.share()
        speedtest_image = response
        if as_text:
            result_text = get_translation(
                'speedtestResultText',
                [
                    '**',
                    elapsed_seconds,
                    convert_bytes_to_human_readable(download_speed),
                    convert_bytes_to_human_readable(upload_speed),
                    ping_time,
                    isp_name,
                    isp_rating,
                    '',
                ],
            )
            edit(message, result_text)
        else:
            reply_img(
                message,
                speedtest_image,
                caption=get_translation('speedtestResultDoc', ['**', elapsed_seconds]),
                delete_file=True,
                delete_orig=True,
            )
    except Exception as exc:
        error_result_text = get_translation(
            'speedtestResultText',
            [
                '**',
                elapsed_seconds,
                convert_bytes_to_human_readable(download_speed),
                convert_bytes_to_human_readable(upload_speed),
                ping_time,
                isp_name,
                isp_rating,
                f'ERROR: {str(exc)}',
            ],
        )
        edit(message, error_result_text)


HELP.update({'speedtest': get_translation('speedtestInfo')})
