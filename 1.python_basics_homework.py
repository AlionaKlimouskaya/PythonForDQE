# Module 1. Python Basics Homework

# Task 1. Create list of 100 random numbers from 0 to 1000
import random

# range function define 1001 as a parameter to select all values to 1000 inclusively
random_list = random.sample(range(1001), 100)

print("List of 100 random numbers: ", random_list)


# Task 2. Sort list from min to max (without using sort())
list_to_sort = random_list
sorted_list = []

while list_to_sort:
    min = list_to_sort[0]
    for element in list_to_sort:
        if element < min:
            min = element
    sorted_list.append(min)
    list_to_sort.remove(min)

print("Sorted list from min to max: ", sorted_list)


# Task 3. Calculate average for even and odd numbers
even_count, odd_count = 0, 0
even_sum, odd_sum = 0, 0

for element in sorted_list:

    # checking condition for even and odd numbers
    if element % 2 == 0:
        even_count += 1
        even_sum = even_sum + element

    else:
        odd_count += 1
        odd_sum = odd_sum + element

# average numbers were rounded to 2 decimal
even_average = round(even_sum / even_count, 2)
odd_average = round(odd_sum / odd_count, 2)

# Task 3. Calculate average for even and odd numbers with using list comprehension
only_odd = [num for num in sorted_list if num % 2 == 1]
only_even = [num for num in sorted_list if num % 2 == 0]

# Task 4. Print both average result in console
print("Average for even numbers (version 1): ", even_average)
print("Average for odd numbers (version 1): ", odd_average)
print("Average for even numbers (version 2): ", round(sum(only_even)/len(only_even), 2))
print("Average for odd numbers (version 2): ", round(sum(only_odd)/len(only_odd), 2))
