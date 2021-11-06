from DbConnector import DbConnector
from functions_homework import normalize_text
import re
from datetime import datetime


class NewsFeedTool:
    def __init__(self):
        self.text = input("Enter the message: ")
        self.completed_message = ''
        self._init_formatting_data()
        self._init_db_data()

    def _init_formatting_data(self):
        self.message_name = ' '.join(re.findall('[A-Z][^A-Z]*', self.__class__.__name__))
        self.header = self.create_message_header()
        self.footer = 30 * '-' + '\n\n'

    def _init_db_data(self):
        self.__connector = DbConnector('newsfeed.db')
        self.table_name = ''
        self.content_db = dict()
        self.params = dict()

    def create_message_header(self):
        return f"{self.message_name} {(30 - len(self.message_name) - 1) * '-'}"

    def publish_date(self):
        return datetime.today()

    def write_to_file(self):
        with open('Newsfeed.txt', 'a') as file:
            file.write(self.completed_message)
        self.__connector.process(self.table_name, self.params, self.content_db)


class News(NewsFeedTool):
    def __init__(self, text='', city='', publish_date=None, is_manual=1):
        if is_manual == 1:
            super().__init__()
            self.city = input("Enter the city name: ")
            self.publish_date = self.publish_date().strftime('%d-%m-%Y %H:%M')
        else:
            self.text = text
            self.city = city
            self.publish_date = publish_date
            super()._init_formatting_data()
            super()._init_db_data()
        self.completed_message = f'{self.header}\n{normalize_text(self.text)}\n' \
                                 f'{self.city.capitalize()}, {self.publish_date}\n' \
                                 f'{self.footer}'
        self.table_name = 'tblNews'
        self.content_db = {'Text': normalize_text(self.text), 'City': self.city.capitalize(),
                           'PublishDate': self.publish_date}
        self.params = {'Text': 'VARCHAR(250)', 'City': 'VARCHAR(100)', 'PublishDate': 'DATETIME'}


class PrivateAd(NewsFeedTool):
    def __init__(self, text='', exp_date=None, is_manual=1):
        if is_manual == 1:
            super().__init__()
            self.publish_date = self.publish_date()
            self.exp_date = self.expiration_date_validation()
        else:
            self.text = text
            self.exp_date = datetime.strptime(exp_date, '%d-%m-%Y')
            self.publish_date = self.publish_date()
            super()._init_formatting_data()
            super()._init_db_data()
        self.left_days = f'{(self.exp_date - self.publish_date).days + 1} days left'
        self.completed_message = f'{self.header}\n{normalize_text(self.text)}\n' \
                                 f'Actual until: {self.exp_date.date()}, ' \
                                 f'{self.left_days}\n{self.footer}'
        self.table_name = 'tblPrivateAd'
        self.content_db = {'Text': normalize_text(self.text), 'ExpirationDate': self.exp_date.date(),
                           'PublishDate': self.publish_date.strftime('%d-%m-%Y %H:%M')}
        self.params = {'Text': 'VARCHAR(250)', 'ExpirationDate': 'DATE', 'PublishDate': 'DATETIME'}

    def expiration_date_validation(self):
        exp_date = datetime.strptime(input("Enter the expiration date (dd-mm-yyyy): "), '%d-%m-%Y')
        while exp_date < self.publish_date:
            print("The expiration date can't be less than current date")
            exp_date = datetime.strptime(input("Enter the expiration date (dd-mm-yyyy): "), '%d-%m-%Y')
        return exp_date


class LostAndFound(NewsFeedTool):
    def __init__(self, text='', item_status='', lost_and_found='', is_manual=1):
        if is_manual == 1:
            super().__init__()
            self.item_status = self.item_status_validation()
            self.lost_and_found = input("Enter the lost-and-found station number: ")
        else:
            self.text = text
            self.item_status = item_status
            self.lost_and_found = lost_and_found
            super()._init_formatting_data()
            super()._init_db_data()
        self.completed_message = f'{self.header}\n{normalize_text(self.text)}\n' \
                                 f'Item status: {self.item_status}, ' \
                                 f'Lost-and-found station number: {self.lost_and_found}\n{self.footer}'
        self.table_name = 'tblLostFound'
        self.content_db = {'Text': normalize_text(self.text), 'ItemStatus': self.item_status,
                           'LostAndFoundStation': self.lost_and_found}
        self.params = {'Text': 'VARCHAR(250)', 'ItemStatus': 'VARCHAR(100)', 'LostAndFoundStation': 'INTEGER'}

    def item_status_validation(self):
        item_status = input("Enter the status of item (lost or found): ")
        while item_status.lower() not in ['lost', 'found']:
            print("The status of item can be LOST or FOUND only.")
            item_status = input("Enter the status of item (lost or found): ")
        return item_status
