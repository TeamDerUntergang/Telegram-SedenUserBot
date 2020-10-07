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

from selenium.webdriver import Chrome, ChromeOptions
from sedenbot import CHROME_DRIVER


def get_webdriver():
    try:
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        prefs = {'download.default_directory': './'}
        options.add_experimental_option('prefs', prefs)
        return Chrome(executable_path=CHROME_DRIVER, options=options)
    except BaseException:
        raise Exception('CHROME_DRIVER not found!')
        return None
