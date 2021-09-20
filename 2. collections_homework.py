# Module 2. Collections

# Task 1. Create a list of random number of dicts (from 2 to 10)
# dict's random numbers of keys should be letter,
# dict's values should be a number (0-100),
# example: [{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]
import string
import random

# initialize list of keys
# assign random elements
# create a random number of dictionaries
list_result = [{ele: random.randint(0, 100)
               for ele in random.sample(string.ascii_lowercase, random.randint(1, 26))}
               for i in range(random.randint(2, 10))]

# printing result
print("Task 1. List of random number of dictionaries: " + str(list_result))

# Task 2. Get previously generated list of dicts and create one common dict:
# if dicts have same key, we will take max value, and rename key with dict number with max value
# if key is only in one dict - take it as is,
# example: {'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}

# initialize a common dictionary
# add the values with a unique key
# add the max values with common keys
# rename key for common keys
# delete added keys
common_dict = {}
for dict_number, dictionary in enumerate(list_result):
    for key in dictionary.keys():
        if key not in [letter[0] for letter in common_dict.keys()]:
            common_dict[key] = dictionary[key]
        elif dictionary[key] > common_dict[[unique_key for unique_key in common_dict.keys() if key in unique_key][0]]:
            common_dict[f'{key}_{dict_number+1}'] = dictionary[key]
            del common_dict[[unique_key for unique_key in common_dict.keys() if key in unique_key][0]]

# printing result
print("Task 2. Common list of dictionaries: ", common_dict)
