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

from os import remove, execl, path
from sys import executable, argv
from heroku3 import from_key
from git import Repo
from git.exc import (GitCommandError, InvalidGitRepositoryError,
                     NoSuchPathError)

from sedenbot import KOMUT, HEROKU_KEY, HEROKU_APPNAME, REPO_URL
from sedenecem.core import (extract_args, sedenify, edit, reply,
                            reply_doc, get_translation, app)

requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), 'requirements.txt')


def gen_chlog(repo, diff):
    ch_log = ''
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += f'•[{c.committed_datetime.strftime(d_form)}]: {c.summary} <{c.author}>\n'
    return ch_log


def update_requirements():
    reqs = str(requirements_path)
    try:
        _, ret = execute_command(f'{executable} -m pip install -r {reqs}')
        return ret
    except Exception as e:
        return repr(e)


@sedenify(pattern=r'^.update(?: |$)(.*)')
def upstream(ups):
    edit(ups, f'`{get_translation("updateCheck")}`')
    conf = extract_args(ups)
    off_repo = REPO_URL
    force_update = False

    try:
        txt = f'`{get_translation("updateFailed")}`\n\n'
        txt += f'**{get_translation("updateLog")}**\n'
        repo = Repo()
    except NoSuchPathError as error:
        edit(ups, get_translation("updateFolderError", [txt, '`', error]))
        repo.__del__()
        return
    except GitCommandError as error:
        edit(ups, get_translation("updateFolderError", [txt, '`', error]))
        repo.__del__()
        return
    except InvalidGitRepositoryError as error:
        if conf != 'now':
            edit(ups, f'`{get_translation("updateGitNotFound", [error])}`')
            return
        repo = Repo.init()
        origin = repo.create_remote('upstream', off_repo)
        origin.fetch()
        force_update = True
        repo.create_head('seden', origin.refs.seden)
        repo.heads.seden.set_tracking_branch(origin.refs.seden)
        repo.heads.seden.checkout(True)

    ac_br = repo.active_branch.name
    if ac_br != 'seden':
        edit(ups, get_translation("updateFolderError", ['**', ac_br]))
        repo.__del__()
        return

    try:
        repo.create_remote('upstream', off_repo)
    except BaseException:
        pass

    ups_rem = repo.remote('upstream')
    ups_rem.fetch(ac_br)

    changelog = gen_chlog(repo, f'HEAD..upstream/{ac_br}')

    if not changelog and not force_update:
        edit(ups, get_translation('updaterUsingLatest', ['**', '`', ac_br]))
        repo.__del__()
        return

    if conf != 'now' and not force_update:
        if len(changelog) > 4096:
            edit(ups, f'`{get_translation("updateOutput")}`')
            file = open('changelog.txt', 'w+')
            file.write(changelog)
            file.close()
            reply_doc(message, ups.chat.id, 'changelog.txt')
            remove('changelog.txt')
        else:
            edit(ups, get_translation(
                'updaterHasUpdate', ['**', '`', ac_br, changelog]))
        reply(ups, f'`{get_translation("updateNow")}`')
        return

    if force_update:
        edit(ups, f'`{get_translation("updateForceSync")}`')
    else:
        edit(ups, f'`{get_translation("updateSedenBot")}`')

    if HEROKU_KEY:
        heroku = from_key(HEROKU_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not HEROKU_APPNAME:
            edit(ups, f'`{get_translation("updateHerokuAppName")}`')
            me[1] = False
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APPNAME:
                heroku_app = app
                break
        if heroku_app is None:
            edit(ups, f'`{get_translation("updateHerokuAppName", [txt])}`')
            me[1] = False
            repo.__del__()
            return
        edit(ups, f'`{get_translation("updateBotUpdating")}`')
        ups_rem.fetch(ac_br)
        repo.git.reset('--hard', 'FETCH_HEAD')
        heroku_git_url = heroku_app.git_url.replace(
            'https://', 'https://api:' + HEROKU_KEY + '@')
        if 'heroku' in repo.remotes:
            remote = repo.remote('heroku')
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote('heroku', heroku_git_url)
        try:
            remote.push(refspec='HEAD:refs/heads/master', force=True)
        except GitCommandError as error:
            edit(ups, get_translation('updaterGitError', ['`', txt, error]))
            repo.__del__()
            return
        edit(ups, f'`{get_translation("updateComplete")}`')
    else:
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset('--hard', 'FETCH_HEAD')
        update_requirements()
        edit(ups, f'`{get_translation("updateLocalComplate")}`')

    try:
        app.terminate()
    except Exception:
        pass

    execl(executable, executable, *argv)


def execute_command(command):
    sonuc = None
    try:
        from subprocess import PIPE, Popen
        islem = Popen(command, stdout=PIPE, stderr=PIPE,
                      universal_newlines=True)
        sonuc, _ = islem.communicate()
    except BaseException:
        pass
    return sonuc, islem.returncode


KOMUT.update({'update': get_translation("updateInfo")})
