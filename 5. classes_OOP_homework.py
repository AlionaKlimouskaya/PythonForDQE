# Create a tool, which will do user generated news feed:
# 1.User select what data type he wants to add
# 2.Provide record type required data
# 3.Record is published on text file in special format
#
# You need to implement:
# 1.News – text and city as input. Date is calculated during publishing.
# 2.Privat ad – text and expiration date as input. Day left is calculated during publishing.
# 3.Your unique one with unique publish rules.

from datetime import datetime
import sys
import re

class NewsFeedTool:
    def __init__(self):
        self.text = input("Enter the message: ")
        self.completed_message = ''
        self.message_name = ' '.join(re.findall('[A-Z][^A-Z]*', self.__class__.__name__))
        self.header = self.create_message_header()
        self.footer = 30 * '-' + '\n\n'

    def create_message_header(self):
        return f"{self.message_name} {(30 - len(self.message_name) - 1) * '-'}"

    def publish_date(self):
        return datetime.today()

    def write_to_file(self):
        with open('Newsfeed.txt', 'a') as file:
            file.write(self.completed_message)


class News(NewsFeedTool):
    def __init__(self):
        super().__init__()
        self.city = input("Enter the city name: ")
        self.publish_date = self.publish_date().strftime('%d-%m-%Y %H:%M')
        self.completed_message = f'{self.header}\n{self.text.capitalize()}\n' \
                                 f'{self.city.capitalize()}, {self.publish_date}\n' \
                                 f'{self.footer}'


class PrivateAd(NewsFeedTool):
    def __init__(self):
        super().__init__()
        self.publish_date = self.publish_date()
        self.exp_date = self.expiration_date_validation()
        self.left_days = f'{(self.exp_date - self.publish_date).days + 1} days left'
        self.completed_message = f'{self.header}\n{self.text.capitalize()}\n' \
                                 f'Actual until: {self.exp_date.date()}, ' \
                                 f'{self.left_days}\n{self.footer}'

    def expiration_date_validation(self):
        exp_date = datetime.strptime(input("Enter the expiration date (dd-mm-yyyy): "), '%d-%m-%Y')
        while exp_date < self.publish_date:
            print("The expiration date can't be less than current date")
            exp_date = datetime.strptime(input("Enter the expiration date (dd-mm-yyyy): "), '%d-%m-%Y')
        return exp_date


class LostAndFound(NewsFeedTool):
    def __init__(self):
        super().__init__()
        self.item_status = self.item_status_validation()
        self.lost_and_found = input("Enter the lost-and-found station number: ")
        self.completed_message = f'{self.header}\n{self.text.capitalize()}\n' \
                                 f'Item status: {self.item_status}, ' \
                                 f'Lost-and-found station number: {self.lost_and_found}\n{self.footer}'

    def item_status_validation(self):
        item_status = input("Enter the status of item (lost or found): ")
        while item_status.lower() not in ['lost', 'found']:
            print("The status of item can be LOST or FOUND only.")
            item_status = input("Enter the status of item (lost or found): ")
        return item_status


while True:
    input_message_type = input('Please enter the message type that you want to add on the feed'
                               'or enter "exit" to close the program. '
                               'Available message types: News, PrivateAd, LostAndFound: ')
    if input_message_type.lower() == 'exit':
        sys.exit()
    elif input_message_type.lower() == 'news':
        News().write_to_file()
    elif input_message_type.lower() == 'privatead':
        PrivateAd().write_to_file()
    elif input_message_type.lower() == 'lostandfound':
        LostAndFound().write_to_file()
    else:
        print('Not implemented')
