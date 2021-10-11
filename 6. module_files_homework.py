# Module 6. Module. Files
# Expand previous Homework 5 with additional class, which allow to provide records by text file:
# 1.Define your input format (one or many records)
# 2.Default folder or user provided file path
# 3.Remove file if it was successfully processed
# 4.Apply case normalization functionality form Homework 3/4

from datetime import datetime
import sys
import re
import os
from functions_homework import normalize_text


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
        self.completed_message = f'{self.header}\n{normalize_text(self.text)}\n' \
                                 f'{self.city.capitalize()}, {self.publish_date}\n' \
                                 f'{self.footer}'


class PrivateAd(NewsFeedTool):
    def __init__(self):
        super().__init__()
        self.publish_date = self.publish_date()
        self.exp_date = self.expiration_date_validation()
        self.left_days = f'{(self.exp_date - self.publish_date).days + 1} days left'
        self.completed_message = f'{self.header}\n{normalize_text(self.text)}\n' \
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
        self.completed_message = f'{self.header}\n{normalize_text(self.text)}\n' \
                                 f'Item status: {self.item_status}, ' \
                                 f'Lost-and-found station number: {self.lost_and_found}\n{self.footer}'

    def item_status_validation(self):
        item_status = input("Enter the status of item (lost or found): ")
        while item_status.lower() not in ['lost', 'found']:
            print("The status of item can be LOST or FOUND only.")
            item_status = input("Enter the status of item (lost or found): ")
        return item_status


class TextProcessor:
    def __init__(self, default_folder=os.getcwd(), default_write_file='Newsfeed.txt'):
        self.rows_to_process = int(input('Enter how many records to process: '))
        self.default_folder = default_folder
        self.default_write_file = default_write_file
        self.file_to_process = input('Enter your file name to process like "Name.txt": ')

    def __get_rows_from_file(self):
        source_file_path = os.path.join(self.default_folder, self.file_to_process)
        with open(source_file_path, 'r') as file:
            file_all_content = file.read()
        list_of_records = re.split('\n\n', file_all_content)
        return list_of_records[0:self.rows_to_process]

    def write_from_file(self):
        with open(self.default_write_file, 'a') as file:
            for row in self.__get_rows_from_file():
                file.write(row + '\n\n')
        os.remove(os.path.join(self.default_folder, self.file_to_process))


def input_type_validation():
    input_type = int(input('Select input type:\n1 - Input\n2 - Get from file\n3 - Exit\n'))
    while input_type not in [1, 2, 3]:
        print("The options can be 1, 2, or 3 only.")
        input_type = int(input('Select input type:\n1 - Input\n2 - Get from file\n3 - Exit\n'))
    return input_type


while True:
    input_type = input_type_validation()
    if input_type == 1:
        input_message_type = input('Please enter the message type that you want to add on the feed '
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
    elif input_type == 2:
        folder_choose = int(input('Select folder path type to file location:\n1 - Default Folder\n'
                                  '2 - User folder\n'))
        if folder_choose == 2:
            user_folder = input('Enter the full path to folder like C:\\ : ')
            TextProcessor(default_folder=user_folder).write_from_file()
        else:
            TextProcessor().write_from_file()
    elif input_type == 3:
        sys.exit()
    else:
        print('Not implemented')
