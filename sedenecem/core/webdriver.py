# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from sedenbot import CHROME_DRIVER
from selenium.webdriver import Chrome, ChromeOptions


def get_webdriver():
    try:
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--window-size=1920x1080')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        prefs = {'download.default_directory': './'}
        options.add_experimental_option('prefs', prefs)
        return Chrome(executable_path=CHROME_DRIVER, options=options)
    except BaseException:
        raise Exception('CHROME_DRIVER not found!')
        return None
