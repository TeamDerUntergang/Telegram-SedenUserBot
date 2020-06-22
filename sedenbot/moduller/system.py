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

from os import execl, remove
from datetime import datetime
from pyrogram.api import functions
from shutil import which
from getpass import getuser
from sys import executable, argv
import operator as op
import ast

from sedenbot.moduller.lovers import saniye
from sedenbot.moduller.ecem import ecem
from sedenbot import KOMUT, ALIVE_MESAJI, BOT_VERSION, SUPPORT_GROUP
from sedenecem.events import edit, reply, reply_doc, send_log, extract_args, sedenify
# ================= CONSTANT =================
KULLANICIMESAJI = ALIVE_MESAJI
# ============================================
@sedenify(pattern='^.neofetch$')
def neofetch(message):
    try:
        from subprocess import PIPE, Popen
        islem = Popen(['neofetch','--stdout'], stdout=PIPE, stderr=PIPE)
        sonuc, _ = islem.communicate()
        edit(message, sonuc.decode(), parse=None)
    except:
        edit(message, '`Lütfen neofetch yükleyin.`')

@sedenify(pattern='^.botver$')
def botver(message):
    if which('git') :
        from subprocess import PIPE, Popen
        degisiklik = Popen(['git', 'rev-list', '--all', '--count'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
        sonuc, _ = degisiklik.communicate()

        edit(message, f'[Seden UserBot](https://telegram.dog/{SUPPORT_GROUP}) `Sürümü: '
                            f'v{BOT_VERSION}'
                            '` \n'
                            '`Toplam değişiklik (Commit): '
                            f'{sonuc}'
                            '`', preview=False, fix_markdown=True)
    else:
        edit(message,
            'Bu arada Seden seni çok seviyor. ❤️'
        )

@sedenify(pattern='^.pip')
def pip3(message):
    pipmodule = extract_args(message)
    if len(pipmodule) > 0:
        edit(message, '`Aranıyor...`')
        pipsorgu = f"pip3 search {pipmodule}"
        from subprocess import PIPE, Popen
        islem = Popen(pipsorgu.split(), stdout=PIPE, stderr=PIPE, universal_newlines=True)
        sonuc, _ = islem.communicate()

        if sonuc:
            if len(sonuc) > 4096:
                edit(message, '`Çıktı çok büyük, dosya olarak gönderiliyor.`')
                file = open('cikti.txt', 'w+')
                file.write(sonuc)
                file.close()
                reply_doc(message, 'cikti.txt')
                remove('cikti.txt')
                return
            edit(message, '**Sorgu: **\n`'
                          f'{pipsorgu}'
                          '`\n**Sonuç: **\n`'
                          f'{sonuc}'
                          '`', fix_markdown=True)
        else:
            edit(message, '**Sorgu: **\n`'
                          f'{pipsorgu}'
                          '`\n**Sonuç: **\n`Bir şey bulunamadı.`')
    else:
        edit(message, '`Bir örnek görmek için .seden pip komutunu kullanın.`')

@sedenify(pattern='^.(restart|yb)$', compat=False)
def restart(client, message):
    edit(message, '`Yeniden başlatılıyor ...`')
    send_log('#RESTART\n'
             'Bot yeniden başlatıldı.')
    try:
        client.terminate()
        client.disconnect()
    except:
        pass
    execl(executable, executable, *argv)

@sedenify(pattern='^.(shutdown|kapat)$', compat=False)
def restart(client, message):
    edit(message, '`Ben kapanıyorum, görüşürüz ...`')
    send_log('#SHUTDOWN \n'
             'Bot kapatıldı.')
    try:
        client.terminate()
        client.disconnect()
    except:
        pass
    execl(executable, 'killall', executable)

@sedenify(pattern='^.ping$')
def ping(message):
    basla = datetime.now()
    edit(message, '`Pong!`')
    bitir = datetime.now()
    sure = (bitir - basla).microseconds / 1000
    edit(message, f'`Pong!\n{sure}ms`')

@sedenify(pattern='^.alive$')
def alive(message):
    if KULLANICIMESAJI.lower() == 'ecem':
        ecem(message)
        return
    elif KULLANICIMESAJI.lower() == 'saniye':
        saniye(message)
        return
    edit(message, f'`{KULLANICIMESAJI}`')

@sedenify(pattern='^.alives')
def alives(message):
    alives = extract_args(message)
    sonuc = '`Kullanım: .alives <alive mesajı>`'
    if len(alives) > 0:
        global KULLANICIMESAJI
        KULLANICIMESAJI = alives
        sonuc = f'Alive mesajı, {KULLANICIMESAJI} olarak ayarlandı!'
    edit(message, '`' f'{sonuc}' '`')

@sedenify(pattern='^.resalive$')
def resalive(message):
    global KULLANICIMESAJI
    KULLANICIMESAJI = str(ALIVE_MESAJI) if ALIVE_MESAJI else kullanicireset().node
    edit(message, '`Alive mesajı başarıyla sıfırlandı!`')

@sedenify(pattern='^.echo')
def echo(message):
    args = extract_args(message)
    if len(args) > 0:
        message.delete()
        reply(message, args)
    else:
        edit(message, '`Argüman yazın`')

@sedenify(pattern='^.dc$', compat=False)
def dc(client, message):
    sonuc = client.send(functions.help.GetNearestDc())
    edit(message, f'**Ülke :** `{sonuc.country}`\n'
                  f'**En yakın veri merkezi :** `{sonuc.nearest_dc}`\n'
                  f'**Şu anki veri merkezi :** `{sonuc.this_dc}`')

# Copyright (c) @NaytSeyd, @frknkrc44 | 2020
@sedenify(pattern='^.term')
def terminal(message):
    command = extract_args(message)

    if len(command) < 1:
        edit(message, '`Lütfen bir komut yazın.`')
        return

    curruser = getuser()
    try:
        from os import geteuid
        uid = geteuid()
    except ImportError:
        uid = 'Bu değil şef!'

    if not command:
        edit(message, '`Yardım almak için .seden term yazarak örneğe bakabilirsin.`')
        return
    
    sonuc = 'Komutun sonucu alınamadı.'
    try:
        from subprocess import PIPE, Popen
        islem = Popen(command.split(), stdout=PIPE, stderr=PIPE, universal_newlines=True)
        sonuc, _ = islem.communicate()
    except:
        pass

    if len(sonuc) > 4096:
        output = open('cikti.txt', 'w+')
        output.write(sonuc)
        output.close()
        reply_doc(message, 'cikti.txt', caption='`Çıktı çok büyük, dosya olarak gönderiliyor`')
        remove('cikti.txt')
        return

    edit(message, f'`{curruser}:~{"#" if uid == 0 else "$"} {command}\n{sonuc}`', fix_markdown=True)

    send_log('Terminal Komutu ' + command + ' başarıyla yürütüldü')

@sedenify(pattern='^.eval')
def eval(message):
    args = extract_args(message)
    if len(args) < 1:
        edit(message, '`Değerlendirmek için bir ifade verin.`')
        return

    try:
        evaluation = safe_eval(args)
        if evaluation:
            if isinstance(evaluation, str):
                if len(evaluation) >= 4096:
                    file = open('cikti.txt', 'w+')
                    file.write(evaluation)
                    file.close()
                    reply_doc(message,
                        'cikti.txt',
                        caption='`Çıktı çok büyük, dosya olarak gönderiliyor`',
                    )
                    remove('cikti.txt')
                    return
                edit(message, '**Sorgu: **\n`'
                              f'{args}'
                              '`\n**Sonuç: **\n`'
                              f'{evaluation}'
                              '`')
        else:
            edit(message, '**Sorgu: **\n`'
                          f'{args}'
                          '`\n**Sonuç: **\n`Sonuç döndürülemedi / Yanlış`')
    except Exception as err:
        edit(message, '**Sorgu: **\n`'
                      f'{args}'
                      '`\n**İstisna: **\n'
                      f'`{err}`')

    send_log(f'Eval sorgusu {args} başarıyla yürütüldü')

operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
			ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
			ast.USub: op.neg}

def safe_eval(expr):
    expr = expr.lower().replace("x","*").replace(" ","")
    return str(_eval(ast.parse(expr, mode='eval').body))

def _eval(node):
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.BinOp):
        return operators[type(node.op)](_eval(node.left), _eval(node.right))
    elif isinstance(node, ast.UnaryOp):
        return operators[type(node.op)](_eval(node.operand))
    else:
        raise TypeError("Bu güvenli bir eval sorgusu olmayabilir.")

KOMUT.update(
    {"neofetch": ".neofetch\
    \nKullanım: Neofetch komutunu kullanarak sistem bilgisi gösterir."})
KOMUT.update({"botver": ".botver\
    \nKullanım: UserBot sürümünü gösterir."})
KOMUT.update(
    {"pip": ".pip <modül ismi>\
    \nKullanım: Pip modüllerinde arama yapar."})
KOMUT.update(
    {"dc": ".dc\
    \nKullanım: Sunucunuza en yakın veri merkezini gösterir."})
KOMUT.update(
    {"restart": ".restart\
\nKullanım: Botu yeniden başlatır."})
KOMUT.update(
    {"shutdown":".shutdown\
\nKullanım: Bazen canın botunu kapatmak ister. Gerçekten o nostaljik \
Windows XP kapanış sesini duyabileceğini zannedersin..."})
KOMUT.update(
    {"ping": ".ping\
    \nKullanım: Botun ping değerini gösterir."})
KOMUT.update(
    {"echo": ".echo\
    \nKullanım: Yazdığınız metni tekrar eder."})
KOMUT.update(
    {"eval": ".eval 2 + 3\
    \nKullanım: Mini ifadeleri değerlendirin."})
KOMUT.update(
    {"term": ".term\
    \nKullanım: Sunucunuzda bash komutlarını ve komut dosyalarını çalıştırın."})
KOMUT.update({
    "alive": ".alive\
    \nKullanım: Seden botunun çalışıp çalışmadığını kontrol etmek için kullanılır.\
    \n\n.alives <alive mesajı>\
    \nKullanım: Bu komut Seden botun alive mesajını değiştirmenize yarar.\
    \n\n.resalive\
    \nKullanım: Bu komut ayarladığınız alive mesajını varsayılan Seden olan haline döndürür."
})
