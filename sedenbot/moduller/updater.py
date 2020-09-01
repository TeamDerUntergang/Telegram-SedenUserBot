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
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from sedenbot import KOMUT, HEROKU_KEY, HEROKU_APPNAME, REPO_URL
from sedenecem.core import extract_args, sedenify, edit, reply, reply_doc

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
    edit(ups, '`SedenBot için güncellemeler denetleniyor...`')
    conf = extract_args(ups)
    off_repo = REPO_URL
    force_update = False

    try:
        txt = '`Güncelleme başarısız oldu!'
        txt += 'Bazı sorunlarla karşılaştık.`\n\n**LOG:**\n'
        repo = Repo()
    except NoSuchPathError as error:
        edit(ups, f'{txt}\n`{error} klasörü bulunamadı.`')
        repo.__del__()
        return
    except GitCommandError as error:
        edit(ups, f'{txt}\n`Git hatası! {error}`')
        repo.__del__()
        return
    except InvalidGitRepositoryError as error:
        if conf != 'now':
            edit(ups,
                 f"`{error} klasörü bir git reposu gibi görünmüyor.\
                 \nFakat bu sorunu .update now komutuyla botu zorla güncelleyerek çözebilirsin.`")
            return
        repo = Repo.init()
        origin = repo.create_remote('upstream', off_repo)
        origin.fetch()
        force_update = True
        repo.create_head('master', origin.refs.seden)
        repo.heads.seden.set_tracking_branch(origin.refs.sql)
        repo.heads.seden.checkout(True)

    ac_br = repo.active_branch.name
    if ac_br != 'seden':
        edit(ups,
             f'**[SedenBot Güncelleyici]:**`Galiba botunun branch ismini değiştirdin. Kullandığın branch ismi: ({ac_br}). '
             'Böyle olursa botunu güncelleyemem. Çünkü branch ismi uyuşmuyor..'
             'Lütfen botunu SedenBot resmi repodan kullan.`')
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
        edit(ups,
             f'\n`Botun` **tamamen güncel!** `Branch:` **{ac_br}**\n')
        repo.__del__()
        return

    if conf != 'now' and not force_update:
        changelog_str = f'**{ac_br} için yeni güncelleme mevcut!\n\nDeğişiklikler:**\n`{changelog}`'
        if len(changelog_str) > 4096:
            edit(ups, '`Değişiklik listesi çok büyük, dosya olarak görüntülemelisin.`')
            file = open('degisiklikler.txt', 'w+')
            file.write(changelog_str)
            file.close()
            reply_doc(message, ups.chat.id, 'degisiklikler.txt')
            remove('degisiklikler.txt')
        else:
            edit(ups, changelog_str)
        reply(ups, '`Güncellemeyi yapmak için \".update now\" komutunu kullan.`')
        return

    if force_update:
        edit(ups, '`Güncel SedenBot kodu zorla eşitleniyor...`')
    else:
        edit(ups, '`Bot güncelleştiriliyor, lütfen bekle...`')
    if HEROKU_KEY:
        heroku = from_key(HEROKU_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not HEROKU_APPNAME:
            edit(ups, '`SedenBot Güncelleyiciyi kullanabilmek için HEROKU_APPNAME değişkenini tanımlamalısın. Aksi halde güncelleyici çalışmaz.`')
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APPNAME:
                heroku_app = app
                break
        if heroku_app is None:
            edit(ups,
                 f'{txt}\n`Heroku değişkenleri yanlış veya eksik tanımlanmış.`')
            repo.__del__()
            return
        edit(ups, '`SedenBot Güncelleniyor..\
             \nBu işlem 1-2 dakika sürebilir, lütfen sabırla bekle. Beklemene değer :)`')
        ups_rem.fetch(ac_br)
        repo.git.reset('--hard', 'FETCH_HEAD')
        heroku_git_url = heroku_app.git_url.replace('https://', 'https://api:' + HEROKU_KEY + '@')
        if 'heroku' in repo.remotes:
            remote = repo.remote('heroku')
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote('heroku', heroku_git_url)
        try:
            remote.push(refspec='HEAD:refs/heads/master', force=True)
        except GitCommandError as error:
            edit(ups, f'{txt}\n`Karşılaşılan hatalar burada:\n{error}`')
            repo.__del__()
            return
        edit(ups, '`Güncelleme başarıyla tamamlandı!\n'
             'SedenBot yeniden başlatılıyor, sabırla beklediğin için teşekkür ederiz :)`')
    else:
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset('--hard', 'FETCH_HEAD')
        update_requirements()
        edit(ups, '`Güncelleme başarıyla tamamlandı!\n'
             'SedenBot yeniden başlatılıyor, sabırla beklediğin için teşekkür ederiz :)`')

    try:
        app.terminate()
    except Exception:
        pass

    execl(executable, executable, *argv)


def execute_command(command):
    sonuc = None
    try:
        from subprocess import PIPE, Popen
        islem = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        sonuc, _ = islem.communicate()
    except: # pylint: disable=W0702
        pass
    return sonuc, islem.returncode


KOMUT.update({
    'update':
    ".update\
\nKullanım: Botunuza siz kurduktan sonra herhangi bir güncelleme gelip gelmediğini kontrol eder.\
\n\n.update now\
\nKullanım: Botunuzu günceller."
})
