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

from requests import get
from json import loads
from sedenbot import KOMUT
from sedenecem.events import sedenify, edit, extract_args

# Copyright (c) @frknkrc44 | 2020
@sedenify(pattern='^.github')
def github(message):
    args = extract_args(message)
    
    if len(args) < 1:
        edit(message, '`Kullanım: .github <kullanıcı-adı>`')
        return

    try:
        user_info = get(f'https://api.github.com/users/{args}')
        json = loads(user_info.text)
    except:
        edit(message, '`Sanırım GitHub beni sevmiyor.`')
        return
        
    login = json.get('login', None)
    if not login:
        edit(message, '`Kullanıcı bulunamadı.`')
        return

    def return_defval_onnull(jsonkey, defval):
        ret = json.get(jsonkey, defval)
        if not ret or len(ret) < 1:
            return defval
        return ret

    user_id = json.get('id', -1)
    user_url = json.get('html_url', f'https://github.com/{args}')

    NULL_TEXT = 'Belirtilmemiş'

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
    except:
        pass
    
    def format_info(key, value):
        return f'**{key}:** `{value}`\n'
    
    def get_repos():
        if not repos or len(repos) < 1:
            return '`Depo bulunamadı.`'
        out = ''
        for i in repos:
            out += f'{i}\n'
        return out 
        
    edit(message, f'**{login} GitHub bilgileri**\n\n' +
                  format_info('Kullanıcı ID', user_id) +
                  format_info('Kullanıcı tipi', acc_type) +
                  format_info('Ad soyad', name) +
                  format_info('Şirket', company) +
                  format_info('Website', blog) +
                  format_info('Konum', location) +
                  format_info('E-posta', email) +
                  format_info('Biyografi', bio) +
                  format_info('Twitter', twitter) +
                  format_info('Toplam depo', repo_count) +
                  format_info('Toplam gist', gist_count) +
                  ((format_info('Takipçiler', followers) +
                  format_info('Takip edilen', following)) 
                  if acc_type == 'User' 
                  else '') +
                  format_info('Oluşturulma tarihi', created) +
                  format_info('Güncelleme tarihi', updated) +
                  f'\nDepolar:\n{get_repos()}', preview=False)
