# Module 4. Functions
# Refactor homeworks from module 2 and 3 using functional approach with decomposition.

import string
import random
import re

# Variable to module 3 homework
start_text = """homEwork:
	tHis iz your homeWork, copy these Text to variable. 

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE. 

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""


# Module 2 homework using the functional approach with decomposition.
def generate_dicts(amount):
    if amount < 2 or amount > 10:
        print("The number of dictionaries can't be less than 2 or more than 10")
        return None
    return [{ele: random.randint(0, 100)
               for ele in random.sample(string.ascii_lowercase, random.randint(1, 26))}
               for i in range(random.randint(1, amount))]


def sort_dictionaries(dictionaries):
    dictionaries_keys = []
    for dictionary in dictionaries:
          dictionaries_keys.extend(dictionary.keys())
    common_dict = {}
    for dict_number, dictionary in enumerate(dictionaries):
        for key in dictionary:
            if key not in [letter[0] for letter in common_dict.keys()]:
                if dictionaries_keys.count(key) == 1:
                    common_dict[key] = dictionary[key]
                else:
                    common_dict[f'{key}_{dict_number + 1}'] = dictionary[key]
            elif common_dict[[unique_key for unique_key in common_dict.keys()
                              if key in unique_key][0]] < dictionary[key]:
                common_dict[f'{key}_{dict_number + 1}'] = dictionary[key]
                del common_dict[[unique_key for unique_key in common_dict.keys() if key in unique_key][0]]
    return common_dict


# Module 3 homework using the functional approach with decomposition.
def fix_misspelling_in_text(text, incorrect_word, correct_word):
    return text.replace(incorrect_word, correct_word)


def normalize_text(text):
    list_of_text = re.split(r'(^|[.]\s|\n\t)', text)
    normalized_text = ''
    for i in list_of_text:
        normalized_text += i.capitalize()
    return ''.join(normalized_text)


def create_sentence_with_last_words_of_each_sentence(text):
    sentences = [sentence for sentence in normalize_text(text).split('.') if sentence]
    last_sentence = []
    for sentence in sentences:
        last_sentence.append(sentence.split()[-1])
    return ', '.join(last_sentence) + '.'


def add_sentence_to_text(text, sentence):
    return text + '\n\n\t' + sentence.capitalize()


def whitespace_characters(text):
    return len(re.findall(r'\s', text))


# the result of Module 2
dictionaries_list = generate_dicts(10)
print("Result of Module 2")
print("List of dictionaries: ", dictionaries_list)
print("Common list of dictionaries: ", sort_dictionaries(dictionaries_list))

# the result of Module 3
count_of_whitespaces = whitespace_characters(start_text)

text_without_misspelling = fix_misspelling_in_text(start_text.lower(), ' iz ', ' is ')

formatted_text = normalize_text(text_without_misspelling)

completed_text = add_sentence_to_text(formatted_text,
                                      create_sentence_with_last_words_of_each_sentence(formatted_text))
print('\n' + "Result of Module 3")
print(completed_text)
print('\n\t' + f"Number of whitespace characters: {count_of_whitespaces}")
