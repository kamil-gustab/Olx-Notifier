# Olx Notifier
Follow ads for your chosen category on OLX.pl
## :book: Description
It is the python app - Web Scrapper for checking and saving list of active ads in chosen category.
## 🚀 Usage
Make sure you have installed:
* [alive_progress](https://pypi.org/project/alive_progress)
* [BeautifulSoup4](https://pypi.org/project/beautifulsoup4)
* [certifi](https://pypi.org/project/certifi)
* [lxml](https://pypi.org/project/lxml/)
* [telegram_send](https://pypi.org/project/telegram_send/)


Before run you need to complete passes file:

`passes.txt`

Data examples:

1. Recipient Email
2. Sender Email address
3. Sender Email app-password

![options.txt example screen](https://i.imgur.com/YR5KSeG.png)

---
After filling file just run the following command at the root of your project:
```
python scrapper.py
```
Or schedule it to run every X minutes on your machine using e.g. crontab like:
```
| every 10min   | your path to scrapper catalog | path to your python
*/10 * * * * cd /home/{your-user}/Olx-Notifier; /usr/bin/python3 main.py
```

## Author

👤 **Kamil Gustab**

- Github: [@gustab.kamil](https://gitlab.com/gustab.kamil)
