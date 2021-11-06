import os
import json
import re
from NewsFeedTool import News, PrivateAd, LostAndFound
import xml.etree.ElementTree as ElementTree


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
