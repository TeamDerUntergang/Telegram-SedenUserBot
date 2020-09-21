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

from json import loads
from requests import get

from sedenbot import KOMUT
from sedenecem.core import sedenify, edit, extract_args, get_translation

# Copyright (c) @frknkrc44 | 2020


@sedenify(pattern='^.github')
def github(message):
    args = extract_args(message)

    if len(args) < 1:
        edit(message, f'`{get_translation("gitUsage")}`')
        return

    try:
        user_info = get(f'https://api.github.com/users/{args}')
        json = loads(user_info.text)
    except BaseException:
        edit(message, f'`{get_translation("gitError")}`')
        return

    login = json.get('login', None)
    if not login:
        edit(message, f'`{get_translation("gitUserNotFound")}`')
        return

    def return_defval_onnull(jsonkey, defval):
        ret = json.get(jsonkey, defval)
        if not ret or len(ret) < 1:
            return defval
        return ret

    user_id = json.get('id', -1)
    user_url = json.get('html_url', f'https://github.com/{args}')

    NULL_TEXT = f'{get_translation("gitNull")}'

    name = return_defval_onnull('name', NULL_TEXT)
    acc_type = return_defval_onnull('type', 'User')
    company = return_defval_onnull('company', NULL_TEXT)
    blog = return_defval_onnull('blog', NULL_TEXT)
    location = return_defval_onnull('location', NULL_TEXT)
    email = return_defval_onnull('email', NULL_TEXT)
    bio = return_defval_onnull('bio', NULL_TEXT)
    twitter = return_defval_onnull('twitter_username', NULL_TEXT)
    repo_count = json.get('public_repos', 0)
    gist_count = json.get('public_gists', 0)
    followers = json.get('followers', 0)
    following = json.get('following', 0)
    created = json.get('created_at', NULL_TEXT)
    updated = json.get('updated_at', NULL_TEXT)

    repos = None

    try:
        repo_info = get(f'https://api.github.com/users/{args}/repos')
        json = loads(repo_info.text)
        repos = []
        for item in json:
            repos.append(f'[{item["name"]}]({item["html_url"]})')
    except BaseException:
        pass

    def format_info(key, value):
        return f'**{key}:** `{value}`\n'

    def get_repos():
        if not repos or len(repos) < 1:
            return f'`{get_translation("gitRepo")}`'
        out = ''
        for i in repos:
            out += f'{i}\n'
        return out

    edit(message, f'**{get_translation("gitUserInfo", [login])}**\n\n' +
                  format_info(get_translation("gitUser"), user_id) +
                  format_info(get_translation("gitAccount"), acc_type) +
                  format_info(get_translation("gitName"), name) +
                  format_info(get_translation("gitCompany"), company) +
                  format_info(get_translation("gitWebsite"), blog) +
                  format_info(get_translation("gitLocation"), location) +
                  format_info(get_translation("gitMail"), email) +
                  format_info(get_translation("gitBio"), bio) +
                  format_info(get_translation("gitTwitter"), twitter) +
                  format_info(get_translation("gitTotalRepo"), repo_count) +
                  format_info(get_translation("gitTotalGist"), gist_count) +
                  ((format_info(get_translation("gitFollowers"), followers) +
                    format_info(get_translation("gitFollowing"), following))
                   if acc_type == 'User'
                   else '') +
                  format_info(get_translation("gitCreationDate"), created) +
                  format_info(get_translation("gitDateOfUpdate"), updated) +
                  f'\n{get_translation("gitRepoList")}\n{get_repos()}', preview=False)


KOMUT.update({"git": get_translation("gitInfo")})
