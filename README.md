Seden UserBot
==

![GitHub repo size](https://img.shields.io/github/repo-size/TeamDerUntergang/Telegram-SedenUserBot?color=brightgreen)
![GitHub](https://img.shields.io/github/license/TeamDerUntergang/Telegram-SedenUserBot?color=red)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Telegram Python Bot running on Python3 with a Postgresql Sqlalchemy database. It is an modular and simple to use bot.

```c
#include <std/disclaimer.h>
/**
    Your Telegram account may be banned.
    I'm not responsible for misuse of bot, responsibility belongs entirely to user.
    This bot is maintained for fun as well as managing groups efficiently.
    If you think you will have fun by spamming groups, you are wrong.
    In case of any spam ban, if you come and write that my account has been banned,
    I'll just laugh at you.
/**
```
## Run Bot
```bash
# Clone repo
git clone https://github.com/TeamDerUntergang/Telegram-SedenUserBot.git
cd Telegram-SedenUserBot

# Install pip dependencies
pip3 install -r requirements.txt

# Generate session from session.py (skip if there is already)
python3 session.py

# Create config.env and fill variables
mv sample_config.env config.env

# Run bot
python3 seden.py
```
### Nix/NixOS
Just type `nix-shell` command in bot folder.

## Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/TeamDerUntergang/Telegram-SedenUserBot/tree/seden)

If you have any requests & complaints & suggestions, you can join our [support group](https://t.me/SedenUserBotSupport) or please contact us through a [GitHub issue](https://github.com/TeamDerUntergang/Telegram-SedenUserBot/issues).

Please go to our [GitHub.io](https://teamderuntergang.github.io/installation.html) page for installation instructions! Questions asked without reading the instruction will not be answered.

## Credits
*   [@NaytSeyd](https://github.com/NaytSeyd) - Founder
*   [@frknkrc44](https://github.com/frknkrc44) - Operator
*   [@Sedenogen](https://github.com/ciyanogen) - Co-Founder
*   [@Delivrance](https://github.com/pyrogram/pyrogram) - Pyrogram Library
*   [@Skittles9823](https://github.com/skittles9823) - Memes
*   [@RaphielGang](https://github.com/raphielgang) - Other Modules
*   [All Contributors](https://github.com/TeamDerUntergang/Telegram-SedenUserBot/graphs/contributors)

## License

This project is licensed under the [AGPL-3](https://www.gnu.org/licenses/agpl-3.0.html).
