# Module 3. String Object

import re

# copy homework text to variable
start_text =  """homEwork:
	tHis iz your homeWork, copy these Text to variable. 

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE. 

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

# normalize text
list_of_text = re.split(r'(^|[.]\s|\n\t)', start_text)

normalized_text = ''

for i in list_of_text:
    normalized_text += i.capitalize()

# replace misspelling in normalized text
normalized_text_without_misspelling = normalized_text.replace(' iz ', ' is ')

# create sentence with last words of each existing sentence
sentences = [sentence for sentence in normalized_text_without_misspelling.split('.') if sentence]

last_sentence = []
for sentence in sentences:
    last_sentence.append(sentence.split()[-1])
last_sentence_text = ', '.join(last_sentence) + '.'

print(normalized_text_without_misspelling + '\n\n\t' + last_sentence_text.capitalize())

# calculate number of whitespace character
whitespace_characters = len(re.findall(r'\s', start_text))

print('\n\t' + 'Number of whitespace character: ', whitespace_characters)