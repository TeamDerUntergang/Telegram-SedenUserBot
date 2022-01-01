# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from json import loads

from requests import get
from sedenbot import HELP
from sedenecem.core import edit, extract_args, get_translation, sedenify


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

    edit(
        message,
        f'**{get_translation("gitUserInfo", [login])}**\n\n'
        + format_info(get_translation("gitUser"), user_id)
        + format_info(get_translation("gitAccount"), acc_type)
        + format_info(get_translation("gitName"), name)
        + format_info(get_translation("gitCompany"), company)
        + format_info(get_translation("gitWebsite"), blog)
        + format_info(get_translation("gitLocation"), location)
        + format_info(get_translation("gitMail"), email)
        + format_info(get_translation("gitBio"), bio)
        + format_info(get_translation("gitTwitter"), twitter)
        + format_info(get_translation("gitTotalRepo"), repo_count)
        + format_info(get_translation("gitTotalGist"), gist_count)
        + (
            (
                format_info(get_translation("gitFollowers"), followers)
                + format_info(get_translation("gitFollowing"), following)
            )
            if acc_type == 'User'
            else ''
        )
        + format_info(get_translation("gitCreationDate"), created)
        + format_info(get_translation("gitDateOfUpdate"), updated)
        + f'\n{get_translation("gitRepoList")}\n{get_repos()}',
        preview=False,
    )


HELP.update({'git': get_translation('gitInfo')})
