# Calculate number of words and letters from previous Homeworks 5/6 output test file.
# Create two csv:
# 1.word-count (all words are preprocessed in lowercase)
# 2.letter, count_all, count_uppercase, percentage (add header, spacecharacters are not included)
# CSVs should be recreated each time new record added.
import re
import csv
import os


class CsvStatisticsCalculator:
    def __init__(self, file_to_process, folder_to_save=os.getcwd()):
        self.file_to_process = file_to_process
        self.folder_to_save = folder_to_save
        self.words_header = ['word', 'count_all']
        self.letters_header = ['letter', 'count_all', 'count_uppercase', 'percentage']
        self.words_csv_name = 'words_stats.csv'
        self.letters_csv_name = 'letters_stats.csv'

    def __extract_data_for_stats(self, pattern):
        return re.findall(pattern, open(self.file_to_process, 'r').read())

    def calculate_words_from_text(self):
        count_all_words = {}
        for word in self.__extract_data_for_stats(r'([A-Za-z]+)'):
            if word.lower() not in count_all_words.keys():
                count_all_words[word.lower()] = 1
            else:
                count_all_words[word.lower()] += 1
        return count_all_words

    def calculate_letters_from_text(self):
        letters = self.__extract_data_for_stats(r'[A-Za-z]')
        count_all_letters = {}
        count_uppercase = {}
        for letter in letters:
            if letter.lower() not in count_all_letters.keys():
                count_all_letters[letter.lower()] = 1
                if letter.isupper():
                    count_uppercase[letter.lower()] = 1
            else:
                count_all_letters[letter.lower()] += 1
                if letter.isupper() and letter.lower() not in count_uppercase.keys():
                    count_uppercase[letter.lower()] = 1
                elif letter.isupper():
                    count_uppercase[letter.lower()] += 1
        for key, values in count_all_letters.items():
            if key in count_uppercase:
                count_all_letters[key] = [values, count_uppercase[key], round(values / len(letters) * 100, 2)]
            else:
                count_all_letters[key] = [values, 0, round(values / len(letters) * 100, 2)]
        return count_all_letters

    def prepare_words_stats(self):
        with open(self.words_csv_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.words_header)
            all_words_stats = self.calculate_words_from_text()
            for key in all_words_stats.keys():
                writer.writerow([key, all_words_stats[key]])

    def prepare_letters_stats(self):
        with open(self.letters_csv_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.letters_header)
            all_letters_stats = self.calculate_letters_from_text()
            for key in all_letters_stats.keys():
                prep_row = all_letters_stats[key]
                prep_row.insert(0, key)
                writer.writerow(prep_row)

    def complete_stats(self):
        self.prepare_words_stats()
        self.prepare_letters_stats()
