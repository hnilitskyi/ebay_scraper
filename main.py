from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import json
import requests
import sys
import subprocess


class eBayScraper(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        try:
            with open('scrap.json', 'r', encoding='utf-8') as json_file:
                self.data = json.load(json_file)
        except FileNotFoundError:
            print('no data')

        self.setWindowTitle('eBay Scraper')
        self.setGeometry(100, 100, 400, 100)

        self.label_token = QLabel('Telegram Bot token:')

        self.token_input = QLineEdit(self)
        self.token_input.setPlaceholderText(self.data['token'])

        self.label_chat = QLabel('Telegram Chat ID for your Bot:')

        self.chatid_input = QLineEdit(self)
        self.chatid_input.setPlaceholderText(self.data['chatid'])

        self.label_url = QLabel('Link for your Ebay item:')

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText(self.data['link'])

        self.btn_start = QPushButton('Start', self)
        self.btn_start.clicked.connect(self.start_tracking)

        self.btn_stop = QPushButton('Stop', self)
        self.btn_stop.clicked.connect(QApplication.instance().quit)

        layout = QVBoxLayout()
        layout.addWidget(self.label_token)
        layout.addWidget(self.token_input)
        layout.addWidget(self.label_chat)
        layout.addWidget(self.chatid_input)
        layout.addWidget(self.label_url)
        layout.addWidget(self.url_input)
        layout.addWidget(self.btn_start)
        layout.addWidget(self.btn_stop)
        self.setLayout(layout)

        self.worker = Worker()

    def start_tracking(self):
        if len(self.url_input.text()) > 10:
            link_url = self.url_input.text()
        else:
            link_url = self.data['link']
        if len(self.token_input.text()) > 9:
            bot_token = self.token_input.text()
        else:
            bot_token = self.data['token']
        if len(self.chatid_input.text()) > 5:
            id_chat = self.chatid_input.text()
        else:
            id_chat = self.data['chatid']
        self.worker.start_tracking(link_url, bot_token, id_chat)


class Worker(QObject):
    started = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.tracking = False

    def start_tracking(self, link_url, bot_token, id_chat):
        self.tracking = True
        self.started.emit()
        self.thread = QThread()
        self.worker = ScrapWorker(link_url, self.tracking, bot_token, id_chat)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()


class ScrapWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, link_url, tracking, bot_token, id_chat):
        super().__init__()
        self.link_url = link_url
        self.bot_token = bot_token
        self.id_chat = id_chat
        self.tracking = tracking

    def run(self):
        ua = UserAgent()
        random_user_agent = ua.random

        headers = {
            'User-Agent': random_user_agent
        }

        while self.tracking:
            response = requests.get(self.link_url, headers=headers).text
            soup = BeautifulSoup(response, 'lxml')
            searching_prep = soup.find(class_='x-price-primary')
            if searching_prep is not None:
                searching = searching_prep.text
                currency = ""
                value_str = ""
                for char in searching:
                    if char.isdigit() or char == '.':
                        value_str += char
                    else:
                        currency += char

                value_current = float(value_str)
                try:
                    with open('scrap.json', 'r', encoding='utf-8') as json_file:
                        data_last = json.load(json_file)
                        value_last = float(data_last['value'])
                except FileNotFoundError:
                    print('no data')

                data = {
                    'token': self.bot_token,
                    'chatid': self.id_chat,
                    'link': self.link_url,
                    'value': str(value_current)
                }
                with open('scrap.json', 'w', encoding='utf-8') as json_file:
                    json.dump(data, json_file, ensure_ascii=False, indent=4)

                subprocess.run(["python", "bot_send.py", str(value_current), str(value_last)])
            else:
                print('bad request')
                continue

            time.sleep(600)

        self.finished.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = eBayScraper()
    window.show()
    sys.exit(app.exec_())
