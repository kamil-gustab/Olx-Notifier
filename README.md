# :bell: Olx Notifier
Follow ads for your chosen category on OLX.pl
## :book: Description
It is the python app - Web Scraper for checking and saving list of active ads in chosen category.
## 🚀 Usage
Make sure you have installed:
* [alive_progress](https://pypi.org/project/alive_progress)
* [BeautifulSoup4](https://pypi.org/project/beautifulsoup4)
* [certifi](https://pypi.org/project/certifi)
* [lxml](https://pypi.org/project/lxml/)
* [telegram_send](https://pypi.org/project/telegram_send/)

### Notifying

You can choose between two options of notifying
- By telegram message (preferred option)
- By e-mail
---
### a) Notifying by telegram message
To do so you first need to configure your `telegram_send` package.

To do so:
1) First create your new telegram bot by writing on telegram to the `BotFather` on telegram, and create new bot by using command `/newbot`.
2) After filling all needed data you will be given you HTTP API token for your bot.
3) In CLI use command `telegram-send configure` - paste your token there, then add your freshly created bot on telegram and send him your activation password (code).
4) Voi'la - you can simply use your bot!

---
### b) Notifying by mail

For best experience you should use gmail along with per-app-password for your script.
More about App Password for gmail - [here](https://support.google.com/accounts/answer/185833)

You should fill file named:

`passes.txt`

Data examples:

1. Recipient Email
2. Sender Email address
3. Sender Email app-password

![options.txt example screen](https://i.imgur.com/YR5KSeG.png)

---
### Run

To start - just run the following command at the root of your project like e.g.:
```
python3 main.py --url <your-url> --notify telegram
python3 main.py --url <your-url> --notify mail
python3 main.py --notify no-notify
```
Or schedule it to run every X minutes on your machine, by using e.g. crontab like:
```
| every 10min   | your path to scrapper catalog | path to your python    | parameters
*/10 * * * * cd /home/{your-user}/Olx-Notifier; /usr/bin/python3 main.py --notify telegram
```

## Author

👤 **Kamil Gustab**

- Github: [@gustab.kamil](https://github.com/kamil-gustab)
