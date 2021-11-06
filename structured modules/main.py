import sys
from Utils import input_type_validation, process_custom_folder
import CsvStatisticsCalculator
from NewsFeedTool import News, PrivateAd, LostAndFound
from FileProcessor import TextProcessor, JsonProcessor, XmlProcessor


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
            CsvStatisticsCalculator.CsvStatisticsCalculator('Newsfeed.txt').complete_stats()
        elif input_message_type.lower() == 'privatead':
            PrivateAd().write_to_file()
            CsvStatisticsCalculator.CsvStatisticsCalculator('Newsfeed.txt').complete_stats()
        elif input_message_type.lower() == 'lostandfound':
            LostAndFound().write_to_file()
            CsvStatisticsCalculator.CsvStatisticsCalculator('Newsfeed.txt').complete_stats()
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
        CsvStatisticsCalculator.CsvStatisticsCalculator('Newsfeed.txt').complete_stats()
    elif input_type == 3:
        sys.exit()
    else:
        print('Not implemented')
