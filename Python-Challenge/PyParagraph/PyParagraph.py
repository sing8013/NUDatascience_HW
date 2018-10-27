import re
import pandas as pd

text_file=open('raw_data/paragraph_1.txt','r')
#read entire 
read_f = text_file.read()
print(read_f)
# Assess the passage for each of the following:

  # Approximate word count
word_list=re.split(' ',read_f)
word_count=len(word_list)

  # Approximate sentence count
sentence_list=re.split("(?<=[.!?]) +",read_f)
sentence_count=len(sentence_list)

  # Approximate letter count (per word)
word_count_list=[len(x) for x in word_list]
avg_letter_count= sum(word_count_list)/len(word_count_list)
  # Average sentence length (in words)
sentence_len_list=[len(x) for x in sentence_list]
avg_sentence_len= sum(sentence_len_list)/len(sentence_len_list)

print(f'Paragraph Analysis')
print(f'-----------------')
print(f'Approximate Word Count: {word_count}')
print(f'Approximate Sentence Count: {sentence_count}')
print(f'Average Letter Count: {avg_letter_count}')
print(f'Average Sentence Length: {avg_sentence_len}')