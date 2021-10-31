# Module 10. Database API
# Expand previous Homework 5/6/7/8/9 with additional class, which allow to save records into database:
# 1.Different types of records require different data tables
# 2.New record creates new row in data table
# 3.Implement “no duplicate” check.

from datetime import datetime
import sys
import re
import os
import json
from functions_homework import normalize_text
import CSV_Parsing_homework
import xml.etree.ElementTree as ElementTree
import sqlite3


class DbConnector:
    def __init__(self, database_url):
        self.database_url = database_url
        self.connection = sqlite3.connect(self.database_url)
        self.cursor = self.connection.cursor()

    def is_table_exists(self, table_name):
        query = f"SELECT count(1) FROM pragma_table_info('{table_name}');"
        self.cursor.execute(query)
        return int(self.cursor.fetchone()[0]) > 0

    def create_table(self, table_name, table_parameters):
        parameters = ',\n'.join([f'{key} {value}' for key, value in table_parameters.items()])
        query = f"""CREATE TABLE {table_name}
        (msg_id INTEGER PRIMARY KEY AUTOINCREMENT,
        {parameters});"""
        self.cursor.execute(query)
        print(f'Table {table_name} was created.')

    def insert_row(self, table_name, datadict):
        columns = [key for key in datadict.keys()]
        values = [f"'{datadict[col]}'" for col in columns]
        query = f"INSERT INTO {table_name}({', '.join(columns)}) values ({', '.join(values)});"
        self.cursor.execute(query)
        self.connection.commit()

    def is_duplicate(self, table_name, datadict):
        params = ' AND '.join([f"{key} = '{datadict[key]}'" for key in datadict.keys() if 'PublishDate' not in key])
        query = f"SELECT COUNT(*) FROM {table_name} WHERE {params};"
        self.cursor.execute(query)
        return int(self.cursor.fetchone()[0]) > 0

    def ddl_schema_table(self, table_name, table_parameters):
        check_table = self.is_table_exists(table_name)
        if not check_table:
            self.create_table(table_name, table_parameters)

    def process(self, table_name, table_parameters, datadict):
        self.ddl_schema_table(table_name, table_parameters)
        if not self.is_duplicate(table_name, datadict):
            self.insert_row(table_name, datadict)
            print(f'Row was inserted into table {table_name} in database.')
        else:
            print(f'DUPLICATE. Row was NOT INSERTED into database table {table_name}.')


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


class FileProcessor:
    def __init__(self, default_folder=os.getcwd(), default_write_file='Newsfeed.txt'):
        self.rows_to_process = int(input('Enter how many records to process: '))
        self.default_folder = default_folder
        self.default_write_file = default_write_file
        self.file_to_process = input('Enter your file name to process like "FileName.FileFormat": ')


class JsonProcessor(FileProcessor):
    def __init__(self, default_folder=None):
        if default_folder:
            super().__init__(default_folder)
        else:
            super().__init__()

    def __get_rows_from_file(self):
        json_data = {}
        source_file_path = os.path.join(self.default_folder, self.file_to_process)
        with open(source_file_path, 'r') as json_file:
            raw_json_data = json.load(json_file)
        counter = self.rows_to_process
        for key, value in raw_json_data.items():
            json_data.update({key: value})
            counter -= 1
            if counter == 0:
                break
        return json_data

    def write_from_file(self):
        json_to_process = self.__get_rows_from_file()
        for newsfeed in json_to_process.values():
            if newsfeed['msg_type'] == 'news':
                News(newsfeed['text'], newsfeed['city'], newsfeed['publish_date'], is_manual=0).write_to_file()
            elif newsfeed['msg_type'] == 'privatead':
                PrivateAd(newsfeed['text'], newsfeed['exp_date'], is_manual=0).write_to_file()
            elif newsfeed['msg_type'] == 'lostandfound':
                LostAndFound(newsfeed['text'], newsfeed['item_status'], newsfeed['lost_and_found'],
                             is_manual=0).write_to_file()
            else:
                print('Message type not implemented in the application')
        os.remove(os.path.join(self.default_folder, self.file_to_process))


class XmlProcessor(FileProcessor):
    def __init__(self, default_folder=None):
        if default_folder:
            super().__init__(default_folder)
        else:
            super().__init__()

    def __get_rows_from_file(self):
        xml_file = ElementTree.parse(os.path.join(self.default_folder, self.file_to_process))
        xml_root = xml_file.getroot()
        messages_in_xml = []
        counter = self.rows_to_process
        for elements in xml_root:
            temp_dict = {}
            for tag in elements:
                temp_dict[tag.tag] = tag.text
            messages_in_xml.append(temp_dict)
            counter -= 1
            if counter == 0:
                break
        return messages_in_xml

    def write_from_file(self):
        xml_to_process = self.__get_rows_from_file()
        for newsfeed in xml_to_process:
            if newsfeed['msg_type'] == 'news':
                News(newsfeed['text'], newsfeed['city'], newsfeed['publish_date'], is_manual=0).write_to_file()
            elif newsfeed['msg_type'] == 'privatead':
                PrivateAd(newsfeed['text'], newsfeed['exp_date'], is_manual=0).write_to_file()
            elif newsfeed['msg_type'] == 'lostandfound':
                LostAndFound(newsfeed['text'], newsfeed['item_status'], newsfeed['lost_and_found'],
                             is_manual=0).write_to_file()
            else:
                print('Message type not implemented in the application')
        os.remove(os.path.join(self.default_folder, self.file_to_process))


class TextProcessor(FileProcessor):
    def __init__(self, default_folder=None):
        if default_folder:
            super().__init__(default_folder)
        else:
            super().__init__()

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
    raw_input_type = int(input('Select input type:\n1 - Input\n2 - Get from file\n3 - Exit\n'))
    while raw_input_type not in [1, 2, 3]:
        print("The options can be 1, 2, or 3 only.")
        raw_input_type = int(input('Select input type:\n1 - Input\n2 - Get from file\n3 - Exit\n'))
    return raw_input_type


def process_custom_folder(folder_type_choice, processor_type):
    if folder_type_choice == 2:
        user_folder = input('Enter the full path to folder like C:\\ : ')
        processor_type(default_folder=user_folder).write_from_file()
    elif folder_type_choice == 1:
        processor_type().write_from_file()
    else:
        print('Not implemented')


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
            CSV_Parsing_homework.CsvStatisticsCalculator('Newsfeed.txt').complete_stats()
        elif input_message_type.lower() == 'privatead':
            PrivateAd().write_to_file()
            CSV_Parsing_homework.CsvStatisticsCalculator('Newsfeed.txt').complete_stats()
        elif input_message_type.lower() == 'lostandfound':
            LostAndFound().write_to_file()
            CSV_Parsing_homework.CsvStatisticsCalculator('Newsfeed.txt').complete_stats()
        else:
            print('Not implemented')
    elif input_type == 2:
        processor_choose = int(input('Please select which type of the file you want to process:'
                                     '\n1 - Txt File\n2 - Json file\n3 - XML file\n'))
        folder_choose = int(input('Select folder path type to file location:\n1 - Default Folder\n'
                                  '2 - User folder\n'))
        if processor_choose == 1:
            process_custom_folder(folder_choose, TextProcessor)
        elif processor_choose == 2:
            process_custom_folder(folder_choose, JsonProcessor)
        elif processor_choose == 3:
            process_custom_folder(folder_choose, XmlProcessor)
        CSV_Parsing_homework.CsvStatisticsCalculator('Newsfeed.txt').complete_stats()
    elif input_type == 3:
        sys.exit()
    else:
        print('Not implemented')
